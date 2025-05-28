from __future__ import annotations

import shutil
from pathlib import Path
import os

from .config import ProjectConfig
from .utils import run_cmd, CommandError


def _detect_build_tool(project_dir: Path) -> str:
    if (project_dir / "build.xml").is_file():
        return "ant"
    if (project_dir / "pom.xml").is_file():
        return "maven"
    if any((project_dir / n).is_file() for n in ("build.gradle", "build.gradle.kts")):
        return "gradle"
    return "maven"

def _copy_refactored_tests(cfg: ProjectConfig) -> None:
    if not cfg.refactored_test_dir.exists():
        return

    dst_root = cfg.generated_test_dir
    for src in cfg.refactored_test_dir.rglob("*.java"):
        rel = src.relative_to(cfg.refactored_test_dir)  # preserve sub‑package path
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

def compile_and_test(cfg: ProjectConfig) -> bool:
    """clean → compile/test, return True if success"""
    _copy_refactored_tests(cfg)
    tool = _detect_build_tool(cfg.project_dir)

    if tool == "ant":
        cmd = ["ant", "-q", "clean", "test"]
    elif tool == "gradle":
        cmd = ["gradle", "-q", "clean", "test"]
    else:
        cmd = ["mvn", "-q", "clean", "test"]

    try:
        run_cmd(cmd, cwd=cfg.project_dir)
        print(f"[Compile] {tool} build OK")
        return True
    except CommandError as e:
        print(f"[Compile] {tool} build FAILED\n", e)
        return False