"""
Script to create the clean submission package: CS637_Project_Submission.zip
Includes:
- CS637_Project_Presentation.mp4 (narrated video presentation)
- CS637_Project_Presentation.pptx (academic slides with notes)
- CS637_Project_Presentation.pdf (exported slide deck)
- README.md, PROJECT_STATUS.md, TEST_REPORT.md
- docs/ (PAPER_ANALYSIS.md, REPRODUCTION_PLAN.md, EXPERIMENTS.md)
- src/ (modular implementation of dataflow, semiring, state-space, scheduler, validator)
- tests/ (unit and integration test suite)
- scripts/ (reproducible experiment and build scripts)
- results/ (raw JSON logs and REPRODUCTION_REPORT.md)
- figures/ (publication-quality benchmark charts)
- presentation/ (speaker script, slide timings, slides)
"""

import os
import zipfile

ZIP_NAME = "CS637_Project_Submission.zip"

INCLUDE_FILES = [
    "README.md",
    "PROJECT_STATUS.md",
    "TEST_REPORT.md",
    "requirements.txt",
    "CS637_Project_Presentation.pptx",
    "CS637_Project_Presentation.pdf",
    "CS637_Project_Presentation_Canva_Style.pptx",
    "CS637_Project_Presentation_Canva_Style.pdf",
    "CS637_Project_Presentation.mp4",
]

INCLUDE_DIRS = [
    "docs",
    "src",
    "tests",
    "scripts",
    "results",
    "figures",
    "figures_canva",
    "presentation",
]

EXCLUDE_EXTS = {".pyc", ".log", ".tmp", ".wav"}
EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".git", ".system_generated", "audio", "clips"}


def build_submission_zip():
    print(f"\n--- Creating Final Submission Package: {ZIP_NAME} ---")
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add root individual files
        for fname in INCLUDE_FILES:
            if os.path.exists(fname):
                print(f"Adding file: {fname}")
                zipf.write(fname, arcname=fname)
            else:
                print(f"Warning: Root file not found: {fname}")

        # Add directories recursively
        for dname in INCLUDE_DIRS:
            if not os.path.exists(dname):
                continue
            for root, dirs, files in os.walk(dname):
                # Filter out excluded dirs
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

                for f in files:
                    ext = os.path.splitext(f)[1]
                    if ext in EXCLUDE_EXTS:
                        continue
                    file_path = os.path.join(root, f)
                    rel_path = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname=rel_path)

    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"\nFinal submission archive successfully created: {ZIP_NAME} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    build_submission_zip()
