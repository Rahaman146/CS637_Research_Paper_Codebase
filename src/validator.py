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
    ) -> ValidationResult:
        if not schedule.is_feasible or schedule.start_times is None:
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
        violations: List[ConstraintViolation] = []
        total_checks = 0
        passed_checks = 0
        max_residual_error = 0.0

        # Helper to get event time
        def get_event_time(aid: int, k: int, etype: EventType) -> float:
            st = schedule.get_start(aid, k)
            w = graph.actors[aid].execution_time
            return st + (w if etype == EventType.COMPLETION else 0.0)

        # 1. Non-negativity check
        for aid in range(n):
            for k in range(K):
                total_checks += 1
                st = schedule.get_start(aid, k)
                if st < -self.tolerance:
                    err = -st
                    max_residual_error = max(max_residual_error, err)
                    violations.append(
                        ConstraintViolation(
                            category="Non-negativity",
                            description=f"Actor {graph.actors[aid].name} has negative start time",
                            iteration=k,
                            expected_bound=0.0,
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


def verify_schedule_legality(graph: ExtendedHSDFG, schedule: ScheduleResult) -> bool:
    """Convenience functional interface for independent validation."""
    validator = IndependentValidator()
    result = validator.validate(graph, schedule)
    return result.is_valid
