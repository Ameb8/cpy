import pytest
from user_vars.manage_vars import parse_var_definition

def test_valid_no_parentheses():
    assert parse_var_definition("MY_VAR") == ("MY_VAR", None)

def test_valid_single_param():
    assert parse_var_definition("GREET(name)") == ("GREET", ["name"])

def test_valid_multiple_params_no_spaces():
    assert parse_var_definition("FUNC(a,b,c)") == ("FUNC", ["a", "b", "c"])

def test_valid_multiple_params_with_spaces():
    assert parse_var_definition("FUNC(a, b, c)") == ("FUNC", ["a", "b", "c"])

def test_valid_spaces_inside_param_list():
    assert parse_var_definition("VAR   (  param1 ,  param2   )") == ("VAR", ["param1", "param2"])

def test_valid_trailing_comma_filtered():
    assert parse_var_definition("VAR(p1, p2,)") == ("VAR", ["p1", "p2"])

def test_invalid_non_alphanumeric_key():
    assert parse_var_definition("BAD-VAR") is None

def test_invalid_chars_in_param():
    assert parse_var_definition("VAR(p@ram)") is None

def test_invalid_extra_text_after_parentheses():
    assert parse_var_definition("FUNC(a, b)) more") is None

def test_invalid_incomplete_param_block():
    assert parse_var_definition("FUNC(a, b") is None

def test_invalid_nested_parentheses():
    assert parse_var_definition("FUNC(a, b(1))") is None

def test_invalid_empty_param_list():
    assert parse_var_definition("FUNC()") is None

def test_invalid_key_with_space():
    assert parse_var_definition("BAD VAR") is None

def test_invalid_non_alphanum_param():
    assert parse_var_definition("FUNC(a$, b)") is None