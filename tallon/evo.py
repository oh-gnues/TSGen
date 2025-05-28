from __future__ import annotations
from pathlib import Path
from typing import List

from .config import ProjectConfig
from .utils import run_cmd
from .compiler import _detect_build_tool

# ── EvoSuite가 다루면 안 되는 루트 패키지 ────────────────────────────────
SKIP_ROOTS = {"java", "javax", "jakarta", "sun", "com.sun", "org.junit"}

# ── 컴파일 경로 탐색 ─────────────────────────────────────────────────────
def _ensure_compiled(cfg: ProjectConfig) -> Path:
    tool = _detect_build_tool(cfg.project_dir)

    if tool == "ant":
        run_cmd(["ant", "-q", "clean", "compile"], cwd=cfg.project_dir)
        possible = [
            cfg.project_dir / "build" / "classes",
            cfg.project_dir / "build",
            cfg.project_dir / "temp" / "staging",
        ]
        classes_dir = next((d for d in possible if d.is_dir()),
                           cfg.project_dir / "build" / "classes")
    elif tool == "gradle":
        run_cmd(["gradle", "-q", "clean", "classes"], cwd=cfg.project_dir)
        classes_dir = cfg.project_dir / "build" / "classes" / "java" / "main"
    else:                              # Maven
        run_cmd(["mvn", "-q", "clean", "compile"], cwd=cfg.project_dir)
        classes_dir = cfg.project_dir / "target" / "classes"

    if classes_dir.is_dir():
        return classes_dir.resolve()

    # fallback: 프로젝트 내부 첫 .class 위치
    for cls in cfg.project_dir.rglob("*.class"):
        print(f"[EvoSuite] Fallback classes dir → {cls.parent}")
        return cls.parent.resolve()

    raise FileNotFoundError("No compiled classes found")

# ── 클래스 FQN 목록 생성 ─────────────────────────────────────────────────
def _discover_target_classes(classes_dir: Path) -> List[str]:
    fqns: List[str] = []
    for cls_file in classes_dir.rglob("*.class"):
        if "$" in cls_file.name:                   # 내부/익명 클래스 제외
            continue
        rel = cls_file.relative_to(classes_dir).with_suffix("")
        fqns.append(".".join(rel.parts))
    # JDK·프레임워크 루트 필터
    return [c for c in fqns if c.split(".")[0] not in SKIP_ROOTS]

# ── 메인 엔트리 ──────────────────────────────────────────────────────────
def generate_tests(cfg: ProjectConfig,
                   target_classes: List[str] | None = None) -> None:
    print("[EvoSuite] Starting test generation...")
    cfg.ensure_dirs()

    classes_dir = _ensure_compiled(cfg)
    print(f"[EvoSuite] Using classpath: {classes_dir}")

    # ① 사용자가 -c 로 준 목록 → ② 클래스 디렉터리 자동 탐색
    target_classes = target_classes or _discover_target_classes(classes_dir)
    target_classes = [c for c in target_classes if c.split(".")[0] not in SKIP_ROOTS]
    if not target_classes:
        print("[EvoSuite] No valid project classes; skip.")
        return

    # --- 긴 명령행 분할 + 진행 로그 ---
    MAX_CMD = 8000
    if len(",".join(target_classes)) > MAX_CMD:
        total = len(target_classes)
        print(f"[EvoSuite] {total} classes too long; running one-by-one.")
        for idx, cls in enumerate(target_classes, 1):
            print(f"[EvoSuite]  ›  [{idx}/{total}]  {cls}")
            try:
                generate_tests(cfg, target_classes=[cls])
            except Exception as e:
                print(f"[EvoSuite] WARNING: {cls} skipped ({e})")
        return

    print(f"[EvoSuite] Batch generating {len(target_classes)} classes…")
    cmd = [
        "java", "-jar", str(cfg.evosuite_jar.resolve()),
        "-class", ",".join(target_classes),
        "-projectCP", str(classes_dir),
        # "-generateSuite",
        "-Dtest_dir", str(cfg.generated_test_dir.resolve()),
        "-seed", "42",
        "-Djunit_check=true",
    ]
    run_cmd(cmd, cwd=cfg.project_dir)
    print("[EvoSuite] Done.\n")