"""
coverage_runner.py - JaCoCo coverage measurement and report generation.

$ python coverage_runner.py --project <project_name> 
$ python coverage_runner.py --project <project_name> --classes com.foo.Bar com.foo.Baz
"""

from __future__ import annotations
from pathlib import Path
import argparse, json, datetime, sys

# Inner modules
from config   import ProjectConfig
from coverage import measure

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run JaCoCo coverage for target classes.")
    ap.add_argument("-p", "--project", required=True,
                    help="experiment/<project> directory name")
    ap.add_argument("-c", "--classes", nargs="*",
                    help="FQCNs to measure (space separated). If omitted, use config.target_classes")
    ap.add_argument("--round-tag", default=None,
                    help="Identifier to append after the resulting folder name(e.g., refactored)")
    return ap.parse_args()

def main() -> None:
    args = parse_args()
    
    cfg = ProjectConfig(project_name=args.project)
    cfg.ensure_dirs()
    
    target_classes = args.classes or getattr(cfg, "target_classes", [])
    if not target_classes:
        sys.exit("No target classes specified. Use --classes or set config.target_classes.")
        
    # Create coverage results directory
    stamp   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    tag     = f"_{args.round_tag}" if args.round_tag else ""
    out_dir = cfg.result_dir / "coverage" / f"{stamp}{tag}"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Coverage for {len(target_classes)} classes → {out_dir}")
    
    summary: dict[str, str] = {}
    for fqcn in target_classes:
        cls_dir       = out_dir / fqcn.replace(".", "_")
        xml           = measure(fqcn, cls_dir, cfg)
        summary[fqcn] = str(Path(xml).resolve().relative_to(cfg.result_dir.resolve()))
        
    # Save summary
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    
    print("Done -- summary.json created")

if __name__ == "__main__":
    main()