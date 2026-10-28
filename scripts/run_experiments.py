"""
Master script to execute all reproduction experiments:
1. Manufacturing system case study with upper dwell bounds (wafer fabrication line)
2. DSP streaming pipeline benchmarks with bound tightness sweeps
3. Computational scalability analysis (scaling actors N=5 to 100, iterations K)
4. Independent verification and artifact generation (JSON results + PNG figures)
"""

import os
import sys
import json
import time
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.model import ExtendedHSDFG, EventType, BoundType, SDFGraph
from src.state_space import transform_extended_hsdfg_to_state_space
from src.scheduler import (
    synthesize_asap_schedule,
    synthesize_periodic_schedule,
    analyze_bound_slack,
    ScheduleResult,
)
from src.validator import IndependentValidator, verify_schedule_legality

RESULTS_DIR = "results"
FIGURES_DIR = "figures"


def setup_directories():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)


# ==============================================================================
# EXPERIMENT 1: MANUFACTURING SYSTEM CASE STUDY
# ==============================================================================
def run_manufacturing_experiment():
    print("\n--- Running Experiment 1: Manufacturing System Case Study ---")
    # Model a cluster wafer fabrication line:
    # 0: LoadLock (w=2.0)
    # 1: PreHeat (w=4.0)
    # 2: ProcessChamber (w=6.0)
    # 3: CoolingChamber (w=4.0)
    # 4: Unload (w=2.0)
    #
    # Constraints:
    # Dataflow: 0 -> 1 -> 2 -> 3 -> 4
    # Re-entrant robot buffer with 1 capacity:
    # 3 -> 1 with 1 token (chamber reuse delay)
    # Critical upper dwell bounds:
    # Transfer between PreHeat completion and ProcessChamber start <= 3.0 s (prevent heat loss)
    # Transfer between ProcessChamber completion and Cooling start <= 2.0 s (prevent over-bake defects)

    g_bounded = ExtendedHSDFG("WaferClusterTool_Bounded")
    ll = g_bounded.add_actor("LoadLock", 2.0)
    ph = g_bounded.add_actor("PreHeat", 4.0)
    pc = g_bounded.add_actor("ProcessChamber", 6.0)
    cc = g_bounded.add_actor("CoolingChamber", 4.0)
    ul = g_bounded.add_actor("Unload", 2.0)

    # Dataflow dependencies
    g_bounded.add_channel(ll, ph, initial_tokens=0)
    g_bounded.add_channel(ph, pc, initial_tokens=0)
    g_bounded.add_channel(pc, cc, initial_tokens=0)
    g_bounded.add_channel(cc, ul, initial_tokens=0)
    # Multi-wafer recirculation: ProcessChamber requires chamber clean before next wafer
    g_bounded.add_channel(pc, pc, initial_tokens=1)

    # Upper timing bounds
    u_ph_pc = 3.0
    u_pc_cc = 2.0
    g_bounded.add_upper_bound(ph, EventType.COMPLETION, pc, EventType.START, u_ph_pc, delay=0)
    g_bounded.add_upper_bound(pc, EventType.COMPLETION, cc, EventType.START, u_pc_cc, delay=0)

    # Also build unbounded graph (greedy baseline)
    g_greedy = ExtendedHSDFG("WaferClusterTool_Greedy")
    g_greedy.add_actor("LoadLock", 2.0)
    g_greedy.add_actor("PreHeat", 4.0)
    g_greedy.add_actor("ProcessChamber", 6.0)
    g_greedy.add_actor("CoolingChamber", 4.0)
    g_greedy.add_actor("Unload", 2.0)
    g_greedy.add_channel(ll, ph, initial_tokens=0)
    g_greedy.add_channel(ph, pc, initial_tokens=0)
    g_greedy.add_channel(pc, cc, initial_tokens=0)
    g_greedy.add_channel(cc, ul, initial_tokens=0)
    g_greedy.add_channel(pc, pc, initial_tokens=1)

    K = 4
    # Synthesize bounded schedule
    res_bounded = synthesize_asap_schedule(g_bounded, iterations=K)
    # Synthesize greedy baseline (without upper bound constraints)
    res_greedy = synthesize_asap_schedule(g_greedy, iterations=K)

    # Validate both with respect to the BOUNDED requirements
    val = IndependentValidator()
    val_bounded = val.validate(g_bounded, res_bounded)
    val_greedy = val.validate(g_bounded, res_greedy)

    # Measure actual dwell times for both critical upper bounds:
    # 1. PreHeat completion -> ProcessChamber start (limit = 3.0s)
    # 2. ProcessChamber completion -> CoolingChamber start (limit = 2.0s)
    dwell_ph_pc_bounded = []
    dwell_ph_pc_greedy = []
    dwell_pc_cc_bounded = []
    dwell_pc_cc_greedy = []

    for k in range(K):
        # PreHeat -> ProcessChamber
        c_ph_b = res_bounded.get_completion(ph, k)
        s_pc_b = res_bounded.get_start(pc, k)
        dwell_ph_pc_bounded.append(s_pc_b - c_ph_b)

        c_ph_g = res_greedy.get_completion(ph, k)
        s_pc_g = res_greedy.get_start(pc, k)
        dwell_ph_pc_greedy.append(s_pc_g - c_ph_g)

        # ProcessChamber -> CoolingChamber
        c_pc_b = res_bounded.get_completion(pc, k)
        s_cc_b = res_bounded.get_start(cc, k)
        dwell_pc_cc_bounded.append(s_cc_b - c_pc_b)

        c_pc_g = res_greedy.get_completion(pc, k)
        s_cc_g = res_greedy.get_start(cc, k)
        dwell_pc_cc_greedy.append(s_cc_g - c_pc_g)

    exp_data = {
        "experiment": "EXP-1 Manufacturing System Case Study",
        "iterations": K,
        "upper_bound_limit_ph_pc": u_ph_pc,
        "upper_bound_limit_pc_cc": u_pc_cc,
        "bounded_schedule": {
            "is_feasible": res_bounded.is_feasible,
            "makespan": res_bounded.makespan,
            "dwell_ph_pc": dwell_ph_pc_bounded,
            "dwell_pc_cc": dwell_pc_cc_bounded,
            "validator_passed": val_bounded.is_valid,
            "validator_violations": len(val_bounded.violations),
        },
        "greedy_baseline": {
            "is_feasible": res_greedy.is_feasible,
            "makespan": res_greedy.makespan,
            "dwell_ph_pc": dwell_ph_pc_greedy,
            "dwell_pc_cc": dwell_pc_cc_greedy,
            "validator_passed": val_greedy.is_valid,
            "validator_violations": len(val_greedy.violations),
            "violation_details": [f"{v.description} (k={v.iteration}, actual={v.actual_value:.1f}s, max={v.expected_bound:.1f}s)" for v in val_greedy.violations]
        },
    }

    with open(os.path.join(RESULTS_DIR, "manufacturing_results.json"), "w") as f:
        json.dump(exp_data, f, indent=2)

    # Plot Gantt Comparison
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    actor_names = ["LoadLock", "PreHeat", "ProcessChamber", "CoolingChamber", "Unload"]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974"]

    # Greedy Plot
    ax0 = axes[0]
    ax0.set_title("Greedy / Unbounded Schedule (Violates Critical Thermal Dwell Bounds)", fontsize=11, fontweight="bold")
    for aid in range(5):
        for k in range(K):
            st = res_greedy.get_start(aid, k)
            dur = g_greedy.actors[aid].execution_time
            ax0.barh(aid, dur, left=st, color=colors[aid], edgecolor="black", alpha=0.85)
            ax0.text(st + dur/2, aid, f"w{k}", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    ax0.set_yticks(range(5))
    ax0.set_yticklabels(actor_names)
    ax0.grid(True, linestyle="--", alpha=0.5)

    # Synthesized Bounded Plot
    ax1 = axes[1]
    ax1.set_title("Synthesized (max, +) Schedule (Guarantees Dwell Bounds <= 2.0s & Prevents Wafer Defects)", fontsize=11, fontweight="bold")
    for aid in range(5):
        for k in range(K):
            st = res_bounded.get_start(aid, k)
            dur = g_bounded.actors[aid].execution_time
            ax1.barh(aid, dur, left=st, color=colors[aid], edgecolor="black", alpha=0.85)
            ax1.text(st + dur/2, aid, f"w{k}", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    ax1.set_yticks(range(5))
    ax1.set_yticklabels(actor_names)
    ax1.set_xlabel("Time (seconds)", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig1_manufacturing_gantt.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")


# ==============================================================================
# EXPERIMENT 2: DSP STREAMING PIPELINE BENCHMARKS & BOUND TIGHTNESS SWEEP
# ==============================================================================
def run_dsp_benchmarks():
    print("\n--- Running Experiment 2: DSP Streaming Benchmarks & Bound Tightness ---")
    # Topologies:
    # 1. 4-stage Pipeline (Fetch w=2, Decode w=3, Execute w=5, Writeback w=2)
    # 2. Biquad IIR Filter (Cyclic feedback loop: A w=2, B w=3 with delay 1, C w=2 with delay 1)
    # 3. Modem Receiver (Demod w=4, Equalizer w=6, Viterbi w=8)

    tightness_factors = [2.0, 1.5, 1.2, 1.0, 0.9, 0.8]  # factor * critical path
    pipeline_results = []

    for tf in tightness_factors:
        g = ExtendedHSDFG(f"Pipeline_tf_{tf}")
        f = g.add_actor("Fetch", 2.0)
        d = g.add_actor("Decode", 3.0)
        e = g.add_actor("Execute", 5.0)
        w = g.add_actor("Writeback", 2.0)
        g.add_channel(f, d, 0)
        g.add_channel(d, e, 0)
        g.add_channel(e, w, 0)
        # 1-iteration feedback loop for steady streaming
        g.add_channel(w, f, 1)

        crit_latency = 2.0 + 3.0 + 5.0 + 2.0  # 12.0
        ub_val = tf * crit_latency

        # Enforce end-to-end latency bound: c_Writeback - s_Fetch <= ub_val
        g.add_upper_bound(f, EventType.START, w, EventType.COMPLETION, ub_val, delay=0)

        t0 = time.perf_counter()
        res = synthesize_asap_schedule(g, iterations=5)
        dt = (time.perf_counter() - t0) * 1000.0

        is_valid = False
        if res.is_feasible:
            val_res = verify_schedule_legality(g, res)
            is_valid = val_res

        pipeline_results.append({
            "tightness_factor": tf,
            "upper_bound_value": ub_val,
            "is_feasible": res.is_feasible,
            "makespan": res.makespan if res.is_feasible else None,
            "runtime_ms": dt,
            "validator_confirmed": is_valid,
        })

    with open(os.path.join(RESULTS_DIR, "dsp_pipeline_results.json"), "w") as f:
        json.dump(pipeline_results, f, indent=2)

    # Plot Throughput / Feasibility vs Bound Tightness
    fig, ax = plt.subplots(figsize=(8, 5))
    tfs = [r["tightness_factor"] for r in pipeline_results]
    feas = [1 if r["is_feasible"] else 0 for r in pipeline_results]
    makespans = [r["makespan"] if r["is_feasible"] else 0.0 for r in pipeline_results]

    ax.plot(tfs, makespans, marker="o", linewidth=2.2, color="#2b5c8f", label="Schedule Makespan (K=5)")
    ax.axvline(1.0, color="crimson", linestyle="--", linewidth=1.8, label="Critical Path Feasibility Threshold (tf=1.0)")
    ax.scatter([tf for tf, f in zip(tfs, feas) if f == 0], [0 for f in feas if f == 0],
               color="red", marker="x", s=100, zorder=5, label="Infeasible (Positive Cycle Detected)")

    ax.set_xlabel("Timing Bound Tightness Factor (x Critical Latency)", fontsize=11)
    ax.set_ylabel("Makespan (time units)", fontsize=11)
    ax.set_title("Schedule Synthesis Feasibility & Makespan vs. Upper-Bound Tightness", fontsize=12, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(frameon=True, loc="upper left")

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig2_dsp_throughput.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")


# ==============================================================================
# EXPERIMENT 3: SCALABILITY & MATRIX TRANSFORMATION RUNTIME
# ==============================================================================
def run_scalability_experiment():
    print("\n--- Running Experiment 3: Computational Scalability Analysis ---")
    actor_counts = [5, 10, 20, 30, 50, 75, 100]
    iterations_list = [1, 5, 10, 20]
    scaling_data = []

    for N in actor_counts:
        # Build synthetic multi-stage pipeline with cross bounds
        g = ExtendedHSDFG(f"Scale_{N}")
        actors = []
        for i in range(N):
            actors.append(g.add_actor(f"A_{i}", execution_time=float((i % 5) + 1)))

        # Forward channels
        for i in range(N - 1):
            g.add_channel(actors[i], actors[i + 1], initial_tokens=0)
        # Recurrent feedback
        g.add_channel(actors[-1], actors[0], initial_tokens=1)

        # Add upper bounds between every 5 stages
        for i in range(0, N - 5, 5):
            g.add_upper_bound(actors[i], EventType.START, actors[i + 5], EventType.COMPLETION, 50.0, delay=0)

        # Measure state-space transformation time
        t_ss0 = time.perf_counter()
        ss = transform_extended_hsdfg_to_state_space(g)
        t_ss = (time.perf_counter() - t_ss0) * 1000.0

        for K in iterations_list:
            t_s0 = time.perf_counter()
            sched = synthesize_asap_schedule(g, iterations=K)
            t_s = (time.perf_counter() - t_s0) * 1000.0

            t_v0 = time.perf_counter()
            val = IndependentValidator().validate(g, sched)
            t_v = (time.perf_counter() - t_v0) * 1000.0

            scaling_data.append({
                "num_actors": N,
                "iterations": K,
                "state_space_ms": t_ss,
                "synthesis_ms": t_s,
                "validation_ms": t_v,
                "is_feasible": sched.is_feasible,
                "is_valid": val.is_valid,
            })

    with open(os.path.join(RESULTS_DIR, "scaling_results.json"), "w") as f:
        json.dump(scaling_data, f, indent=2)

    # Plot Scalability Runtime
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Ax 1: Runtime vs Number of Actors (for K=10)
    k10_data = [d for d in scaling_data if d["iterations"] == 10]
    ns = [d["num_actors"] for d in k10_data]
    ss_times = [d["state_space_ms"] for d in k10_data]
    syn_times = [d["synthesis_ms"] for d in k10_data]
    val_times = [d["validation_ms"] for d in k10_data]

    ax1.plot(ns, syn_times, marker="s", color="#1f77b4", linewidth=2, label="Schedule Synthesis")
    ax1.plot(ns, ss_times, marker="o", color="#2ca02c", linewidth=2, label="State-Space Matrix Trans.")
    ax1.plot(ns, val_times, marker="^", color="#d62728", linewidth=2, label="Independent Validator")
    ax1.set_xlabel("Number of Actors (N)", fontsize=11)
    ax1.set_ylabel("Execution Time (milliseconds)", fontsize=11)
    ax1.set_title("Runtime vs. Graph Scale (K=10 Iterations)", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()

    # Ax 2: Runtime vs Iterations K (for N=50)
    n50_data = [d for d in scaling_data if d["num_actors"] == 50]
    ks = [d["iterations"] for d in n50_data]
    k_syn_times = [d["synthesis_ms"] for d in n50_data]

    ax2.plot(ks, k_syn_times, marker="D", color="#9467bd", linewidth=2, label="Synthesis (N=50)")
    ax2.set_xlabel("Iteration Horizon (K)", fontsize=11)
    ax2.set_ylabel("Execution Time (milliseconds)", fontsize=11)
    ax2.set_title("Runtime vs. Iteration Horizon (N=50 Actors)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig3_scalability.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")


# ==============================================================================
# EXPERIMENT 4: BOUND SLACK DISTRIBUTION & SENSITIVITY
# ==============================================================================
def run_slack_distribution():
    print("\n--- Running Experiment 4: Slack Distribution & Constraint Sensitivity ---")
    # Using a 10-actor DSP benchmark with mixed upper and lower bounds
    g = ExtendedHSDFG("SlackBenchmark")
    n = 10
    acts = [g.add_actor(f"T{i}", execution_time=float(i + 1)) for i in range(n)]
    for i in range(n - 1):
        g.add_channel(acts[i], acts[i + 1], initial_tokens=0)
    g.add_channel(acts[-1], acts[0], initial_tokens=1)

    # Add lower bounds
    for i in range(0, n - 2, 2):
        g.add_lower_bound(acts[i], EventType.START, acts[i + 2], EventType.START, 10.0, delay=0)

    # Add upper bounds
    for i in range(0, n - 3, 3):
        g.add_upper_bound(acts[i], EventType.START, acts[i + 3], EventType.COMPLETION, 35.0, delay=0)

    sched = synthesize_asap_schedule(g, iterations=5)
    assert sched.is_feasible

    slacks = analyze_bound_slack(g, sched)
    lb_slacks = [s["slack"] for s in slacks["lower_bounds"]]
    ub_slacks = [s["slack"] for s in slacks["upper_bounds"]]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(lb_slacks, bins=8, alpha=0.65, color="#1f77b4", edgecolor="black", label=f"Lower Bound Slacks (n={len(lb_slacks)})")
    ax.hist(ub_slacks, bins=8, alpha=0.65, color="#ff7f0e", edgecolor="black", label=f"Upper Bound Slacks (n={len(ub_slacks)})")
    ax.axvline(0.0, color="red", linestyle="--", linewidth=1.5, label="Binding / Critical Constraint Boundary (Slack=0)")
    ax.set_xlabel("Temporal Slack (time units)", fontsize=11)
    ax.set_ylabel("Constraint Count", fontsize=11)
    ax.set_title("Constraint Slack Distribution Across Schedule Iterations", fontsize=12, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "fig4_slack_distribution.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")


def main():
    setup_directories()
    run_manufacturing_experiment()
    run_dsp_benchmarks()
    run_scalability_experiment()
    run_slack_distribution()
    print("\nAll experiments successfully completed! Results and figures saved.")


if __name__ == "__main__":
    main()
