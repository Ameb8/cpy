import subprocess
import os
import pytest
import yaml
import pyperclip
import tempfile
import shutil
import logging
from pathlib import Path
from ..file_setup.file_setup import setup_temp_structure
from .dbm_setup import clean_test_db
from .setup import run_setup
from .cleanup import run_cleanup

logger = logging.getLogger(__name__)

def print_bold(text):
    return f"\033[1m{text}\033[0m"

def load_test_cases():
    test_classes_dir = Path(__file__).parent.parent / "test_cases"
    all_classes = []

    for file in sorted(test_classes_dir.glob("*.yaml")):
        with open(file, "r") as f: # Load test class
            loaded = yaml.safe_load(f)

            if not loaded: # Skip empty files
                continue

            if isinstance(loaded, list): # Load list of classes
                all_classes.extend(loaded)
            else: # Load class
                all_classes.append(loaded)

    return all_classes


def run_step(step, temp_dir_path=None):
    cwd = temp_dir_path if temp_dir_path else None

    # Path to project root
    project_root = str(Path(__file__).resolve().parent.parent.parent.parent)

    pythonpath = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

    return subprocess.run(
        ["python3", "-m", "src.cpy.cpy"] + step["args"],
        capture_output=True,
        text=True,
        cwd=cwd,
        env={
            **os.environ,
            "PYTHONPATH": pythonpath
        }
    )



@pytest.mark.parametrize("case", load_test_cases(), ids=lambda c: c["name"])
def test_cli_multi_step(case):
    if case.get("expected_fail", False): # Test case expected failure
        pytest.xfail(f"Expected failure: {case['name']}")

    if case.get("skip", True): # Skip test case
        return

    pyperclip.copy("")  # Clear clipboard before each test

    temp_dir_path = None
    if case.get("run_in_tmp"):
        temp_dir_path = tempfile.mkdtemp(prefix="testcase-")

    try:
        run_setup(case.get("setup"), temp_dir_path)
        run_steps(case["steps"], temp_dir_path)
    finally:
        run_cleanup(case.get("cleanup"))


def run_steps(steps, temp_dir_path=None):
    for step in steps: # Iterate steps
        result = run_step(step, temp_dir_path)

        step_name = step.get("name", "<unnamed step>")


        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"\n{print_bold(step_name + ':')}:")
            logger.debug(f"\n{print_bold('stdout:')}\n\n{result.stdout}")
            logger.debug(f"\n{print_bold('stderr:')}\n\n{result.stderr}")

        # Check return code
        assert result.returncode == step.get("return_code", 0), (
            f"[{step_name}] Expected return code {step.get('return_code', 0)}, "
            f"got {result.returncode}"
        )

        # Check stdout
        if "expected_stdout" in step:
            assert result.stdout.strip() == step["expected_stdout"], (
                f"[{step_name}] Expected stdout:\n{step['expected_stdout']!r}\n"
                f"Got:\n{result.stdout.strip()!r}"
            )

        # Check stderr
        if "expected_stderr" in step:
            assert result.stderr.strip() == step["expected_stderr"], (
                f"[{step_name}] Expected stderr:\n{step['expected_stderr']!r}\n"
                f"Got:\n{result.stderr.strip()!r}"
            )

        # Check stdout contains
        if "expected_stdout_contains" in step:
            for item in step["expected_stdout_contains"]:
                assert item in result.stdout, (
                    f"[{step_name}] Expected stdout to contain:\n{item!r}\n"
                    f"Got:\n{result.stdout!r}"
                )

        # Check stderr contains
        if "expected_stderr_contains" in step:
            assert step["expected_stderr_contains"] in result.stderr, (
                f"[{step_name}] Expected stderr to contain:\n{step['expected_stderr_contains']!r}\n"
                f"Got:\n{result.stderr!r}"
            )

        # Check clipboard content
        if "expected_clipboard" in step:
            clipboard_contents = pyperclip.paste()
            assert clipboard_contents == step["expected_clipboard"], (
                f"[{step_name}] Expected clipboard:\n{step['expected_clipboard']!r}\n"
                f"Got:\n{clipboard_contents!r}"
            )
