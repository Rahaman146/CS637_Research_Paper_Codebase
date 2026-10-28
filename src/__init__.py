"""
Schedule synthesis for synchronous dataflow models with lower and upper timing bounds.
Reproduction of EMSOFT 2025 paper by Joep van Wanrooij, Twan Basten, and Marc Geilen.
"""

from .maxplus import (
    EPSILON,
    mp_add,
    mp_mult,
    mp_identity,
    mp_zero,
    kleene_star,
    maximum_cycle_mean,
    MPMatrix,
)
from .model import (
    EventType,
    BoundType,
    Actor,
    Channel,
    TimingConstraint,
    ExtendedHSDFG,
    SDFGraph,
)
from .state_space import (
    StateSpaceMatrices,
    transform_extended_hsdfg_to_state_space,
)
from .scheduler import (
    synthesize_asap_schedule,
    synthesize_periodic_schedule,
    analyze_bound_slack,
    ScheduleResult,
)
from .validator import (
    IndependentValidator,
    ValidationResult,
    verify_schedule_legality,
)

__all__ = [
    "EPSILON",
    "mp_add",
    "mp_mult",
    "mp_identity",
    "mp_zero",
    "kleene_star",
    "maximum_cycle_mean",
    "MPMatrix",
    "EventType",
    "BoundType",
    "Actor",
    "Channel",
    "TimingConstraint",
    "ExtendedHSDFG",
    "SDFGraph",
    "StateSpaceMatrices",
    "transform_extended_hsdfg_to_state_space",
    "synthesize_asap_schedule",
    "synthesize_periodic_schedule",
    "analyze_bound_slack",
    "ScheduleResult",
    "IndependentValidator",
    "ValidationResult",
    "verify_schedule_legality",
]
