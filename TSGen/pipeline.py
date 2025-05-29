from __future__ import annotations
import time
import shutil
from typing import List, Dict

from .config import ProjectConfig
from .evo import generate_tests
from .tsdetect import run_tsdetect, smell_counts_from_csv, get_test_methods_count
from .llm_refactor import refactor_tests, refactor_tests_zeroshot, fix_compile_errors
from .compiler import compile_and_test

# ── utility: pretty‑print smell summary ──────────────────────────────────
def _print_smell_summary(smells: Dict[str, Dict[str, int]], method_counts: Dict[str, int], phase: str) -> None:
    total_smells = sum(sum(c for c in counts.values()) for counts in smells.values())
    total_methods = sum(method_counts.values())
    total_classes = len(method_counts)
    
    print(f"[TSDetect] {phase} - Test classes: {total_classes}, Test methods: {total_methods}, Smells: {total_smells}")
    print("[TSDetect] Method count by class:")
    for class_name, method_count in method_counts.items():
        print(f"    {class_name}: {method_count} methods")
    
    if total_smells > 0:
        print("[TSDetect] Smell list:")
        for counts in smells.values():
            for s, n in counts.items():
                if n > 0:
                    print(f"    {s} × {n}")

# ── 1단계: tsDetect → {testClass: [smell…]} ─────────────────────────────
def detect_smells(cfg: ProjectConfig) -> tuple[Dict[str, Dict[str, int]], Dict[str, int]]:
    """
    Run tsDetect on each test file and return:
        ({TestClassFileName: {smellName: count, ...}, ...}, {TestClassFileName: methodCount, ...})
    """
    smell_map: Dict[str, Dict[str, int]] = {}
    method_counts: Dict[str, int] = {}
    
    for test_file in cfg.generated_test_dir.rglob("*.java"):
        # Skip EvoSuite scaffolding/helper classes
        if "scaffolding" in test_file.name.lower():
            continue
        csv_path = run_tsdetect(cfg, cfg.project_name, test_file)
        counts = smell_counts_from_csv(csv_path)
        methods_count = get_test_methods_count(csv_path)
        
        if counts:
            smell_map[test_file.name] = counts
        method_counts[test_file.name] = methods_count
    
    return smell_map, method_counts

# ── 2단계: 단일 프로젝트 파이프라인 ──────────────────────────────────────
def run_pipeline(project_name: str,
                 target_classes: List[str] | None = None) -> None:
    cfg = ProjectConfig(project_name)
    cfg.ensure_dirs()

    # 1) EvoSuite
    generate_tests(cfg, target_classes=target_classes)
    
    #TODO: --- copy baseline tests ---
    baseline_dir = cfg.result_dir / "baseline_tests"
    if baseline_dir.exists():
        shutil.rmtree(baseline_dir)
    shutil.copytree(cfg.generated_test_dir, baseline_dir)

    # 2) smell detect
    smells, method_counts = detect_smells(cfg)
    
    _print_smell_summary(smells, method_counts, "Detected")

    round_ = 0
    while smells and round_ < cfg.max_refactor_rounds:
        round_ += 1
        print(f"\n===== REFACTOR ROUND {round_} =====")

        # 3) LLM refactor
        # Convert {smell: count} → list[str] for LLM prompt
        llm_smell_map = {
            cls: [s for s, n in counts.items() if n > 0]
            for cls, counts in smells.items()
        }
        
        #TODO: Archive previous round
        round_dir = cfg.result_dir / f"refactor_round_{round_}"
        if round_dir.exists():
            shutil.rmtree(round_dir)
        # refactor_tests(cfg, llm_smell_map, archive_dir=round_dir)
        
        #TODO: Archive zero-shot refactor
        refactor_tests_zeroshot(cfg, archive_dir=round_dir)

        # 4) compile + test with error fixing
        compile_success = False
        for attempt in range(1, cfg.max_compile_retries + 1):
            print(f"[Compile] Attempt {attempt}")
            success, error_output = compile_and_test(cfg)
            
            if success:
                compile_success = True
                break
            elif error_output and attempt < cfg.max_compile_retries:
                # Try to fix compile errors with LLM
                print(f"[Pipeline] Compile failed, asking LLM to fix errors...")
                error_fix_dir = cfg.result_dir / f"error_fix_round_{round_}_attempt_{attempt}"
                fix_compile_errors(cfg, error_output, archive_dir=error_fix_dir)
                time.sleep(2)
            else:
                print(f"[Pipeline] Compile attempt {attempt} failed")
                time.sleep(2)
        
        if not compile_success:
            print("[Pipeline] All compile attempts failed; abort.")
            return

        # 5) re-detect smells
        smells, method_counts = detect_smells(cfg)
        _print_smell_summary(smells, method_counts, "Remaining")

    if smells:
        print("[Pipeline] Max rounds reached – smells remain.")
    else:
        print("[Pipeline] Success – all smells removed!")

# ── CLI ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TSGen test-smell pipeline")
    parser.add_argument("project", help="Project dir name under experiment/")
    parser.add_argument(
        "-c", "--class", dest="classes", action="append",
        help="Fully-qualified target class (repeatable). If omitted, all classes.")
    args = parser.parse_args()
    run_pipeline(project_name=args.project, target_classes=args.classes)