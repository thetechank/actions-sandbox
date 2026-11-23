"""The stand-in's probes, shaped like the harness lab's tests/test_sandbox.py: the CLI run the way a
user would, in a temp workspace. The docker ones need a running Docker and the python:3.13-slim image;
./check leaves them out, with one FAIL line, when Docker isn't running."""

import subprocess

import pytest

DOCKER = pytest.mark.docker


def shape(workspace, *args):
    return subprocess.run(["shape", *args], cwd=workspace, capture_output=True, text=True, timeout=60)


def test_without_a_command_it_prints_its_usage(tmp_path):
    done = shape(tmp_path)
    assert (done.returncode, done.stderr) == (2, "usage: shape run COMMAND\n")


@DOCKER
def test_a_command_can_write_inside_the_workspace(tmp_path):
    done = shape(tmp_path, "run", "echo made inside > inside.txt && cat inside.txt")
    assert done.stdout == "made inside\n[exit code 0]\n"
    assert (tmp_path / "inside.txt").read_text() == "made inside\n"


@DOCKER
def test_a_write_outside_the_workspace_is_blocked(tmp_path):
    done = shape(tmp_path, "run", "python3 -c \"open('../outside.txt', 'w').write('escaped')\"")
    # Read-only image, or (a workspace under /tmp) the sandbox's own root-made /tmp: blocked either way.
    assert done.stdout.endswith(("Read-only file system: '../outside.txt'\n[exit code 1]\n",
                                 "Permission denied: '../outside.txt'\n[exit code 1]\n")), done.stdout
    assert not (tmp_path.parent / "outside.txt").exists()


@DOCKER
def test_the_network_is_off(tmp_path):
    done = shape(tmp_path, "run", "python3 -c \"import socket; socket.create_connection(('pypi.org', 443), 5)\"")
    assert done.stdout.endswith("[exit code 1]\n"), done.stdout
    assert "socket.gaierror" in done.stdout or "OSError" in done.stdout, done.stdout
