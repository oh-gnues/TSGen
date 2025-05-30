from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import os

@dataclass
class ProjectConfig:
    """Global paths & settings shared by all modules."""
    project_name: str                      # e.g. "caloriecount"

    # root folders
    root_repo: Path = Path(__file__).resolve().parent.parent
    root_experiment: Path = Path("experiment")
    root_results: Path = Path("results")
    smell_guides_dir: Path = Path("smell-guides")

    # tool locations
    evosuite_jar: Path = Path("tools/evosuite-1.2.0.jar")
    tsdetect_jar: Path = Path("tools/TestSmellDetector.jar")

    # JaCoCo locations
    jacoco_agent: Path = Path("tools/lib/jacocoagent.jar").resolve()
    jacoco_cli: Path = Path("tools/lib/jacococli.jar").resolve()

    # LLM
    openai_model: str = "o3"
    temperature: float = 0.2

    # pipeline limits
    max_refactor_rounds: int = 3
    max_compile_retries: int = 3

    # ───── convenience paths ─────
    @property
    def project_dir(self) -> Path:
        return self.root_experiment / self.project_name

    @property
    def result_dir(self) -> Path:
        return self.root_results / self.project_name

    @property
    def generated_test_dir(self) -> Path:
        # EvoSuite writes tests here via -Dbase_dir
        return self.project_dir / "src" / "test" / "java"

    @property
    def refactored_test_dir(self) -> Path:
        return self.result_dir / "refactored_tests"

    @property
    def reports_dir(self) -> Path:
        return self.result_dir / "reports"

    # default classes dir (Maven). Ant/Gradle handled in evo.py
    @property
    def classes_dir(self) -> Path:
        return self.project_dir / "target" / "classes"
    
    @property
    def test_classes_dir(self) -> Path:
        return self.project_dir / "temp" / "test-classes"
    
    @property
    def prod_classes_dir(self) -> Path:
        return self.project_dir / "temp" / "staging"

    # ───── create necessary dirs ─────
    def ensure_dirs(self) -> None:
        for p in (
            self.project_dir,
            self.result_dir,
            self.generated_test_dir,
            self.refactored_test_dir,
            self.reports_dir,
        ):
            p.mkdir(parents=True, exist_ok=True)