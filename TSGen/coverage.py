from pathlib import Path
from utils import run_cmd, CommandError
from config import ProjectConfig
import re
import xml.etree.ElementTree as ET

_RUNWITH_RE = re.compile(r'^\s*@RunWith\s*\(\s*EvoRunner\.class\s*\)\s*$')
_PARAM_RE   = re.compile(r'^\s*@EvoRunnerParameters\([^)]*\)\s*$')

def _toggle_evorunner(fpath: Path, disable: bool) -> None:
    """Toggle EvoRunner annotations in the given Java file."""
    lines = fpath.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for ln in lines:
        if disable:
            if _RUNWITH_RE.match(ln) or _PARAM_RE.match(ln):
                    new_lines.append("// " + ln)
            else:
                new_lines.append(ln)
        else:
            # re-enable: remove leading '//' only if the rest matches pattern
            if ln.lstrip().startswith("//"):
                raw = ln.lstrip()[2:]
                if _RUNWITH_RE.match(raw) or _PARAM_RE.match(raw):
                    new_lines.append(raw)
                    continue
            new_lines.append(ln)
    fpath.write_text("\n".join(new_lines), encoding="utf-8")
    

def _compile_with_ant(cfg: ProjectConfig) -> None:
    """Compile the project using Ant, ensuring test classes are built."""
    print("[Ant] Compile classes ...")
    run_cmd("ant -q clean compile",       cwd=cfg.project_dir)
    run_cmd("ant -q clean compile-tests", cwd=cfg.project_dir)


def measure(class_fqcn: str, work_dir: Path, cfg: ProjectConfig) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    exec_file = (work_dir / "jacoco.exec").resolve()
    
    # 1. Temporarily disable EvoRunner annotations in the test source
    pkg = ".".join(class_fqcn.split(".")[:-1])
    test_src_path = (
        cfg.project_dir / "src" / "test" / "java" / Path(*pkg.split(".")) / f"{class_fqcn.split('.')[-1]}_ESTest.java"
    )
    # _toggle_evorunner(test_src_path, disable=True)
    
    # 2. Make sure classes are compiled
    _compile_with_ant(cfg)
    
    # 3. JaCoCo agent option
    package_pattern = ".".join(class_fqcn.split(".")[:-1]) + ".*"
    agent_opts = (
       f"-javaagent:{cfg.jacoco_agent.resolve()}=destfile={exec_file},"
       f"includes={package_pattern}"
    )

    # 4. Run Test (JUnitCore)
    test_class = f"{pkg}.{class_fqcn.split('.')[-1]}_ESTest"
    proj_lib   = (cfg.project_dir / "lib").resolve().as_posix() + "/*"
    test_dir   = cfg.test_classes_dir.resolve().as_posix()
    proj_dir   = cfg.prod_classes_dir.resolve().as_posix()
    cp         = f"{proj_lib}:{test_dir}:{proj_dir}"

    try:
        run_cmd(
            f"java {agent_opts} -cp {cp} org.junit.runner.JUnitCore {test_class}",
            cwd=cfg.project_dir
        )
    except CommandError as e:
        # JUnit reported test failures (non-zero exit). We log and continue so that
        # JaCoCo data is still processed.
        print(f"[WARN] Tests reported failures; continuing to collect coverage.")

    # 5. Generate JaCoCo report
    cls_path = (proj_dir / Path(*class_fqcn.split('.')[:-1]))
    src_path = (cfg.project_dir / 'src').resolve()
    html_dir = (work_dir / "coverage_html").resolve()
    xml_path = (work_dir / "coverage.xml").resolve()
    run_cmd(
        f"java -jar {cfg.jacoco_cli} "
        f"report {exec_file} "
        f"--classfiles {cls_path} "
        f"--sourcefiles {src_path} "
        f"--html {html_dir} "
        f"--xml {xml_path}",
        cwd=cfg.project_dir
    )
    
    # 6. Parse XML and print coverage for only the target class
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # JaCoCo stores class names with slashes
        class_slash = class_fqcn.replace('.', '/')
        class_node = root.find(f".//class[@name='{class_slash}']")
        
        if class_node is None:
            print(f"[Coverage] WARNING: Class '{class_fqcn}' not found in report XML.")
        else:
            instr = class_node.find("./counter[@type='INSTRUCTION']")
            branch = class_node.find("./counter[@type='BRANCH']")
            
            if instr is not None:
                covered = int(instr.get("covered"))
                missed = int(instr.get("missed"))
                instr_cov = 100 * covered / (covered + missed)
                print(f"[Coverage] {class_fqcn} -- Instructions: {instr_cov:.2f}% "
                      f"({covered}/{covered + missed})")
            
            if branch is not None:
                b_cov = int(branch.get("covered"))
                b_mis = int(branch.get("missed"))
                total_b = b_cov + b_mis
                if total_b > 0:
                    branch_cov = 100 * b_cov / total_b
                    print(f"[Coverage] {class_fqcn} -- Branch:       {branch_cov:.2f}% "
                          f"({b_cov}/{total_b})")
                else:
                    print(f"[Coverage] {class_fqcn} -- Branch:       n/a (no branches)")
    except Exception as e:
        print(f"[Coverage] Failed to parse XML: {e}")
    
    # 7. Re-enable EvoRunner annotations
    _toggle_evorunner(test_src_path, disable=False)
    print(f"Coverage report generated: {xml_path}")
    
    return xml_path