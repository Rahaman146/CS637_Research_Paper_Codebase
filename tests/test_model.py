"""
Unit tests for dataflow models and Extended HSDFGs.
"""

import pytest
import numpy as np

from src.model import (
    EventType,
    BoundType,
    Actor,
    Channel,
    TimingConstraint,
    ExtendedHSDFG,
    SDFGraph,
)


def test_actor_creation():
    a = Actor(0, "A", 5.0)
    assert a.id == 0
    assert a.name == "A"
    assert a.execution_time == 5.0

    with pytest.raises(ValueError):
        Actor(1, "Bad", -2.0)


def test_channel_creation():
    ch = Channel(0, 1, 2, initial_tokens=1, prd_rate=2, cns_rate=3)
    assert ch.initial_tokens == 1
    assert ch.prd_rate == 2
    assert ch.cns_rate == 3

    with pytest.raises(ValueError):
        Channel(1, 1, 2, initial_tokens=-1)


def test_extended_hsdfg_normalization():
    # 2 actors: A (w=3), B (w=4)
    # Channel: A -> B with 0 tokens => s_B(k) >= s_A(k) + 3
    # Upper bound: Completion of B within 10 units of Start of A:
    # c_B(k) - s_A(k) <= 10 => (s_B(k) + 4) - s_A(k) <= 10 => s_B(k) - s_A(k) <= 6
    # Reverse lower bound: s_A(k) - s_B(k) >= -6
    g = ExtendedHSDFG("TestGraph")
    a = g.add_actor("A", 3.0)
    b = g.add_actor("B", 4.0)
    g.add_channel(a, b, initial_tokens=0)
    g.add_upper_bound(a, EventType.START, b, EventType.COMPLETION, 10.0, delay=0)

    diffs = g.normalize_to_difference_constraints()
    assert len(diffs) == 2

    # Forward channel: A -> B with delay 0, weight 3.0
    fwd = next(d for d in diffs if not d.is_upper_bound_reverse)
    assert fwd.src_id == a
    assert fwd.dst_id == b
    assert fwd.delay == 0
    assert fwd.weight == 3.0

    # Reverse upper bound: B -> A with delay 0, weight -6.0
    rev = next(d for d in diffs if d.is_upper_bound_reverse)
    assert rev.src_id == b
    assert rev.dst_id == a
    assert rev.delay == 0
    assert rev.weight == -6.0


def test_sdf_repetition_vector():
    # Producer-consumer: P (prd=2) -> C (cns=3)
    # Balance: q(P)*2 = q(C)*3 => q(P)=3, q(C)=2
    sdf = SDFGraph("PC")
    p = sdf.add_actor("P", 1.0)
    c = sdf.add_actor("C", 1.0)
    sdf.add_channel(p, c, initial_tokens=0, prd_rate=2, cns_rate=3)

    q = sdf.compute_repetition_vector()
    assert q is not None
    assert q[p] == 3
    assert q[c] == 2


def test_sdf_to_hsdf_conversion():
    from src.scheduler import synthesize_asap_schedule

    sdf = SDFGraph("PC")
    p = sdf.add_actor("P", 2.0)
    c = sdf.add_actor("C", 3.0)
    sdf.add_channel(p, c, initial_tokens=0, prd_rate=2, cns_rate=3)

    # 1. Unconstrained mode: only dataflow token channels
    hsdf_unconstrained = sdf.to_hsdfg(preserve_actor_sequentiality=False)
    assert hsdf_unconstrained.num_actors == 5
    assert hsdf_unconstrained.num_channels == 6

    # 2. Sequential mode: enforces non-reentrant intra-actor execution
    # P: 3 instances (2 internal + 1 wrap-around = 3 channels)
    # C: 2 instances (1 internal + 1 wrap-around = 2 channels)
    # Total channels = 6 dataflow + 5 sequential = 11 channels
    hsdf_sequential = sdf.to_hsdfg(preserve_actor_sequentiality=True)
    assert hsdf_sequential.num_actors == 5
    assert hsdf_sequential.num_channels == 11

    # Verify that in sequential mode, instances execute sequentially without overlap
    sched = synthesize_asap_schedule(hsdf_sequential, iterations=1)
    assert sched.is_feasible
    # P instances: P_0 [0, 2], P_1 [2, 4], P_2 [4, 6]
    p0 = next(aid for aid, act in hsdf_sequential.actors.items() if act.name == "P_0")
    p1 = next(aid for aid, act in hsdf_sequential.actors.items() if act.name == "P_1")
    p2 = next(aid for aid, act in hsdf_sequential.actors.items() if act.name == "P_2")
    c0 = next(aid for aid, act in hsdf_sequential.actors.items() if act.name == "C_0")
    c1 = next(aid for aid, act in hsdf_sequential.actors.items() if act.name == "C_1")

    assert sched.get_start(p0, 0) == 0.0
    assert sched.get_start(p1, 0) >= 2.0
    assert sched.get_start(p2, 0) >= 4.0
    assert sched.get_start(c1, 0) >= sched.get_completion(c0, 0)
