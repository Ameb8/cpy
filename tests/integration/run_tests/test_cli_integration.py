import subprocess
import os
import pytest
import yaml
import pyperclip
from pathlib import Path
from ..file_setup.file_setup import setup_temp_structure
from .dbm_setup import clean_test_db
from .setup import run_setup
from .cleanup import run_cleanup


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

'''
def run_step(step, temp_dir_path=None):
    cwd = temp_dir_path if temp_dir_path else None
    return subprocess.run(
        ["python3", "-m", "src.cpy.cpy"] + step["args"],
        capture_output=True,
        text=True,
        cwd=cwd
    )
'''


def run_step(step, temp_dir_path=None):
    cwd = temp_dir_path if temp_dir_path else None
    project_root = str(Path(__file__).parent.parent.parent)  # Adjust based on your structure

    return subprocess.run(
        ["python3", "-m", "src.cpy.cpy"] + step["args"],
        capture_output=True,
        text=True,
        cwd=cwd,
        env={
            **os.environ,
            "PYTHONPATH": project_root  # Add project root to Python path
        }
    )

def run_test_case(case, temp_dir_path=None):
    try:
        run_setup(case.get("setup"))
        run_steps(case["steps"], temp_dir_path)
    finally:
        run_cleanup(case.get("cleanup"))


@pytest.mark.parametrize("case", load_test_cases(), ids=lambda c: c["name"])
def test_cli_multi_step(case):
    pyperclip.copy("")  # Clear clipboard before each test

    if "file_structure" in case:
        temp_dir_ctx, temp_dir_path = setup_temp_structure(case["file_structure"])
        with temp_dir_ctx:
            run_test_case(case, temp_dir_path)
    else:
        run_test_case(case)


def run_steps(steps, temp_dir_path=None):
    for step in steps: # Iterate steps
        result = run_step(step, temp_dir_path)

        step_name = step.get("name", "<unnamed step>")

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
            assert step["expected_stdout_contains"] in result.stdout, (
                f"[{step_name}] Expected stdout to contain:\n{step['expected_stdout_contains']!r}\n"
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
