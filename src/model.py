"""
Data structures and graph models for Synchronous Dataflow (SDF) and
Extended Homogeneous Synchronous Dataflow Graphs (Extended HSDFG)
with Lower and Upper Timing Bounds.
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, NamedTuple
import math
import numpy as np


class EventType(Enum):
    START = "START"
    COMPLETION = "COMPLETION"


class BoundType(Enum):
    LOWER = "LOWER"
    UPPER = "UPPER"


class Actor:
    def __init__(self, actor_id: int, name: str, execution_time: float):
        if execution_time < 0:
            raise ValueError(f"Actor execution time cannot be negative: {execution_time}")
        self.id = actor_id
        self.name = name
        self.execution_time = float(execution_time)

    def __repr__(self):
        return f"Actor({self.id}, '{self.name}', w={self.execution_time})"


class Channel:
    def __init__(
        self,
        channel_id: int,
        src_actor_id: int,
        dst_actor_id: int,
        initial_tokens: int = 0,
        prd_rate: int = 1,
        cns_rate: int = 1,
    ):
        if initial_tokens < 0:
            raise ValueError("Initial tokens cannot be negative")
        if prd_rate <= 0 or cns_rate <= 0:
            raise ValueError("Token production and consumption rates must be strictly positive")
        self.id = channel_id
        self.src_id = src_actor_id
        self.dst_id = dst_actor_id
        self.initial_tokens = int(initial_tokens)
        self.prd_rate = int(prd_rate)
        self.cns_rate = int(cns_rate)

    def __repr__(self):
        return (
            f"Channel({self.id}: {self.src_id} -> {self.dst_id}, "
            f"tokens={self.initial_tokens}, prd={self.prd_rate}, cns={self.cns_rate})"
        )


class TimingConstraint:
    """
    Timing constraint between two events:
    Event difference: dst_event(k) - src_event(k - delay)
    If bound_type == LOWER: dst_event(k) - src_event(k - delay) >= bound_value
    If bound_type == UPPER: dst_event(k) - src_event(k - delay) <= bound_value
    """

    def __init__(
        self,
        constraint_id: int,
        src_actor_id: int,
        src_event: EventType,
        dst_actor_id: int,
        dst_event: EventType,
        bound_type: BoundType,
        bound_value: float,
        delay: int = 0,
    ):
        self.id = constraint_id
        self.src_id = src_actor_id
        self.src_event = src_event
        self.dst_id = dst_actor_id
        self.dst_event = dst_event
        self.bound_type = bound_type
        self.bound_value = float(bound_value)
        self.delay = int(delay)

    def __repr__(self):
        op = ">=" if self.bound_type == BoundType.LOWER else "<="
        return (
            f"TimingConstraint({self.id}: {self.dst_id}.{self.dst_event.name}(k) - "
            f"{self.src_id}.{self.src_event.name}(k-{self.delay}) {op} {self.bound_value})"
        )


class NormalizedDifferenceConstraint(NamedTuple):
    """
    Standard difference inequality on start times:
    s_{dst}(k) - s_{src}(k - delay) >= weight
    """
    src_id: int
    dst_id: int
    delay: int
    weight: float
    original_constraint_id: Optional[int]
    is_upper_bound_reverse: bool


class ExtendedHSDFG:
    """
    Extended Homogeneous Synchronous Dataflow Graph (HSDFG) supporting:
    - Actor nodes with deterministic execution times w(v) >= 0
    - Dataflow FIFO channels (prd=1, cns=1) with initial tokens d(e) >= 0
    - Explicit lower-bound timing constraints (C_L)
    - Explicit upper-bound timing constraints (C_U)
    """

    def __init__(self, name: str = "ExtendedHSDFG"):
        self.name = name
        self.actors: Dict[int, Actor] = {}
        self.channels: Dict[int, Channel] = {}
        self.constraints: List[TimingConstraint] = []
        self._next_actor_id = 0
        self._next_channel_id = 0
        self._next_constraint_id = 0

    @property
    def num_actors(self) -> int:
        return len(self.actors)

    @property
    def num_channels(self) -> int:
        return len(self.channels)

    @property
    def num_constraints(self) -> int:
        return len(self.constraints)

    def add_actor(self, name: str, execution_time: float) -> int:
        aid = self._next_actor_id
        self._next_actor_id += 1
        self.actors[aid] = Actor(aid, name, execution_time)
        return aid

    def add_channel(self, src_id: int, dst_id: int, initial_tokens: int = 0) -> int:
        if src_id not in self.actors or dst_id not in self.actors:
            raise KeyError("Channel source and destination actors must exist in the graph")
        cid = self._next_channel_id
        self._next_channel_id += 1
        self.channels[cid] = Channel(cid, src_id, dst_id, initial_tokens, prd_rate=1, cns_rate=1)
        return cid

    def add_lower_bound(
        self,
        src_id: int,
        src_event: EventType,
        dst_id: int,
        dst_event: EventType,
        bound_value: float,
        delay: int = 0,
    ) -> int:
        if src_id not in self.actors or dst_id not in self.actors:
            raise KeyError("Constraint source and destination actors must exist in the graph")
        cid = self._next_constraint_id
        self._next_constraint_id += 1
        ct = TimingConstraint(
            cid, src_id, src_event, dst_id, dst_event, BoundType.LOWER, bound_value, delay
        )
        self.constraints.append(ct)
        return cid

    def add_upper_bound(
        self,
        src_id: int,
        src_event: EventType,
        dst_id: int,
        dst_event: EventType,
        bound_value: float,
        delay: int = 0,
    ) -> int:
        if src_id not in self.actors or dst_id not in self.actors:
            raise KeyError("Constraint source and destination actors must exist in the graph")
        cid = self._next_constraint_id
        self._next_constraint_id += 1
        ct = TimingConstraint(
            cid, src_id, src_event, dst_id, dst_event, BoundType.UPPER, bound_value, delay
        )
        self.constraints.append(ct)
        return cid

    def normalize_to_difference_constraints(self) -> List[NormalizedDifferenceConstraint]:
        """
        Translates all dataflow edges, lower bounds, and upper bounds into a unified
        set of linear difference inequalities on start times:
        s_{dst}(k) - s_{src}(k - delay) >= weight
        """
        diff_constraints: List[NormalizedDifferenceConstraint] = []

        # 1. Standard dataflow edges: s_dst(k) >= c_src(k - delay) = s_src(k - delay) + w(src)
        for ch in self.channels.values():
            w_src = self.actors[ch.src_id].execution_time
            diff_constraints.append(
                NormalizedDifferenceConstraint(
                    src_id=ch.src_id,
                    dst_id=ch.dst_id,
                    delay=ch.initial_tokens,
                    weight=w_src,
                    original_constraint_id=None,
                    is_upper_bound_reverse=False,
                )
            )

        # 2. Explicit timing constraints
        for ct in self.constraints:
            w_src = self.actors[ct.src_id].execution_time
            w_dst = self.actors[ct.dst_id].execution_time

            # Compute adjustment from (starts, completions) to starts:
            # dst_event(k) - src_event(k - delta)
            # dst_event = s_dst if START else s_dst + w_dst
            # src_event = s_src if START else s_src + w_src
            dst_offset = w_dst if ct.dst_event == EventType.COMPLETION else 0.0
            src_offset = w_src if ct.src_event == EventType.COMPLETION else 0.0

            # (s_dst + dst_offset) - (s_src + src_offset) = s_dst - s_src + (dst_offset - src_offset)
            # delta_offset = dst_offset - src_offset
            delta_offset = dst_offset - src_offset

            if ct.bound_type == BoundType.LOWER:
                # s_dst(k) - s_src(k - delay) + delta_offset >= bound_value
                # => s_dst(k) - s_src(k - delay) >= bound_value - delta_offset
                weight = ct.bound_value - delta_offset
                diff_constraints.append(
                    NormalizedDifferenceConstraint(
                        src_id=ct.src_id,
                        dst_id=ct.dst_id,
                        delay=ct.delay,
                        weight=weight,
                        original_constraint_id=ct.id,
                        is_upper_bound_reverse=False,
                    )
                )
            else:
                # Upper bound:
                # s_dst(k) - s_src(k - delay) + delta_offset <= bound_value
                # => s_dst(k) - s_src(k - delay) <= bound_value - delta_offset = U'
                # Rewriting as a lower bound on reverse edge:
                # s_src(k - delay) - s_dst(k) >= -U'
                u_prime = ct.bound_value - delta_offset
                diff_constraints.append(
                    NormalizedDifferenceConstraint(
                        src_id=ct.dst_id,
                        dst_id=ct.src_id,
                        delay=-ct.delay,
                        weight=-u_prime,
                        original_constraint_id=ct.id,
                        is_upper_bound_reverse=True,
                    )
                )

        return diff_constraints


class SDFGraph:
    """
    General Multi-Rate Synchronous Dataflow Graph.
    Supports arbitrary production/consumption rates, topology matrix generation,
    consistency verification, repetition vector computation, and conversion to HSDF.
    """

    def __init__(self, name: str = "SDFGraph"):
        self.name = name
        self.actors: Dict[int, Actor] = {}
        self.channels: Dict[int, Channel] = {}
        self._next_actor_id = 0
        self._next_channel_id = 0

    def add_actor(self, name: str, execution_time: float) -> int:
        aid = self._next_actor_id
        self._next_actor_id += 1
        self.actors[aid] = Actor(aid, name, execution_time)
        return aid

    def add_channel(
        self,
        src_id: int,
        dst_id: int,
        initial_tokens: int = 0,
        prd_rate: int = 1,
        cns_rate: int = 1,
    ) -> int:
        if src_id not in self.actors or dst_id not in self.actors:
            raise KeyError("Channel source and destination actors must exist")
        cid = self._next_channel_id
        self._next_channel_id += 1
        self.channels[cid] = Channel(
            cid, src_id, dst_id, initial_tokens, prd_rate=prd_rate, cns_rate=cns_rate
        )
        return cid

    def compute_topology_matrix(self) -> np.ndarray:
        """
        Builds the |E| x |V| topology matrix Gamma.
        Gamma[e, u] = prd(e), Gamma[e, v] = -cns(e)
        """
        n_actors = len(self.actors)
        n_channels = len(self.channels)
        gamma = np.zeros((n_channels, n_actors), dtype=int)

        actor_ids = sorted(self.actors.keys())
        actor_idx = {aid: idx for idx, aid in enumerate(actor_ids)}

        for c_idx, ch in enumerate(self.channels.values()):
            u_idx = actor_idx[ch.src_id]
            v_idx = actor_idx[ch.dst_id]
            gamma[c_idx, u_idx] += ch.prd_rate
            gamma[c_idx, v_idx] -= ch.cns_rate

        return gamma

    def compute_repetition_vector(self) -> Optional[Dict[int, int]]:
        """
        Finds the minimal non-trivial integer repetition vector q such that Gamma * q = 0.
        Returns a dict mapping actor_id -> integer repetitions q[a], or None if inconsistent.
        """
        actor_ids = sorted(self.actors.keys())
        n = len(actor_ids)
        if n == 0:
            return {}
        if len(self.channels) == 0:
            return {aid: 1 for aid in actor_ids}

        # Solve balance equations using rational propagation
        # q(u) * prd(e) = q(v) * cns(e) => q(v) = q(u) * prd(e) / cns(e)
        from fractions import Fraction

        fractions: Dict[int, Fraction] = {actor_ids[0]: Fraction(1, 1)}
        queue = [actor_ids[0]]
        visited = {actor_ids[0]}

        # Build adjacency
        adj: Dict[int, List[Tuple[int, int, int, bool]]] = {aid: [] for aid in actor_ids}
        for ch in self.channels.values():
            adj[ch.src_id].append((ch.dst_id, ch.prd_rate, ch.cns_rate, True))
            adj[ch.dst_id].append((ch.src_id, ch.prd_rate, ch.cns_rate, False))

        while queue:
            curr = queue.pop(0)
            curr_frac = fractions[curr]
            for neighbor, prd, cns, is_forward in adj[curr]:
                if is_forward:
                    # curr is src: q(neighbor) = q(curr) * prd / cns
                    cand_frac = curr_frac * Fraction(prd, cns)
                else:
                    # curr is dst: q(neighbor) = q(curr) * cns / prd
                    cand_frac = curr_frac * Fraction(cns, prd)

                if neighbor in fractions:
                    if fractions[neighbor] != cand_frac:
                        # Inconsistent graph
                        return None
                else:
                    fractions[neighbor] = cand_frac
                    queue.append(neighbor)
                    visited.add(neighbor)

        # Verify all actors were reachable; if disconnected, solve each component
        if len(visited) < n:
            unvisited = set(actor_ids) - visited
            while unvisited:
                start_node = next(iter(unvisited))
                fractions[start_node] = Fraction(1, 1)
                queue = [start_node]
                visited.add(start_node)
                unvisited.remove(start_node)
                while queue:
                    curr = queue.pop(0)
                    curr_frac = fractions[curr]
                    for neighbor, prd, cns, is_forward in adj[curr]:
                        if is_forward:
                            cand_frac = curr_frac * Fraction(prd, cns)
                        else:
                            cand_frac = curr_frac * Fraction(cns, prd)
                        if neighbor in fractions:
                            if fractions[neighbor] != cand_frac:
                                return None
                        else:
                            fractions[neighbor] = cand_frac
                            queue.append(neighbor)
                            visited.add(neighbor)
                            unvisited.discard(neighbor)

        # Scale fractions to coprime integers
        # Least common multiple of denominators
        denominators = [frac.denominator for frac in fractions.values()]
        lcm_denom = 1
        for d in denominators:
            lcm_denom = (lcm_denom * d) // math.gcd(lcm_denom, d)

        int_q = {aid: int(fractions[aid] * lcm_denom) for aid in actor_ids}

        # Divide by greatest common divisor of numerators
        gcd_num = int_q[actor_ids[0]]
        for val in int_q.values():
            gcd_num = math.gcd(gcd_num, val)

        return {aid: val // gcd_num for aid, val in int_q.items()}

    def to_hsdfg(self, preserve_actor_sequentiality: bool = True) -> ExtendedHSDFG:
        """
        Converts this consistent multi-rate SDF graph to an equivalent Extended HSDFG
        by replicating each actor v into q(v) instances and connecting tokens.

        If preserve_actor_sequentiality is True (default), enforces non-reentrant
        sequential execution between consecutive instances of the same actor
        (inst_i -> inst_{i+1} with delay 0, and inst_{q-1} -> inst_0 with delay 1).
        """
        q = self.compute_repetition_vector()
        if q is None:
            raise ValueError("Cannot convert inconsistent SDF graph to HSDFG: no valid repetition vector exists")

        hsdf = ExtendedHSDFG(name=f"{self.name}_HSDF")
        # Instance mapping: (actor_id, instance_idx) -> hsdf_actor_id
        instance_map: Dict[Tuple[int, int], int] = {}

        for aid, actor in self.actors.items():
            rep = q[aid]
            for inst in range(rep):
                name = f"{actor.name}_{inst}"
                h_aid = hsdf.add_actor(name, actor.execution_time)
                instance_map[(aid, inst)] = h_aid

            if preserve_actor_sequentiality and rep > 1:
                for inst in range(rep - 1):
                    hsdf.add_channel(
                        instance_map[(aid, inst)],
                        instance_map[(aid, inst + 1)],
                        initial_tokens=0,
                    )
                hsdf.add_channel(
                    instance_map[(aid, rep - 1)],
                    instance_map[(aid, 0)],
                    initial_tokens=1,
                )

        # Expand channels
        for ch in self.channels.values():
            u, v = ch.src_id, ch.dst_id
            p, c = ch.prd_rate, ch.cns_rate
            d = ch.initial_tokens
            total_tokens = q[u] * p

            for i in range(total_tokens):
                # Token i produced by u at firing:
                prod_firing = i // p
                prod_inst = prod_firing % q[u]
                # Token i + d consumed by v at firing:
                cons_firing = (i + d) // c
                cons_inst = cons_firing % q[v]
                delay = (i + d) // (q[v] * c) - (i // (q[u] * p))

                u_inst_id = instance_map[(u, prod_inst)]
                v_inst_id = instance_map[(v, cons_inst)]
                hsdf.add_channel(u_inst_id, v_inst_id, initial_tokens=max(0, delay))

        return hsdf
