# Schedule Synthesis for Synchronous Dataflow Models with Lower and Upper Timing Bounds

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Conference](https://img.shields.io/badge/EMSOFT-2025-red.svg)](https://esweek.org/)

**CS637: Embedded Systems — Final Research Project & Reproduction**  
**Assigned Paper:** *Schedule synthesis for synchronous dataflow models with lower and upper timing bounds*  
**Authors:** Joep van Wanrooij, Twan Basten, Marc Geilen (Eindhoven University of Technology)  
**Publication:** *ACM Transactions on Embedded Computing Systems* (TECS), Vol. 24, Issue 5s, Article 143 (EMSOFT 2025)  
**DOI:** [10.1145/3762643](https://doi.org/10.1145/3762643)

---

## Team Members & Contributions

- **Sk J Ur Rahaman** (Roll: 230951, `shaikja23@iitk.ac.in`) — 20%
- **Sanga Badri** (Roll: 230911, `sangabadri23@iitk.ac.in`) — 20%
- **Ampili Hemanth Kumar** (Roll: 230128, `hemanthka23@iitk.ac.in`) — 20%
- **Vempati Prem Santhosh** (Roll: 231137, `psanthosh23@iitk.ac.in`) — 20%
- **Koneti Karthik** (Roll: 230568, `konetik23@iitk.ac.in`) — 20%

---

## Overview

Synchronous Dataflow Graphs (SDFGs) and Homogeneous Synchronous Dataflow Graphs (HSDFGs) are widely used for modeling concurrent streaming and manufacturing systems. While classical models enforce precedence (lower-bound timing constraints: a task can only start after predecessor completion), practical industrial systems frequently exhibit **upper-bound timing constraints** (deadlines, maximum dwell or cooling times, freshness guarantees) and **relative timing bounds** between arbitrary starts and completions.

This repository provides a faithful, end-to-end Python reproduction of the method proposed by van Wanrooij, Basten, and Geilen:
1. **Extended HSDFG Representation**: Models multi-rate and homogeneous SDFGs augmented with arbitrary lower and upper timing bounds ($C_L, C_U$) on event pairs $(s_u, c_u) \to (s_v, c_v)$ across intra- and inter-iteration delays.
2. **$(\max, +)$ Linear System Transformation**: Converts extended HSDFGs into state-space matrices $(A_0, A_1, \dots, A_D)$, resolving intra-iteration dependencies via Kleene star closure $A_0^*$, and mapping upper bounds to backward difference constraints.
3. **Schedule Synthesis**:
   - As-Soon-As-Possible (ASAP) schedule synthesis minimizing makespan over finite horizons.
   - Periodic schedule synthesis optimizing throughput $\lambda^*$.
   - Conflict detection and cycle-slack analysis.
4. **Independent Validation**: An independent constraint verifier checking schedule legality without relying on max-plus solver internals.
5. **Experimental Pipeline**: Re-executes the manufacturing system case study, DSP streaming pipelines, and bound-tightness parameter sweeps.
6. **Multimedia Deliverables**: Complete PowerPoint presentation (`CS637_Project_Presentation.pptx`) and narrated presentation video (`CS637_Project_Presentation.mp4`).

---

## Directory Structure

```text
├── PROJECT_STATUS.md            # Initial repository audit and status
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── TEST_REPORT.md               # Unit and integration test verification report
├── docs/
│   ├── PAPER_ANALYSIS.md        # Deep analytical study of the research paper
│   ├── REPRODUCTION_PLAN.md     # Reproduction contract and verification protocol
│   └── EXPERIMENTS.md           # Benchmark descriptions and experimental evaluation
├── src/
│   ├── __init__.py
│   ├── maxplus.py               # Complete (max, +) semiring matrix algebra
│   ├── model.py                 # Extended HSDFG & SDF data structures & converters
│   ├── state_space.py           # State-space matrix transformation engine
│   ├── scheduler.py             # ASAP and periodic schedule synthesis
│   └── validator.py             # Independent schedule & constraint validator
├── tests/
│   ├── test_maxplus.py          # Unit tests for max-plus operations & algorithms
│   ├── test_model.py            # Unit tests for SDF / HSDF representation
│   ├── test_state_space.py      # Unit tests for state-space matrix construction
│   ├── test_scheduler.py        # Unit tests for schedule synthesis & bounds
│   └── test_validator.py        # Integration tests with independent validator
├── scripts/
│   ├── run_experiments.py       # Master script running all reproduction benchmarks
│   ├── generate_presentation.py # Script generating presentation slides
│   ├── generate_video.py        # Script assembling narrated MP4 video
│   └── make_submission.py       # Script packaging CS637_Project_Submission.zip
├── results/
│   ├── REPRODUCTION_REPORT.md   # Final experimental reproduction analysis
│   ├── manufacturing_results.json
│   ├── dsp_pipeline_results.json
│   └── scaling_results.json
├── figures/                     # Publication-quality benchmark and comparison plots
└── presentation/
    ├── CS637_Project_Presentation.pptx
    ├── CS637_Project_Presentation.mp4
    ├── SPEAKER_SCRIPT.md
    └── SLIDE_TIMINGS.md
```

---

## Quickstart

### 1. Installation
```powershell
pip install -r requirements.txt
```

### 2. Run Test Suite
```powershell
pytest -v tests/
```

### 3. Run Experimental Reproduction
```powershell
python scripts/run_experiments.py
```

### 4. Build Presentation & Video
```powershell
python scripts/generate_presentation.py
python scripts/generate_video.py
```

### 5. Package Submission
```powershell
python scripts/make_submission.py
```
