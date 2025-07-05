import os
import re
import tempfile
import platform
from unittest import mock
from cpy.parse_content import (
    preprocess_content,
    handle_command,
    get_output,
)

def test_preprocess_content_replaces_backslashes():
    input_text = "line1\\ line2\\ line3"
    expected_output = "line1\nline2\nline3"
    assert preprocess_content(input_text) == expected_output

def test_handle_command_now_returns_datetime():
    result, error = handle_command("now")
    assert error is None
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", result)

def test_handle_command_upper_with_arg():
    result, error = handle_command("upper:hello")
    assert error is None
    assert result == "HELLO"

def test_handle_command_reverse():
    result, error = handle_command("reverse:abcd")
    assert error is None
    assert result == "dcba"

def test_handle_command_repeat_valid():
    result, error = handle_command("repeat:3,ha")
    assert error is None
    assert result == "hahaha"

def test_handle_command_repeat_invalid():
    result, error = handle_command("repeat:hello")
    assert result is None
    assert error == "Invalid syntax for 'repeat'"

def test_handle_command_env_var(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "value")
    result, error = handle_command("env:TEST_VAR")
    assert error is None
    assert result == "value"

def test_handle_command_env_var_missing():
    result, error = handle_command("env:NON_EXISTENT_VAR")
    assert result is None
    assert error == "Environment variable 'NON_EXISTENT_VAR' not set"

def test_handle_command_file_reads_contents():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("file contents")
        tmp_path = tmp.name
    try:
        result, error = handle_command(f"file:{tmp_path}")
        assert error is None
        assert result == "file contents"
    finally:
        os.remove(tmp_path)

def test_handle_command_unrecognized():
    result, error = handle_command("some_random_command")
    assert result is None
    assert error.startswith("Command not recognized:")

def test_get_output_handles_single_command():
    text = "Today is [[today]]"
    result, errors = get_output(text)
    assert not errors
    assert "Today is " in result
    assert len(result) > len("Today is [[today]]")

def test_get_output_handles_multiple_commands():
    text = "UUID: [[uuid]], Upper: [[upper:foo]]"
    result, errors = get_output(text)
    assert not errors
    assert "UUID: " in result
    assert "Upper: FOO" in result

def test_get_output_handles_missing_command():
    text = "Bad: [[notarealcommand]]"
    result, errors = get_output(text)
    
    assert any("notarealcommand" in err[0] for err in errors)
    assert "[Command not recognized: notarealcommand]" not in result  # error text is not in output (replaced with empty)
