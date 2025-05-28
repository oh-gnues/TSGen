from __future__ import annotations
import csv, tempfile
from pathlib import Path
from typing import Dict, List
from .config import ProjectConfig
from .utils import run_cmd

META = {"App","TestClass","TestFilePath","ProductionFilePath",
        "RelativeTestFilePath","RelativeProductionFilePath","NumberOfMethods"}

def _infer_production_file(cfg: ProjectConfig, test_file: Path) -> Path | None:
    """
    Infer the source (.java) file for a given EvoSuite *_ESTest.java.
    Example:
      experiment/<proj>/src/test/java/com/foo/Bar_ESTest.java
      -> experiment/<proj>/src/com/foo/Bar.java
    Returns Path or None if inference fails.
    """
    try:
        rel = test_file.relative_to(cfg.project_dir)
    except ValueError:
        return None

    parts = rel.parts
    # Expect: src/test/java/...
    if len(parts) < 4 or parts[1] != "test" or parts[2] != "java":
        return None

    source_subpath = Path(*parts[3:])               # com/foo/Bar_ESTest.java
    # Remove _ESTest suffix
    if not source_subpath.name.endswith("_ESTest.java"):
        return None
    prod_name = source_subpath.name.replace("_ESTest.java", ".java")
    prod_path = cfg.project_dir / "src" / source_subpath.with_name(prod_name)
    return prod_path if prod_path.is_file() else None

def run_tsdetect(cfg: ProjectConfig, project: str, test_file: Path,
                 production_file: Path | None = None) -> Path:
    """Run tsDetect (numerical mode) on a single test file → return output CSV path"""
    if production_file is None:
        production_file = _infer_production_file(cfg, test_file)
    # Create a temporary CSV list for tsDetect
    fd, tmp_path = tempfile.mkstemp(suffix=".csv", text=True)
    list_csv = Path(tmp_path)
    with open(fd, "w", newline="") as tf:
        csv.writer(tf).writerow(
            [project, str(test_file.resolve()),
             str(production_file.resolve()) if production_file else ""]
        )

    out_csv = cfg.result_dir / f"{test_file.stem}_smells.csv"
    cmd = ["java", "-jar", str(cfg.tsdetect_jar.resolve()),
           "-f", str(list_csv), "-g", "numerical", "-o", str(out_csv)]
    run_cmd(cmd)
    list_csv.unlink(missing_ok=True)
    return out_csv

def smell_counts_from_csv(path: Path) -> Dict[str, int]:
    with path.open(newline="") as f:
        row = next(csv.DictReader(f))
    return {k:int(v) for k,v in row.items() if k not in META}

def get_test_methods_count(path: Path) -> int:
    """Extract NumberOfMethods from tsDetect CSV output"""
    with path.open(newline="") as f:
        row = next(csv.DictReader(f))
    return int(row.get("NumberOfMethods", 0))