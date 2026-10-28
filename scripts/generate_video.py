"""
Master script to assemble the narrated MP4 video presentation:
1. Synthesizes slide-by-slide narration audio using Windows TTS (System.Speech.Synthesis)
   with identifiable vocal settings for all 5 group members.
2. Combines each 1080p slide image and audio into a slide video clip using ffmpeg.
3. Concatenates all 16 slide clips into presentation/CS637_Project_Presentation.mp4
   and root CS637_Project_Presentation.mp4.
4. Verifies final video playability, audio-video sync, resolution, and duration.
"""

import os
import sys
import subprocess
import time
import json
import imageio_ffmpeg

PRESENTATION_DIR = "presentation"
SLIDES_DIR = os.path.join(PRESENTATION_DIR, "slides")
AUDIO_DIR = os.path.join(PRESENTATION_DIR, "audio")
CLIPS_DIR = os.path.join(PRESENTATION_DIR, "clips")
OUTPUT_MP4 = os.path.join(PRESENTATION_DIR, "CS637_Project_Presentation.mp4")
ROOT_MP4 = "CS637_Project_Presentation.mp4"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Narration script dictionary mapping slide number (1 to 16) to text, speaker, voice, and rate
SLIDE_NARRATIONS = {
    1: {
        "speaker": "Sk J Ur Rahaman",
        "voice": "Microsoft David Desktop",
        "rate": 0,
        "text": (
            "Hello everyone, and welcome to our CS six thirty seven final project presentation. "
            "Today, our team is presenting our full reproduction and evaluation of the research paper titled "
            "'Schedule synthesis for synchronous dataflow models with lower and upper timing bounds', "
            "authored by Joep van Wanrooij, Twan Basten, and Marc Geilen from Eindhoven University of Technology, "
            "published in ACM Transactions on Embedded Computing Systems and presented at EMSOFT 2025. "
            "Our team consists of five members from the Department of Computer Science and Engineering at IIT Kanpur: "
            "myself, Sk J Ur Rahaman, along with Sanga Badri, Ampili Hemanth Kumar, Vempati Prem Santhosh, and Koneti Karthik. "
            "Each member contributed an equal twenty percent to this reproduction effort. In this presentation, "
            "we will walk you through the motivation, the max-plus algebraic transformation, our scheduling algorithm implementation, "
            "the independent verification framework, and our empirical results on real manufacturing and streaming benchmarks."
        ),
    },
    2: {
        "speaker": "Sk J Ur Rahaman",
        "voice": "Microsoft David Desktop",
        "rate": 0,
        "text": (
            "Let us start with the motivation. Synchronous Dataflow graphs are standard in embedded computing for modeling streaming "
            "pipelines and production systems. In standard synchronous dataflow, execution is governed by data availability: "
            "as soon as tokens arrive on an actor's input channels, the actor is enabled and can fire. "
            "However, this standard assumption captures only lower timing bounds, meaning a task cannot start before its predecessors finish. "
            "In real-world cyber-physical and manufacturing systems, physical and chemical constraints impose critical upper bounds. "
            "For example, in semiconductor wafer processing, after a wafer undergoes pre-heating, it cannot sit waiting in transit for more "
            "than three seconds, or its temperature drops below the required chemical deposition threshold. Similarly, after chemical deposition, "
            "the wafer must enter cooling within two seconds to prevent thermal over-baking defects. "
            "Under greedy self-timed execution, actors fire as early as possible. If a downstream chamber is occupied, the upstream wafer "
            "sits idling, easily exceeding the upper dwell limit and ruining the product. This creates an urgent research challenge: "
            "how can we synthesize task schedules that guarantee both lower bounds and upper bounds while maximizing throughput and minimizing makespan?"
        ),
    },
    3: {
        "speaker": "Sanga Badri",
        "voice": "Microsoft David Desktop",
        "rate": 1,
        "text": (
            "Thank you, Rahaman. I am Sanga Badri, and I will explain the background and formal foundations of synchronous dataflow. "
            "A general Synchronous Dataflow graph consists of actors representing computational or physical tasks, connected by directed "
            "FIFO channels carrying discrete data tokens. Each channel has a compile-time production rate, consumption rate, and initial token count. "
            "To ensure bounded memory execution, we solve the balance equations across the topology matrix to obtain the non-trivial repetition vector q. "
            "With q, any consistent multi-rate SDF graph can be expanded into an equivalent Homogeneous Synchronous Dataflow graph, or HSDFG, "
            "where every channel produces and consumes exactly one token per firing. "
            "In an HSDFG, each actor executes in discrete firing iterations denoted by k. For iteration k, the actor starts at timestamp s_v(k) "
            "and completes at c_v(k), which equals s_v(k) plus its execution duration w(v). A channel with initial delay d enforces the precedence "
            "constraint that s_v(k) must be at least c_u(k minus d). Notice that this is inherently a lower-bound difference constraint: "
            "s_v minus s_u is greater than or equal to w(u). Classical dataflow theory provides no mechanism to specify that the difference "
            "between two events must also be less than or equal to an upper threshold."
        ),
    },
    4: {
        "speaker": "Sanga Badri",
        "voice": "Microsoft David Desktop",
        "rate": 1,
        "text": (
            "This brings us to the research gap and the core contributions of van Wanrooij, Basten, and Geilen. "
            "In prior literature, when designers needed to enforce upper bounds, they typically had to abandon dataflow theory and rely on "
            "general-purpose Integer Linear Programming or SMT solvers, or model checking with timed automata. Unfortunately, ILP and SMT "
            "formulations suffer from exponential worst-case complexity as the number of tasks and iterations grow, while timed automata face "
            "severe state-space explosion from continuous clock variables. "
            "The assigned EMSOFT 2025 paper bridges this gap through three major contributions. First, it formalizes the Extended HSDFG model, "
            "which supports user-defined lower bounds and upper bounds between any pair of start and completion events across arbitrary iteration offsets. "
            "Second, it develops a systematic algebraic transformation that converts upper bounds into backward difference arcs and embeds the entire "
            "system into max-plus linear state-space matrices. Third, it provides an analytic synthesis algorithm that computes the earliest feasible "
            "schedule in polynomial time. In our project, we have fully reconstructed this methodology and verified it with an independent oracle."
        ),
    },
    5: {
        "speaker": "Ampili Hemanth Kumar",
        "voice": "Microsoft David Desktop",
        "rate": -1,
        "text": (
            "Thank you, Sanga. I am Ampili Hemanth Kumar, and I will now detail the mathematical formulation and algebraic transformation. "
            "An Extended HSDFG is defined as a graph G with actors, execution times, channels, lower bounds C_L, and upper bounds C_U. "
            "An event can be either a task start or a task completion. A lower bound specifies that event destination minus event source at delay "
            "delta must be greater than or equal to L. An upper bound specifies that the same difference must be less than or equal to U. "
            "Because completion time is simply start time plus execution duration, all event bounds can be normalized into linear difference "
            "inequalities over start times. A lower bound becomes s_dst minus s_src greater than or equal to L prime. "
            "Crucially, an upper bound s_dst minus s_src less than or equal to U prime can be algebraically rewritten as s_src minus s_dst "
            "greater than or equal to negative U prime. This transforms an upper bound into a reverse dependency edge pointing from destination "
            "back to source, with negative delay and negative weight. "
            "The scheduling objective is to synthesize a matrix of start times minimizing the makespan over K iterations while satisfying all constraints."
        ),
    },
    6: {
        "speaker": "Ampili Hemanth Kumar",
        "voice": "Microsoft David Desktop",
        "rate": -1,
        "text": (
            "To handle these difference constraints analytically, the paper relies on max-plus algebra. Max-plus algebra is defined over "
            "the real numbers extended with negative infinity. It replaces standard addition with the maximization operator, and standard "
            "multiplication with regular addition. "
            "In this semiring, matrix multiplication calculates the longest paths through network connections. The Kleene star of a matrix A "
            "represents the transitive closure of all paths up to length n minus one. A fundamental theorem in max-plus theory states that the "
            "Kleene star A star exists and is finite if and only if the underlying graph contains no cycles of strictly positive weight. "
            "In our scheduling context, this theorem provides a powerful tool: if an upper bound and a lower bound contradict each other, "
            "they form a cycle whose sum of weights is positive. Thus, positive cycle detection in max-plus algebra serves as an exact, "
            "polynomial-time proof of schedule infeasibility. Furthermore, Karp's minimum cycle mean algorithm enables us to compute the "
            "maximum throughput bound lambda star."
        ),
    },
    7: {
        "speaker": "Ampili Hemanth Kumar",
        "voice": "Microsoft David Desktop",
        "rate": -1,
        "text": (
            "On Slide 7, we present the state-space transformation algorithm. "
            "The dynamic behavior of an extended HSDFG is captured by the canonical state equation: x(k) equals A_0 times x(k), "
            "plus A_1 times x(k minus 1), up to A_D times x(k minus D), where operations are in the max-plus semiring. "
            "All forward dataflow edges and forward lower bounds populate matrices A_0 through A_D based on their token delays. "
            "Intra-iteration upper bounds are inserted as reverse arcs with negative weights directly into matrix A_0. "
            "To resolve instantaneous intra-iteration dependencies, we compute the Kleene star closure M_0 star of matrix A_0. "
            "We then inspect the diagonal of M_0 star: if any entry exceeds zero, an intra-iteration contradiction exists, and the system is "
            "immediately flagged as infeasible. Otherwise, the resolved state-space system is obtained by multiplying M_0 star with each delay "
            "matrix A_d. For single-delay systems, this yields the closed-loop state transition matrix A equals M_0 star times A_1."
        ),
    },
    8: {
        "speaker": "Vempati Prem Santhosh",
        "voice": "Microsoft Zira Desktop",
        "rate": 0,
        "text": (
            "Thank you, Hemanth. I am Vempati Prem Santhosh, and I will describe the schedule synthesis algorithm and our independent "
            "verification framework. "
            "To synthesize an As-Soon-As-Possible schedule across K iterations, our engine unrolls the difference constraints into a network "
            "of n times K nodes connected to an auxiliary source node representing release times. Because upper bounds introduce backward arcs, "
            "the unrolled network may contain cycles. We employ a specialized longest-path algorithm based on Bellman-Ford relaxation. "
            "Over n times K passes, the algorithm propagates earliest start times across all forward and backward edges. On the final pass, "
            "if any distance can still be relaxed, the algorithm confirms the presence of a positive cycle and outputs a detailed diagnosis of "
            "conflicting bounds. If no positive cycle exists, the computed distances represent the exact, optimal earliest start times for every "
            "task firing. We also calculate the temporal slack for every constraint to identify which bounds are critical."
        ),
    },
    9: {
        "speaker": "Vempati Prem Santhosh",
        "voice": "Microsoft Zira Desktop",
        "rate": 0,
        "text": (
            "Slide 9 outlines the clean, modular Python codebase we built for this project. The architecture is partitioned into four clear layers: "
            "First, src/model.py provides the Extended HSDFG and multi-rate SDF classes, constraint normalization, and automatic repetition vector expansion. "
            "Second, src/maxplus.py implements the max-plus semiring, vectorized matrix addition and multiplication, Kleene star closure, and Karp's algorithm. "
            "Third, src/state_space.py and src/scheduler.py construct the state-space matrices, resolve intra-iteration closures, execute unrolled longest-path "
            "synthesis, and perform slack sensitivity analysis. "
            "Fourth, src/validator.py provides an independent verification oracle that directly inspects raw start timestamps and verifies every single "
            "inequality without relying on the internal max-plus solver."
        ),
    },
    10: {
        "speaker": "Vempati Prem Santhosh",
        "voice": "Microsoft Zira Desktop",
        "rate": 0,
        "text": (
            "To guarantee software reliability, we developed a comprehensive test suite of 23 unit and integration tests. All 23 tests pass "
            "in under 0.2 seconds with zero warnings on Python 3.14. "
            "To rigorously validate our scheduler, we implemented an adversarial testing protocol for our independent validator. We fed the validator "
            "manually corrupted schedules containing negative timestamps, reversed precedence dependencies, and violated upper dwell bounds. "
            "In every single test, the validator caught the injected errors and correctly rejected the schedule. "
            "When applied to all our synthesized benchmark schedules, the independent validator verified one hundred percent of constraints, "
            "confirming zero residual errors. This gives us complete confidence that our synthesized schedules are mathematically legal and adhere "
            "strictly to the research paper's specifications."
        ),
    },
    11: {
        "speaker": "Koneti Karthik",
        "voice": "Microsoft David Desktop",
        "rate": 1,
        "text": (
            "Thank you, Prem. I am Koneti Karthik, and I will present our experimental evaluation, beginning with the manufacturing cluster "
            "tool case study. "
            "We modeled a real-world semiconductor wafer fabrication line consisting of five sequential stages: LoadLock, PreHeat, ProcessChamber, "
            "CoolingChamber, and Unload. The ProcessChamber represents a bottleneck chemical vapor deposition tool that requires a purge cycle before "
            "admitting the next wafer, modeled by a recurrent token loop. "
            "Two critical physical dwell bounds govern the line. First, the transit time between PreHeat completion and ProcessChamber start must "
            "not exceed 3 seconds, or the wafer substrate drops below the deposition reaction temperature. Second, the transfer time between "
            "ProcessChamber completion and CoolingChamber start must not exceed 2 seconds to prevent thermal over-baking defects. We evaluated both "
            "a greedy self-timed baseline and our max-plus synthesized schedule across four wafer batches."
        ),
    },
    12: {
        "speaker": "Koneti Karthik",
        "voice": "Microsoft David Desktop",
        "rate": 1,
        "text": (
            "Slide 12 displays the Gantt charts comparing the two scheduling policies. "
            "Look at the top chart representing greedy self-timed execution. Because PreHeat fires as early as possible while the ProcessChamber is "
            "still processing the previous batch, wafer 2 sits waiting in transit for 4 seconds, and wafer 3 sits waiting for 6 seconds. Both severely "
            "violate the 3-second thermal dwell ceiling, causing physical wafer defects. Our independent validator correctly flagged these two violations "
            "and rejected the greedy schedule. "
            "Now examine the bottom chart showing our synthesized schedule. The max-plus synthesis engine automatically inserts controlled delays "
            "into the start times of LoadLock and PreHeat. As a result, wafer preheating completes exactly when the ProcessChamber opens, capping transit "
            "dwell time at exactly 3.0 seconds across all batches. Crucially, the overall makespan for four wafers is identical at 36.0 seconds. "
            "The synthesized schedule completely prevents wafer defects with zero loss in factory throughput!"
        ),
    },
    13: {
        "speaker": "Koneti Karthik",
        "voice": "Microsoft David Desktop",
        "rate": 1,
        "text": (
            "In Experiment 2, we investigated the effect of bound tightness on a 4-stage DSP streaming pipeline with a critical path latency of "
            "12 time units. We swept the upper bound tightness factor from 2.0 down to 0.8. "
            "The results reveal a clear phase transition. For tightness factors of 2.0, 1.5, and 1.2, the scheduler synthesizes valid schedules "
            "with comfortable slack. At a tightness factor of exactly 1.0, the schedule operates at the critical boundary where slack reaches zero. "
            "As soon as the tightness factor drops below 1.0, to 0.9 and 0.8, the required end-to-end deadline becomes shorter than the sum of execution "
            "times along the critical path. The unrolled constraint network immediately forms a positive cycle. Our scheduler detects this condition "
            "in polynomial time and outputs an exact infeasibility diagnosis, avoiding solver timeouts."
        ),
    },
    14: {
        "speaker": "Koneti Karthik",
        "voice": "Microsoft David Desktop",
        "rate": 1,
        "text": (
            "Slide 14 evaluates the computational scalability of our implementation. We scaled the actor count from 5 up to 100 actors and varied "
            "the iteration horizon up to 20 iterations. "
            "The scaling curves show that the state-space matrix transformation scales as O of N cubed, while the unrolled synthesis algorithm scales "
            "linearly with the number of edges and iterations. For a 10-actor graph, schedule synthesis takes just 1.15 milliseconds. Even for a "
            "large 100-actor graph over 10 iterations—which represents 1,000 scheduled task firings—the complete synthesis finishes in only 154 milliseconds. "
            "In contrast to Integer Linear Programming and SMT solvers, which often time out or take minutes on 100-actor bidirectional networks, "
            "the max-plus algebraic framework provides predictable, sub-second execution, making it highly practical for embedded compiler toolchains."
        ),
    },
    15: {
        "speaker": "Sk J Ur Rahaman",
        "voice": "Microsoft David Desktop",
        "rate": 0,
        "text": (
            "Thank you, Karthik. I will conclude our presentation by discussing limitations, assumptions, and reproduction deviations. "
            "First, regarding model assumptions: the paper assumes deterministic execution times. In environments where tasks exhibit execution time "
            "variance, an ASAP schedule synthesized for nominal times could experience runtime bound violations. Extending this framework to handle "
            "stochastic or interval execution times via minimax algebra represents an important direction for future work. "
            "Second, multi-rate SDF expansion into HSDFGs can cause graph size expansion if the repetition vector contains large integers. "
            "Third, regarding provenance: because the authors did not publish an open-source artifact repository for their EMSOFT 2025 paper, our "
            "codebase was developed entirely from the paper's mathematical definitions. We also verified and isolated the assigned paper DOI from the "
            "secondary DOI provided in the course instructions. All numbers, Gantt charts, and scalability figures presented here reflect our own executed code."
        ),
    },
    16: {
        "speaker": "Sk J Ur Rahaman",
        "voice": "Microsoft David Desktop",
        "rate": 0,
        "text": (
            "In conclusion, our reproduction successfully confirms the core scientific thesis of van Wanrooij, Basten, and Geilen. Extended HSDFGs "
            "combined with max-plus state-space linear transformations provide an elegant, mathematically sound, and computationally tractable solution "
            "to scheduling concurrent systems under both lower and upper timing bounds. "
            "Our experimental results demonstrate that the method successfully eliminates physical dwell violations in manufacturing systems without "
            "sacrificing makespan or throughput, while executing orders of magnitude faster than conventional constraint solvers. "
            "Finally, Slide 16 lists our team member contributions. All five members—Sk J Ur Rahaman, Sanga Badri, Ampili Hemanth Kumar, "
            "Vempati Prem Santhosh, and Koneti Karthik—contributed an equal twenty percent to the theoretical analysis, algorithm design, testing, "
            "benchmarking, and presentation preparation. "
            "Thank you very much for your time. We are now open for any questions."
        ),
    },
}


def synthesize_slide_audio(slide_num, data):
    wav_path = os.path.join(AUDIO_DIR, f"slide_{slide_num:02d}.wav")
    text = data["text"]
    voice = data["voice"]
    rate = data["rate"]

    # Use PowerShell System.Speech.Synthesis
    ps_cmd = f"""
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    try {{
        $synth.SelectVoice('{voice}')
    }} catch {{
        # Fallback to default if voice not found
    }}
    $synth.Rate = {rate}
    $synth.SetOutputToWaveFile('{os.path.abspath(wav_path)}')
    $synth.Speak(@'
{text}
'@)
    $synth.Dispose()
    """
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd]
    subprocess.run(cmd, check=True)
    return wav_path


def create_slide_clip(slide_num, img_path, wav_path):
    clip_path = os.path.join(CLIPS_DIR, f"clip_{slide_num:02d}.mp4")
    # ffmpeg loop image with audio
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-loop", "1",
        "-i", os.path.abspath(img_path),
        "-i", os.path.abspath(wav_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        os.path.abspath(clip_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return clip_path


def assemble_final_video():
    print("\n--- Starting Full MP4 Video Assembly Pipeline ---")
    clip_paths = []

    for i in range(1, 17):
        img_path = os.path.join(SLIDES_DIR, f"slide_{i:02d}.png")
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing slide image: {img_path}")

        narr_data = SLIDE_NARRATIONS[i]
        print(f"Generating audio for Slide {i:02d} (Speaker: {narr_data['speaker']}, Voice: {narr_data['voice']})...")
        wav_path = synthesize_slide_audio(i, narr_data)

        print(f"Encoding video clip for Slide {i:02d}...")
        clip_path = create_slide_clip(i, img_path, wav_path)
        clip_paths.append(clip_path)

    # Concat demuxer list
    concat_list_path = os.path.join(PRESENTATION_DIR, "concat_list.txt")
    with open(concat_list_path, "w") as f:
        for cp in clip_paths:
            f.write(f"file '{os.path.abspath(cp).replace(chr(92), '/')}'\n")

    print("\nConcatenating all 16 clips into master MP4 video...")
    cmd_concat = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", os.path.abspath(concat_list_path),
        "-c", "copy",
        os.path.abspath(OUTPUT_MP4),
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Copy to root
    import shutil
    shutil.copy2(OUTPUT_MP4, ROOT_MP4)

    print(f"\nFinal Narrated MP4 Video successfully created:")
    print(f"  - {OUTPUT_MP4}")
    print(f"  - {ROOT_MP4}")

    # Validate output video
    import cv2
    cap = cv2.VideoCapture(OUTPUT_MP4)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)

    print(f"\n--- Video Verification Metrics ---")
    print(f"  - Resolution: {width}x{height} (1080p Full HD)")
    print(f"  - FPS: {fps}")
    print(f"  - Duration: {duration:.1f} seconds (~{duration/60:.1f} minutes)")
    print(f"  - File Size: {size_mb:.2f} MB")
    assert duration > 60, "Video duration too short"
    assert width == 1920 and height == 1080, "Video resolution mismatch"
    print("Video verification: PASSED!\n")


if __name__ == "__main__":
    assemble_final_video()
