from __future__ import annotations

import os
import textwrap
import openai
import shutil
from pathlib import Path
from typing import Dict, List

import re
from collections import Counter

# --- helpers --------------------------------------------------------------- #
def _prettify_smell(name: str) -> str:
    """
    Convert detector‑style names like 'EmptyTest' or 'IgnoredTest' to
    human‑readable 'Empty Test', 'Ignored Test' so that they match
    guide headings.

    Underscores are replaced with spaces and CamelCase is split.
    """
    if " " in name:
        return name.strip()

    # Replace underscores first
    name = name.replace("_", " ")
    # Insert spaces before capital letters (except the first)
    name = re.sub(r"(?<!^)(?=[A-Z])", " ", name)
    return name.strip().title()

from .config import ProjectConfig

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")
openai.api_key = os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an expert Java QA engineer. Your sole task is to refactor generated
    JUnit tests so they remain functionally identical while eliminating code
    smells and improving readability. Always preserve imports, annotations,
    and class names unless renaming is essential to remove a smell (e.g.,
    AnonymousTest).  Preserve the JUnit version already used in the source (do not switch between JUnit 4 and 5).  When replacing literals,
    introduce well‑named constants.  Keep each assertion atomic and add a clear
    message string.  Output strictly valid Java source *only*.
    """
).strip()

PROMPT_TEMPLATE = """<s>[INST]
You are given the entire contents of a Java test class {TEST_CLASS} below.

```java
{TEST_SOURCE}
```

This test code currently exhibits the following test smells detected by static analysis:
{DETECTED_SMELLS}

Below are the Safe‑Fix checklists for the detected smells. 
Apply **every checklist item** that is relevant while preserving functional behaviour and coverage.

{SMELL_GUIDE}

**Output rules**
Return ONLY the final Java source code – no explanation, comments, or markdown fences.
[/INST]"""

def _load_guide(cfg: ProjectConfig) -> str:
    """
    Concatenate all `<smell>.md` files in `cfg.smell_guides_dir` into a single
    Markdown string that is easy to split later.

    * The **first Markdown heading** in each file (e.g. `# Sleepy Test`) is kept
      as the smell’s canonical title but normalised to level‑2 (`##`).
    * Any subsequent level‑2 headings (`## `) inside the same file are demoted
      to level‑3 (`### `) so that our later `re.split(r"\\n(?=## )", ...)`
      correctly treats the entire block as one smell section.
    * If a file lacks a heading, we derive one from the filename.
    """
    parts: list[str] = []

    for md in sorted(cfg.smell_guides_dir.glob("*.md")):
        lines = md.read_text(encoding="utf-8").splitlines()

        # Strip leading blank lines
        while lines and not lines[0].strip():
            lines.pop(0)

        # Determine / insert the primary heading
        if lines and lines[0].startswith("#"):
            heading_text = lines[0].lstrip("#").strip()
            lines[0] = f"## {heading_text}"
        else:
            heading_text = md.stem.replace("_", " ").title()
            lines.insert(0, f"## {heading_text}")

        # Demote internal `## ` headings to `### `
        for i in range(1, len(lines)):
            if lines[i].startswith("## ") and not lines[i].startswith("### "):
                lines[i] = "#" + lines[i]   # "## " → "### "

        parts.append("\n".join(lines))

    return "\n\n".join(parts)

def _select_relevant_guides(all_guides: str, smells: List[str]) -> str:
    """
    Return only the guide sections relevant to `smells`.

    A smell may appear in several naming styles (e.g., "Empty_Test",
    "EmptyTest", "Empty Test").  We normalise by removing spaces/underscores and
    lower‑casing before comparison.
    """
    import re

    def _norm(name: str) -> str:
        return re.sub(r"[\\s_]+", "", name).lower()

    targets = {_norm(s) for s in smells}
    if not targets:
        return ""  # no guide needed

    selected: list[str] = []
    for block in re.split(r"\n(?=## )", all_guides):
        if not block.strip():
            continue
        heading = block.splitlines()[0].lstrip("#").strip()
        if _norm(heading) in targets:
            selected.append(block)

    return "\n\n".join(selected)
            

def refactor_tests(cfg: ProjectConfig, smell_map: Dict[str, List[str]], archive_dir: Path | None = None) -> None:
    guide = _load_guide(cfg)
    for src_file in cfg.generated_test_dir.rglob("*.java"):
        if "scaffolding" in src_file.name.lower():
            continue
        print(f"[LLM] refactoring {src_file.name}...")
            
        raw_smells = smell_map.get(src_file.name, [])

        # Prettify and deduplicate
        pretty_counts = Counter(_prettify_smell(s) for s in raw_smells)
        unique_smells = list(pretty_counts.keys())

        if not unique_smells:
            print("  ↳ No smells detected, skipping.")
            continue

        smells_str = ", ".join(
            f"{s} (x{c})" if pretty_counts[s] > 1 else s
            for s, c in pretty_counts.items()
        )
        
        focused_guide = _select_relevant_guides(guide, unique_smells)
                
        prompt = PROMPT_TEMPLATE.format(
            TEST_CLASS=src_file.name,
            TEST_SOURCE=src_file.read_text(encoding="utf-8"),
            DETECTED_SMELLS=smells_str,
            SMELL_GUIDE=focused_guide,
        )
        
        resp = openai.chat.completions.create(
            model=cfg.openai_model,
            messages=[{"role":"system","content":SYSTEM_PROMPT},
                      {"role":"user","content":prompt}],
            temperature=0.1, max_tokens=8192,
        )
        improved = resp.choices[0].message.content.strip()

        # Preserve original sub‑package folder when saving
        rel_path = src_file.relative_to(cfg.generated_test_dir)
        out_path = cfg.refactored_test_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        out_path.write_text(improved, encoding="utf-8")
        # ----- archive per-round -----
        if archive_dir is not None:
            archive_path = archive_dir / rel_path
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(out_path, archive_path)
            
        print(f"[LLM] saved → {out_path}")