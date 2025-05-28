from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence


class CommandError(RuntimeError):
    pass


def run_cmd(cmd: Sequence[str] | str, cwd: Path | None = None, env=None) -> str:
    proc = subprocess.run(
        cmd, cwd=cwd, env=env, shell=isinstance(cmd, str),
        text=True, capture_output=True
    )
    if proc.returncode != 0:
        raise CommandError(
            f"Command failed (exit {proc.returncode}): {cmd}\n"
            f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout