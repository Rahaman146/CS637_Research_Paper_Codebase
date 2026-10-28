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
