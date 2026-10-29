"""
Independent Schedule and Constraint Validator.
Decoupled verification of schedules produced by the max-plus synthesis engine.
Validates:
1. Non-negativity of start times: s_v(k) >= 0
2. Intra-actor non-overlapping firings: s_v(k+1) >= s_v(k) + w(v)
3. Dataflow FIFO channel precedence: s_v(k) >= s_u(k - d(e)) + w(u)
4. Lower-bound timing constraints: t_dst(k) - t_src(k - delta) >= L - epsilon
5. Upper-bound timing constraints: t_dst(k) - t_src(k - delta) <= U + epsilon
"""

from typing import List, Dict, Optional, Tuple, NamedTuple
import numpy as np

from .model import ExtendedHSDFG, EventType, BoundType
from .scheduler import ScheduleResult


class ConstraintViolation(NamedTuple):
    category: str
    description: str
    iteration: int
    expected_bound: float
    actual_value: float
    error_margin: float


class ValidationResult:
    """Detailed validation verdict and diagnostic report."""

    def __init__(
        self,
        is_valid: bool,
        total_checks: int,
        passed_checks: int,
        max_residual_error: float,
        violations: List[ConstraintViolation],
    ):
        self.is_valid = is_valid
        self.total_checks = total_checks
        self.passed_checks = passed_checks
        self.max_residual_error = max_residual_error
        self.violations = violations

    def __repr__(self):
        status = "PASSED" if self.is_valid else f"FAILED ({len(self.violations)} violations)"
        return (
            f"ValidationResult({status}: {self.passed_checks}/{self.total_checks} checks passed, "
            f"max_error={self.max_residual_error:.2e})"
        )


class IndependentValidator:
    """
    Independent schedule verification engine.
    Does not reuse any max-plus matrices, shortest path or Kleene star logic.
    Directly computes ground truth event differences and tests every inequality.
    """

    def __init__(self, tolerance: float = 1e-7):
        self.tolerance = tolerance

    def validate(
        self,
        graph: ExtendedHSDFG,
        schedule: ScheduleResult,
        release_times: Optional[Dict] = None,
    ) -> ValidationResult:
        if not schedule.is_feasible:
            return ValidationResult(
                is_valid=False,
                total_checks=1,
                passed_checks=0,
                max_residual_error=float("inf"),
                violations=[
                    ConstraintViolation(
                        category="Feasibility",
                        description="Schedule was marked infeasible by synthesis engine",
                        iteration=0,
                        expected_bound=0.0,
                        actual_value=-1.0,
                        error_margin=1.0,
                    )
                ],
            )

        n = graph.num_actors
        K = schedule.iterations

        # An empty graph or zero-horizon schedule trivially satisfies all constraints
        if n == 0 or K == 0:
            return ValidationResult(
                is_valid=True,
                total_checks=0,
                passed_checks=0,
                max_residual_error=0.0,
                violations=[],
            )

        if schedule.start_times is None:
            return ValidationResult(
                is_valid=False,
                total_checks=1,
                passed_checks=0,
                max_residual_error=float("inf"),
                violations=[
                    ConstraintViolation(
                        category="Feasibility",
                        description="Schedule start times matrix is None",
                        iteration=0,
                        expected_bound=0.0,
                        actual_value=-1.0,
                        error_margin=1.0,
                    )
                ],
            )

        # Validate schedule array dimensions match graph
        if schedule.start_times.shape != (n, K):
            return ValidationResult(
                is_valid=False,
                total_checks=1,
                passed_checks=0,
                max_residual_error=float("inf"),
                violations=[
                    ConstraintViolation(
                        category="MalformedSchedule",
                        description=f"start_times shape {schedule.start_times.shape} does not match expected ({n}, {K})",
                        iteration=0,
                        expected_bound=float(n),
                        actual_value=float(schedule.start_times.shape[0]),
                        error_margin=1.0,
                    )
                ],
            )

        if schedule.actor_to_idx is not None:
            missing_actors = [aid for aid in graph.actors if aid not in schedule.actor_to_idx]
            if missing_actors:
                return ValidationResult(
                    is_valid=False,
                    total_checks=1,
                    passed_checks=0,
                    max_residual_error=float("inf"),
                    violations=[
                        ConstraintViolation(
                            category="MalformedSchedule",
                            description=f"Actors {missing_actors} missing from schedule actor_to_idx mapping",
                            iteration=0,
                            expected_bound=0.0,
                            actual_value=float(len(missing_actors)),
                            error_margin=float(len(missing_actors)),
                        )
                    ],
                )

        violations: List[ConstraintViolation] = []
        total_checks = 0
        passed_checks = 0
        max_residual_error = 0.0

        # Validate completion times consistency: c_v(k) == s_v(k) + w(v)
        if schedule.completion_times is not None:
            if schedule.completion_times.shape != (n, K):
                return ValidationResult(
                    is_valid=False,
                    total_checks=1,
                    passed_checks=0,
                    max_residual_error=float("inf"),
                    violations=[
                        ConstraintViolation(
                            category="MalformedSchedule",
                            description=f"completion_times shape {schedule.completion_times.shape} does not match expected ({n}, {K})",
                            iteration=0,
                            expected_bound=float(n),
                            actual_value=float(schedule.completion_times.shape[0]),
                            error_margin=1.0,
                        )
                    ],
                )

            for aid, actor in graph.actors.items():
                for k in range(K):
                    total_checks += 1
                    c_act = schedule.get_completion(aid, k)
                    s_act = schedule.get_start(aid, k)
                    exp_c = s_act + actor.execution_time
                    err = abs(c_act - exp_c)
                    if err > self.tolerance:
                        max_residual_error = max(max_residual_error, err)
                        violations.append(
                            ConstraintViolation(
                                category="CompletionTime",
                                description=f"Actor {actor.name} completion time {c_act} != start {s_act} + duration {actor.execution_time}",
                                iteration=k,
                                expected_bound=exp_c,
                                actual_value=c_act,
                                error_margin=err,
                            )
                        )
                    else:
                        passed_checks += 1

        # Validate makespan consistency: makespan == max_{v, k} c_v(k)
        if schedule.completion_times is not None and schedule.completion_times.size > 0:
            total_checks += 1
            calc_makespan = float(np.max(schedule.completion_times))
            m_err = abs(schedule.makespan - calc_makespan)
            if m_err > self.tolerance:
                max_residual_error = max(max_residual_error, m_err)
                violations.append(
                    ConstraintViolation(
                        category="Makespan",
                        description=f"Reported makespan {schedule.makespan} != maximum completion time {calc_makespan}",
                        iteration=K - 1,
                        expected_bound=calc_makespan,
                        actual_value=schedule.makespan,
                        error_margin=m_err,
                    )
                )
            else:
                passed_checks += 1

        # Helper to get event time
        def get_event_time(aid: int, k: int, etype: EventType) -> float:
            st = schedule.get_start(aid, k)
            w = graph.actors[aid].execution_time
            return st + (w if etype == EventType.COMPLETION else 0.0)

        # 1. Non-negativity and release-time check
        for aid, actor in graph.actors.items():
            for k in range(K):
                total_checks += 1
                st = schedule.get_start(aid, k)
                r_min = 0.0
                if k == 0 and release_times:
                    if aid in release_times:
                        r_min = float(release_times[aid])
                    elif actor.name in release_times:
                        r_min = float(release_times[actor.name])

                if st < r_min - self.tolerance:
                    err = r_min - st
                    max_residual_error = max(max_residual_error, err)
                    violations.append(
                        ConstraintViolation(
                            category="Non-negativity" if r_min == 0.0 else "ReleaseTime",
                            description=f"Actor {actor.name} starts before required time {r_min}",
                            iteration=k,
                            expected_bound=r_min,
                            actual_value=st,
                            error_margin=err,
                        )
                    )
                else:
                    passed_checks += 1

        # 2. Sequential intra-actor execution: s_v(k+1) >= s_v(k) + w(v)
        for aid, actor in graph.actors.items():
            w = actor.execution_time
            for k in range(K - 1):
                total_checks += 1
                s_curr = schedule.get_start(aid, k)
                s_next = schedule.get_start(aid, k + 1)
                diff = s_next - (s_curr + w)
                if diff < -self.tolerance:
                    err = -diff
                    max_residual_error = max(max_residual_error, err)
                    violations.append(
                        ConstraintViolation(
                            category="Sequentiality",
                            description=f"Actor {actor.name} firing {k+1} starts before firing {k} completes",
                            iteration=k + 1,
                            expected_bound=s_curr + w,
                            actual_value=s_next,
                            error_margin=err,
                        )
                    )
                else:
                    passed_checks += 1

        # 3. Dataflow FIFO channel precedence: s_v(k) >= s_u(k - d) + w(u)
        for ch in graph.channels.values():
            w_u = graph.actors[ch.src_id].execution_time
            d = ch.initial_tokens
            for k in range(K):
                k_src = k - d
                if 0 <= k_src < K:
                    total_checks += 1
                    s_u = schedule.get_start(ch.src_id, k_src)
                    s_v = schedule.get_start(ch.dst_id, k)
                    diff = s_v - (s_u + w_u)
                    if diff < -self.tolerance:
                        err = -diff
                        max_residual_error = max(max_residual_error, err)
                        violations.append(
                            ConstraintViolation(
                                category="DataflowPrecedence",
                                description=(
                                    f"Channel {ch.id} ({graph.actors[ch.src_id].name} -> "
                                    f"{graph.actors[ch.dst_id].name}) precedence violated"
                                ),
                                iteration=k,
                                expected_bound=s_u + w_u,
                                actual_value=s_v,
                                error_margin=err,
                            )
                        )
                    else:
                        passed_checks += 1

        # 4. Explicit Lower-bound and Upper-bound timing constraints
        for ct in graph.constraints:
            for k in range(K):
                k_src = k - ct.delay
                if 0 <= k_src < K:
                    total_checks += 1
                    t_src = get_event_time(ct.src_id, k_src, ct.src_event)
                    t_dst = get_event_time(ct.dst_id, k, ct.dst_event)
                    diff = t_dst - t_src

                    if ct.bound_type == BoundType.LOWER:
                        # t_dst - t_src >= bound_value
                        slack = diff - ct.bound_value
                        if slack < -self.tolerance:
                            err = -slack
                            max_residual_error = max(max_residual_error, err)
                            violations.append(
                                ConstraintViolation(
                                    category="LowerBound",
                                    description=(
                                        f"Constraint {ct.id}: {graph.actors[ct.dst_id].name}.{ct.dst_event.name}(k) - "
                                        f"{graph.actors[ct.src_id].name}.{ct.src_event.name}(k-{ct.delay}) < {ct.bound_value}"
                                    ),
                                    iteration=k,
                                    expected_bound=ct.bound_value,
                                    actual_value=diff,
                                    error_margin=err,
                                )
                            )
                        else:
                            passed_checks += 1
                    else:
                        # t_dst - t_src <= bound_value
                        excess = diff - ct.bound_value
                        if excess > self.tolerance:
                            err = excess
                            max_residual_error = max(max_residual_error, err)
                            violations.append(
                                ConstraintViolation(
                                    category="UpperBound",
                                    description=(
                                        f"Constraint {ct.id}: {graph.actors[ct.dst_id].name}.{ct.dst_event.name}(k) - "
                                        f"{graph.actors[ct.src_id].name}.{ct.src_event.name}(k-{ct.delay}) > {ct.bound_value}"
                                    ),
                                    iteration=k,
                                    expected_bound=ct.bound_value,
                                    actual_value=diff,
                                    error_margin=err,
                                )
                            )
                        else:
                            passed_checks += 1

        is_valid = len(violations) == 0
        return ValidationResult(
            is_valid=is_valid,
            total_checks=total_checks,
            passed_checks=passed_checks,
            max_residual_error=max_residual_error,
            violations=violations,
        )


def verify_schedule_legality(
    graph: ExtendedHSDFG,
    schedule: ScheduleResult,
    release_times: Optional[Dict] = None,
) -> bool:
    """Convenience functional interface for independent validation."""
    validator = IndependentValidator()
    result = validator.validate(graph, schedule, release_times=release_times)
    return result.is_valid
