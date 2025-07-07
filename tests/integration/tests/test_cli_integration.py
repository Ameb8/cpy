import subprocess
import pytest
import yaml
import pyperclip
from pathlib import Path
from file_setup.file_setup import setup_temp_structure

def load_test_cases():
    with open(Path(__file__).parent / "test_cases.yaml") as f:
        return yaml.safe_load(f)
    
def run_test_case(case, temp_dir_path = None):
    cwd = temp_dir_path if temp_dir_path else None
    
    return subprocess.run(
        ["python3", "-m", "src.cpy.cpy"] + case["args"],
        capture_output=True,
        text=True,
        cwd=cwd
    )

@pytest.mark.parametrize("case", load_test_cases(), ids=lambda c: c["name"])
def test_cli_clipboard_and_output(case):
    # Clear clipboard before test
    pyperclip.copy("")

    if "file_structure" in case: # Run test with temp file structure
        temp_dir_ctx, temp_dir_path = setup_temp_structure(case["file_structure"])

        with temp_dir_ctx:
            result = run_test_case(case, temp_dir_path)
    else: # Run without file structure
        result = run_test_case(case)

    # DEBUG *********
    print(result.stdout)
    print(result.stderr)
    # END DEBUG *****

    assert result.returncode == case["returncode"]

    # Check stdout/stderr if defined
    if "expected_stdout_contains" in case:
        assert case["expected_stdout_contains"] in result.stdout

    if "expected_stderr_contains" in case:
        assert case["expected_stderr_contains"] in result.stderr

    # Check clipboard contents
    if "expected_clipboard" in case:
        clipboard_contents = pyperclip.paste()
        assert clipboard_contents == case["expected_clipboard"]
