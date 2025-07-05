import os
import re
import tempfile
import platform
from unittest import mock
from cpy.parse_content import (
    preprocess_content,
    handle_input,
    get_output,
)

def test_preprocess_content_replaces_backslashes():
    input_text = "line1\\ line2\\ line3"
    expected_output = "line1\nline2\nline3"
    assert preprocess_content(input_text) == expected_output

def test_handle_input_now_returns_datetime():
    result, error = handle_input("now")
    assert error is None
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", result)

def test_handle_input_upper_with_arg():
    result, error = handle_input("upper:hello")
    assert error is None
    assert result == "HELLO"

def test_handle_input_reverse():
    result, error = handle_input("reverse:abcd")
    assert error is None
    assert result == "dcba"

def test_handle_input_repeat_valid():
    result, error = handle_input("repeat:3,ha")
    assert error is None
    assert result == "hahaha"

def test_handle_input_repeat_invalid():
    result, error = handle_input("repeat:hello")
    assert result is None
    assert error == "Invalid syntax for 'repeat'"

def test_handle_input_env_var(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "value")
    result, error = handle_input("env:TEST_VAR")
    assert error is None
    assert result == "value"

def test_handle_input_env_var_missing():
    result, error = handle_input("env:NON_EXISTENT_VAR")
    assert result is None
    assert error == "Environment variable 'NON_EXISTENT_VAR' not set"

def test_handle_input_unrecognized():
    result, error = handle_input("some_random_command")
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
