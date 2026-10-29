"""
Unit and integration tests for Independent Schedule Validator.
"""

import pytest
import numpy as np

from src.model import ExtendedHSDFG, EventType
from src.scheduler import synthesize_asap_schedule, ScheduleResult
from src.validator import IndependentValidator, verify_schedule_legality


def test_validator_on_valid_schedule():
    g = ExtendedHSDFG("ValidGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_lower_bound(a, EventType.START, b, EventType.START, 4.0, delay=0)
    g.add_upper_bound(a, EventType.START, b, EventType.COMPLETION, 12.0, delay=0)

    sched = synthesize_asap_schedule(g, iterations=3)
    assert sched.is_feasible

    validator = IndependentValidator()
    val_res = validator.validate(g, sched)
    assert val_res.is_valid
    assert len(val_res.violations) == 0
    assert val_res.passed_checks == val_res.total_checks
    assert verify_schedule_legality(g, sched)


def test_validator_detects_tampered_negative_start():
    g = ExtendedHSDFG("TamperedGraph")
    a = g.add_actor("A", 2.0)

    # Manually constructed invalid schedule with negative start
    bad_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.array([[-1.0]]),
        completion_times=np.array([[1.0]]),
        makespan=1.0,
        iterations=1,
    )

    validator = IndependentValidator()
    val_res = validator.validate(g, bad_sched)
    assert not val_res.is_valid
    assert any(v.category == "Non-negativity" for v in val_res.violations)


def test_validator_detects_precedence_violation():
    g = ExtendedHSDFG("PrecedenceGraph")
    a = g.add_actor("A", 5.0)
    b = g.add_actor("B", 2.0)
    g.add_channel(a, b, initial_tokens=0)

    # Manually constructed schedule where B starts before A finishes
    # A starts at 0, completes at 5; but B starts at 3!
    bad_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.array([[0.0], [3.0]]),
        completion_times=np.array([[5.0], [5.0]]),
        makespan=5.0,
        iterations=1,
    )

    validator = IndependentValidator()
    val_res = validator.validate(g, bad_sched)
    assert not val_res.is_valid
    assert any(v.category == "DataflowPrecedence" for v in val_res.violations)


def test_validator_detects_upper_bound_violation():
    g = ExtendedHSDFG("UBViolationGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 2.0)
    g.add_channel(a, b, initial_tokens=0)
    # Upper bound: Completion of B within 3 of Start of A
    g.add_upper_bound(a, EventType.START, b, EventType.COMPLETION, 3.0, delay=0)

    # Schedule where B completes at 4 (diff = 4 > 3)
    bad_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.array([[0.0], [2.0]]),
        completion_times=np.array([[2.0], [4.0]]),
        makespan=4.0,
        iterations=1,
    )

    validator = IndependentValidator()
    val_res = validator.validate(g, bad_sched)
    assert not val_res.is_valid
    assert any(v.category == "UpperBound" for v in val_res.violations)


def test_validator_detects_sequentiality_violation():
    # Actor A has w=3. Firing 0 at t=0 completes at 3.
    # Bad schedule starts firing 1 at t=2 < 3!
    g = ExtendedHSDFG("SeqViolationGraph")
    a = g.add_actor("A", 3.0)

    bad_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.array([[0.0, 2.0]]),
        completion_times=np.array([[3.0, 5.0]]),
        makespan=5.0,
        iterations=2,
    )

    validator = IndependentValidator()
    val_res = validator.validate(g, bad_sched)
    assert not val_res.is_valid
    assert any(v.category == "Sequentiality" for v in val_res.violations)


def test_validator_detects_lower_bound_violation():
    # Actor A (w=2) and B (w=2). Lower bound: s_B - s_A >= 5.0.
    # Bad schedule starts B at t=3.0 (diff = 3.0 < 5.0).
    g = ExtendedHSDFG("LBViolationGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 2.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_lower_bound(a, EventType.START, b, EventType.START, 5.0, delay=0)

    bad_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.array([[0.0], [3.0]]),
        completion_times=np.array([[2.0], [5.0]]),
        makespan=5.0,
        iterations=1,
    )

    validator = IndependentValidator()
    val_res = validator.validate(g, bad_sched)
    assert not val_res.is_valid
    assert any(v.category == "LowerBound" for v in val_res.violations)


def test_zero_weight_cycle_feasibility():
    # Exact equality constraint: s_B - s_A >= 4.0 and s_B - s_A <= 4.0
    # Forms a zero-weight cycle in difference constraint graph.
    g = ExtendedHSDFG("ZeroWeightCycleGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 2.0)
    g.add_lower_bound(a, EventType.START, b, EventType.START, 4.0, delay=0)
    g.add_upper_bound(a, EventType.START, b, EventType.START, 4.0, delay=0)

    sched = synthesize_asap_schedule(g, iterations=2)
    assert sched.is_feasible
    assert sched.get_start(a, 0) == 0.0
    assert sched.get_start(b, 0) == 4.0
    assert sched.get_start(b, 0) - sched.get_start(a, 0) == 4.0

    validator = IndependentValidator()
    val_res = validator.validate(g, sched)
    assert val_res.is_valid


def test_adversarial_cyclic_contradiction():
    # 3-hop cyclic bound: A -> B (wt >= 3), B -> C (wt >= 4), C -> A (upper bound <= 5)
    # Total path A -> B -> C is >= 7, but C -> A requires c_C - s_A <= 5 => contradiction!
    g = ExtendedHSDFG("AdversarialCycle")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 2.0)
    c = g.add_actor("C", 2.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_channel(b, c, initial_tokens=0)
    # End-to-end upper bound: c_C - s_A <= 5.0 (whereas precedence requires >= 6.0)
    g.add_upper_bound(a, EventType.START, c, EventType.COMPLETION, 5.0, delay=0)

    sched = synthesize_asap_schedule(g, iterations=1)
    assert not sched.is_feasible
    assert "positive cycle" in sched.conflict_info.lower()


def test_validator_empty_graph_and_zero_horizon():
    validator = IndependentValidator()

    # Empty graph
    g_empty = ExtendedHSDFG("Empty")
    sched_empty = synthesize_asap_schedule(g_empty, iterations=1)
    res_empty = validator.validate(g_empty, sched_empty)
    assert res_empty.is_valid
    assert res_empty.total_checks == 0
    assert len(res_empty.violations) == 0

    # Normal graph with K=0 iterations
    g = ExtendedHSDFG("ZeroK")
    g.add_actor("A", 2.0)
    sched_k0 = synthesize_asap_schedule(g, iterations=0)
    res_k0 = validator.validate(g, sched_k0)
    assert res_k0.is_valid
    assert res_k0.total_checks == 0


def test_validator_arbitrary_actor_ids():
    from src.model import Actor
    g = ExtendedHSDFG("NonContig")
    g.actors[55] = Actor(55, "Task55", 2.0)
    g.actors[99] = Actor(99, "Task99", 3.0)
    g.add_channel(55, 99, initial_tokens=0)

    sched = synthesize_asap_schedule(g, iterations=2)
    assert sched.is_feasible

    validator = IndependentValidator()
    res = validator.validate(g, sched)
    assert res.is_valid
    assert res.total_checks > 0
    assert len(res.violations) == 0


def test_validator_release_times():
    g = ExtendedHSDFG("RelVal")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)

    # Valid schedule respecting release time
    sched = synthesize_asap_schedule(g, iterations=1, release_times={a: 10.0})
    validator = IndependentValidator()
    res = validator.validate(g, sched, release_times={a: 10.0})
    assert res.is_valid

    # Schedule where actor A starts before required release time
    res_bad = validator.validate(g, sched, release_times={a: 15.0})
    assert not res_bad.is_valid
    assert any(v.category == "ReleaseTime" for v in res_bad.violations)


def test_validator_detects_tampered_completion_time():
    g = ExtendedHSDFG("TamperedComp")
    a = g.add_actor("A", 5.0)
    sched = synthesize_asap_schedule(g, iterations=1)
    assert sched.is_feasible

    # Forged completion time: should be 0.0 + 5.0 = 5.0, tampered to 999.0
    tampered = ScheduleResult(
        is_feasible=True,
        start_times=np.copy(sched.start_times),
        completion_times=np.array([[999.0]]),
        makespan=999.0,
        iterations=1,
        actor_to_idx=sched.actor_to_idx,
    )
    val = IndependentValidator()
    res = val.validate(g, tampered)
    assert not res.is_valid
    assert any(v.category == "CompletionTime" for v in res.violations)


def test_validator_detects_tampered_makespan():
    g = ExtendedHSDFG("TamperedMakespan")
    a = g.add_actor("A", 5.0)
    sched = synthesize_asap_schedule(g, iterations=1)
    assert sched.is_feasible

    # Forged makespan: should be 5.0, tampered to 0.0
    tampered = ScheduleResult(
        is_feasible=True,
        start_times=np.copy(sched.start_times),
        completion_times=np.copy(sched.completion_times),
        makespan=0.0,
        iterations=1,
        actor_to_idx=sched.actor_to_idx,
    )
    val = IndependentValidator()
    res = val.validate(g, tampered)
    assert not res.is_valid
    assert any(v.category == "Makespan" for v in res.violations)


def test_validator_detects_shape_mismatch():
    g = ExtendedHSDFG("ShapeMismatch")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)

    # Schedule has shape (1, 1) instead of (2, 1)
    bad_shape_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.zeros((1, 1)),
        completion_times=np.array([[2.0]]),
        makespan=2.0,
        iterations=1,
        actor_to_idx={a: 0},
    )
    val = IndependentValidator()
    res = val.validate(g, bad_shape_sched)
    assert not res.is_valid
    assert any(v.category == "MalformedSchedule" for v in res.violations)


def test_validator_detects_missing_actor_mapping():
    g = ExtendedHSDFG("MissingActorMap")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)

    # Actor B is missing from actor_to_idx mapping
    bad_map_sched = ScheduleResult(
        is_feasible=True,
        start_times=np.zeros((2, 1)),
        completion_times=np.array([[2.0], [3.0]]),
        makespan=3.0,
        iterations=1,
        actor_to_idx={a: 0},  # B missing
    )
    val = IndependentValidator()
    res = val.validate(g, bad_map_sched)
    assert not res.is_valid
    assert any(v.category == "MalformedSchedule" for v in res.violations)
