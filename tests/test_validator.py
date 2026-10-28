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
