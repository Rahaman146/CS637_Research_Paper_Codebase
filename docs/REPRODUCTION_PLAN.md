# Reproduction Plan & Contract: Schedule Synthesis for Synchronous Dataflow Models with Lower and Upper Timing Bounds

**Paper:** *Schedule synthesis for synchronous dataflow models with lower and upper timing bounds* (EMSOFT 2025 / ACM TECS)  
**Authors:** Joep van Wanrooij, Twan Basten, Marc Geilen  
**DOI:** [10.1145/3762643](https://doi.org/10.1145/3762643)

---

## 1. Reproduction Mapping Contract

| Paper Requirement | Implementation Component | Validation Method | Evidence |
|---|---|---|---|
| **Formal Model**<br>Extended HSDFG with event-level lower ($C_L$) and upper ($C_U$) bounds | `src/model.py` (`Actor`, `Channel`, `Constraint`, `ExtendedHSDFG`, `SDFGraph`) | Unit tests verifying rate balance, graph consistency, repetition vector computation, and conversion to HSDF | `tests/test_model.py` passing |
| **$(\max, +)$ Semiring**<br>Max-plus algebra operations ($\oplus, \otimes$), Kleene star, Howard's algorithm | `src/maxplus.py` (`MPMatrix`, `maxplus_add`, `maxplus_mult`, `kleene_star`, `maximum_cycle_mean`) | Mathematical property tests (associativity, distributivity, closure, known cycle means) | `tests/test_maxplus.py` passing |
| **State-Space Transformation**<br>Conversion of extended HSDFG to state-space matrices $(A_0, \dots, A_D, M_0^*)$ | `src/state_space.py` (`StateSpaceMatrices`, `transform_extended_hsdfg_to_state_space`) | Verification of intra- and inter-iteration delays, backward upper-bound arc insertion, Kleene star feasibility check | `tests/test_state_space.py` passing |
| **Schedule Synthesis**<br>ASAP makespan optimization, periodic throughput optimization, conflict detection | `src/scheduler.py` (`synthesize_asap_schedule`, `synthesize_periodic_schedule`, `analyze_bound_slack`) | Execution on test cases with known optimal start times and intentionally infeasible graphs | `tests/test_scheduler.py` passing |
| **Independent Verification**<br>Decoupled constraint verifier | `src/validator.py` (`verify_schedule_legality`) | Rigorous verification of all precedence, lower, and upper bounds on all outputs | `tests/test_validator.py` passing |
| **Experimental Benchmarks**<br>Manufacturing case study, DSP streaming pipelines, scalability analysis | `scripts/run_experiments.py`, `docs/EXPERIMENTS.md` | Automated execution across parameter sweeps, logging raw JSON/CSV, generating figures | `results/*.json`, `figures/*.png`, `results/REPRODUCTION_REPORT.md` |
| **Academic Presentation**<br>16-slide PPTX with speaker notes & team contributions | `scripts/generate_presentation.py` | Successful PPTX creation and validation of shape/text/table hierarchy | `presentation/CS637_Project_Presentation.pptx` |
| **Narrated MP4 Video**<br>Slide-by-slide narrated video with 5 equal member parts | `scripts/generate_video.py` | TTS audio generation, slide-audio synchronization, playable MP4 compilation | `presentation/CS637_Project_Presentation.mp4` |

---

## 2. Explicit Acceptance Criteria

1. **Model Correctness:**
   - Both general multi-rate SDF and homogeneous SDF representation must be supported.
   - Conversion from multi-rate SDF to HSDF must strictly preserve total token production and consumption balance.
   - Event types (`START`, `COMPLETION`) must be correctly translated into start-time linear difference inequalities.
2. **Algebraic Rigor:**
   - Max-plus addition $\oplus = \max$ and multiplication $\otimes = +$ must obey semiring axioms.
   - Kleene star $A^*$ must correctly compute all-pairs longest paths on DAGs and detect positive weight cycles.
3. **Scheduling Correctness:**
   - Every synthesized schedule $\mathbf{S}^*$ must satisfy $s_v(k) \ge 0$.
   - For every channel $(u, v)$ with delay $\delta$, $s_v(k) \ge s_u(k - \delta) + w(u)$.
   - For every lower bound, $t_{dst}(k) - t_{src}(k - \delta) \ge L$.
   - For every upper bound, $t_{dst}(k) - t_{src}(k - \delta) \le U$.
   - If an upper bound contradicts a lower bound, the scheduler must explicitly detect infeasibility rather than silently generating invalid timestamps.
4. **Independent Validation:**
   - The validator module `src/validator.py` must be completely decoupled from the synthesis algorithm.
   - 100% of generated valid schedules must pass the validator with zero residual error.
5. **Experimental Reproducibility:**
   - All benchmark experiments must execute from a single documented command:
     `python scripts/run_experiments.py`
   - Generated figures in `figures/` must visually illustrate the difference between greedy/unbounded schedules and synthesized bounded schedules.
6. **Deliverable Completeness:**
   - Presentation slides (`CS637_Project_Presentation.pptx`) must contain complete technical depth, presenter notes, and the verified team contribution breakdown (20% each).
   - Presentation video (`CS637_Project_Presentation.mp4`) must be a valid, playable MP4 with audible speech narration synchronized to each slide.
   - The entire submission package must be bundled into `CS637_Project_Submission.zip`.
