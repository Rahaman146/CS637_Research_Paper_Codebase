"""
Unit tests for schedule synthesis engine.
"""

import pytest
import numpy as np

from src.model import ExtendedHSDFG, EventType
from src.scheduler import (
    synthesize_asap_schedule,
    synthesize_periodic_schedule,
    analyze_bound_slack,
)


def test_asap_pure_precedence():
    # Chain: A (w=2) -> B (w=3) -> C (w=1)
    g = ExtendedHSDFG("Chain")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    c = g.add_actor("C", 1.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_channel(b, c, initial_tokens=0)

    res = synthesize_asap_schedule(g, iterations=1)
    assert res.is_feasible
    assert res.get_start(a, 0) == 0.0
    assert res.get_start(b, 0) == 2.0
    assert res.get_start(c, 0) == 5.0
    assert res.get_completion(c, 0) == 6.0
    assert res.makespan == 6.0


def test_asap_with_lower_bound():
    # A (w=2) -> B (w=3)
    # Extra lower bound: Start of B must be at least 5 units after Start of A
    # s_B >= s_A + 5 (whereas precedence alone only requires s_B >= s_A + 2)
    g = ExtendedHSDFG("LowerBoundGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_lower_bound(a, EventType.START, b, EventType.START, 5.0, delay=0)

    res = synthesize_asap_schedule(g, iterations=1)
    assert res.is_feasible
    assert res.get_start(a, 0) == 0.0
    assert res.get_start(b, 0) == 5.0
    assert res.makespan == 8.0


def test_asap_with_upper_bound():
    # Two parallel tasks: A (w=2), B (w=10)
    # Task C (w=1) starts after both finish
    # Upper bound: Task A start to Task B start difference <= 1
    # s_B - s_A <= 1 (they must start almost synchronously)
    g = ExtendedHSDFG("SyncGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 10.0)
    g.add_upper_bound(a, EventType.START, b, EventType.START, 1.0, delay=0)

    res = synthesize_asap_schedule(g, iterations=1)
    assert res.is_feasible
    assert res.get_start(a, 0) == 0.0
    assert res.get_start(b, 0) == 0.0  # both can start at 0, diff = 0 <= 1


def test_asap_infeasible_schedule():
    # A (w=5) -> B (w=5)
    # Upper bound: Completion of B within 8 of Start of A
    # But s_B >= c_A = 5, c_B = s_B + 5 >= 10.
    # So c_B - s_A >= 10. Upper bound specifies <= 8!
    g = ExtendedHSDFG("InfeasibleGraph")
    a = g.add_actor("A", 5.0)
    b = g.add_actor("B", 5.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_upper_bound(a, EventType.START, b, EventType.COMPLETION, 8.0, delay=0)

    res = synthesize_asap_schedule(g, iterations=1)
    assert not res.is_feasible
    assert "positive cycle" in res.conflict_info.lower() or "contradictory" in res.conflict_info.lower()


def test_slack_analysis():
    g = ExtendedHSDFG("SlackGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)
    # Upper bound c_B - s_A <= 10. Actual is 5. Slack = 10 - 5 = 5.
    g.add_upper_bound(a, EventType.START, b, EventType.COMPLETION, 10.0, delay=0)

    res = synthesize_asap_schedule(g, iterations=1)
    slacks = analyze_bound_slack(g, res)
    assert len(slacks["upper_bounds"]) == 1
    ub_slack = slacks["upper_bounds"][0]
    assert ub_slack["actual_diff"] == 5.0
    assert ub_slack["slack"] == 5.0
    assert not ub_slack["is_binding"]


def test_scheduler_non_contiguous_actor_ids():
    from src.model import Actor
    g = ExtendedHSDFG("NonContig")
    g.actors[10] = Actor(10, "Task10", 2.0)
    g.actors[20] = Actor(20, "Task20", 3.0)
    g.add_channel(10, 20, initial_tokens=0)

    res = synthesize_asap_schedule(g, iterations=2)
    assert res.is_feasible
    assert res.get_start(10, 0) == 0.0
    assert res.get_start(20, 0) == 2.0
    assert res.get_start(10, 1) == 2.0
    assert res.get_start(20, 1) == 5.0


def test_scheduler_empty_and_zero_horizon():
    # Empty graph (0 actors)
    g_empty = ExtendedHSDFG("Empty")
    res_empty = synthesize_asap_schedule(g_empty, iterations=1)
    assert res_empty.is_feasible
    assert res_empty.makespan == 0.0
    assert res_empty.start_times.shape == (0, 1)

    # Normal graph with K=0 iterations
    g = ExtendedHSDFG("ZeroK")
    g.add_actor("A", 2.0)
    res_k0 = synthesize_asap_schedule(g, iterations=0)
    assert res_k0.is_feasible
    assert res_k0.makespan == 0.0
    assert res_k0.start_times.shape == (1, 0)


def test_scheduler_release_times():
    g = ExtendedHSDFG("ReleaseGraph")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)

    # Actor A released at t=5.0
    res = synthesize_asap_schedule(g, iterations=1, release_times={a: 5.0})
    assert res.is_feasible
    assert res.get_start(a, 0) == 5.0
    assert res.get_start(b, 0) == 7.0
    assert res.makespan == 10.0


def test_synthesize_periodic_schedule_feedback_loop():
    # Feedback cycle: A (w=2.0) -> B (w=3.0) with delay 0, B -> A with 1 initial token
    # Cycle weight = 2.0 + 3.0 = 5.0; delay = 1.
    # Analytical period lambda* = 5.0 => Throughput = 1 / 5.0 = 0.2
    g = ExtendedHSDFG("FeedbackCycle")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_channel(b, a, initial_tokens=1)

    sched = synthesize_periodic_schedule(g, max_test_iterations=6)
    assert sched.is_feasible
    assert sched.throughput is not None
    assert pytest.approx(sched.throughput, rel=1e-5) == 0.2


def test_periodic_schedule_disconnected_bottleneck():
    # Adversarial test: Disconnected components with mismatched cycle periods.
    # Component 1: A (w=5) -> B (w=5), lower bound 35 with delay 2 -> cycle period 20.0 (throughput 0.05)
    # Component 2: C (w=2) -> D (w=3) with delay 1 feedback -> cycle period 5.0 (throughput 0.20)
    # True system bottleneck throughput is min(0.05, 0.20) = 0.05 (period 20.0).
    # Previous buggy arithmetic mean gave 0.085714. Bottleneck max period yields exact 0.05.
    g = ExtendedHSDFG("DisconnectedBottleneck")
    a = g.add_actor("A", 5.0)
    b = g.add_actor("B", 5.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_channel(b, a, initial_tokens=2)
    g.add_lower_bound(b, EventType.START, a, EventType.START, 35.0, delay=2)

    c = g.add_actor("C", 2.0)
    d = g.add_actor("D", 3.0)
    g.add_channel(c, d, initial_tokens=0)
    g.add_channel(d, c, initial_tokens=1)

    sched = synthesize_periodic_schedule(g, max_test_iterations=10)
    assert sched.is_feasible
    assert sched.throughput is not None
    assert pytest.approx(sched.throughput, rel=1e-5) == 0.05


def test_synthesize_strictly_periodic_schedule():
    g = ExtendedHSDFG("StrictPeriodic")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_channel(b, a, initial_tokens=1)

    # Strictly 1-periodic schedule
    sched = synthesize_periodic_schedule(g, max_test_iterations=5, strictly_periodic=True)
    assert sched.is_feasible
    # Period is 5.0. For each actor, s(k) - s(k-1) should be exactly 5.0 for all k
    for k in range(1, 5):
        assert pytest.approx(sched.get_start(a, k) - sched.get_start(a, k - 1)) == 5.0
        assert pytest.approx(sched.get_start(b, k) - sched.get_start(b, k - 1)) == 5.0


def test_scheduler_unknown_actor_id_raises_key_error():
    g = ExtendedHSDFG("KeyErrorTest")
    a = g.add_actor("A", 2.0)
    res = synthesize_asap_schedule(g, iterations=1)
    assert res.is_feasible
    with pytest.raises(KeyError, match="not found in schedule"):
        res.get_start(999, 0)
    with pytest.raises(KeyError, match="not found in schedule"):
        res.get_completion(999, 0)


def test_scheduler_invalid_iteration_index_raises_index_error():
    g = ExtendedHSDFG("IndexErrorTest")
    a = g.add_actor("A", 2.0)
    res = synthesize_asap_schedule(g, iterations=2)
    assert res.is_feasible
    with pytest.raises(IndexError, match="out of range"):
        res.get_start(a, -1)
    with pytest.raises(IndexError, match="out of range"):
        res.get_start(a, 5)
    with pytest.raises(IndexError, match="out of range"):
        res.get_completion(a, -1)
    with pytest.raises(IndexError, match="out of range"):
        res.get_completion(a, 5)
