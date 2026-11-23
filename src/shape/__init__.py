"""shape: the harness lab's Docker sandbox in miniature. `shape run COMMAND` runs COMMAND with bash
in a throwaway python:3.13-slim container that sees only the current folder and has no network, the
way the harness's `docker` sandbox runs a model's bash call (harness/build-sandbox.md)."""

import os
import subprocess
import sys
import uuid
from pathlib import Path

IMAGE = "python:3.13-slim"  # the image the harness lab's sandbox uses; CI pulls or loads it


def sandboxed(workspace: Path, command: str) -> list[str]:
    """The docker run argv for one command: removed on exit, no network, the image read-only, only the
    workspace writable (at the same path as on the host), as the calling user."""
    return ["docker", "run", "--rm", "--name", f"shape-{uuid.uuid4().hex[:12]}",
            "--network", "none",
            "--read-only", "--tmpfs", "/tmp",
            "--volume", f"{workspace}:{workspace}",
            "--workdir", str(workspace),
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            IMAGE, "bash", "-c", command]


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "run":
        print("usage: shape run COMMAND", file=sys.stderr)
        return 2
    done = subprocess.run(sandboxed(Path.cwd(), sys.argv[2]), capture_output=True, text=True)
    print(done.stdout + done.stderr, end="")
    print(f"[exit code {done.returncode}]")
    return 0
