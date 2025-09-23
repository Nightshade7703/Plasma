"""
Tests parsing of Plasma syntax.
"""
import json
import pytest
from plasma.compiler import PlasmaParser

@pytest.fixture
def parser():
    """Parser for all test functions."""
    return PlasmaParser()

def pretty_print(dictionary: dict):
    """Prints a dictionary in a more readable way."""
    print(json.dumps(
        dictionary,
        ensure_ascii=False,
        indent=4,
    ))

# Test valid syntax
def test_valid_integer(parser):  # pylint: disable=redefined-outer-name
    """Do integers pass as programs?"""
    code = "42;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'integer_literal'
    assert tree['body']['value'] == 42

def test_valid_string(parser):  # pylint: disable=redefined-outer-name
    """Do strings pass as programs?"""
    code = '"hello";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'string_literal'
    assert tree['body']['value'] == 'hello'

# Test invalid syntax
def test_invalid_integer_non_digit(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect invalid integers?"""
    code = "abc;"
    with pytest.raises(SyntaxError, match=r"Invalid character at position 0: 'a'"):
        parser.parse(code)

def test_invalid_integer_mixed(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect mixed characters?"""
    code = "4a;"
    with pytest.raises(SyntaxError, match=r"Invalid character at position 1: 'a'"):
        parser.parse(code)

def test_invalid_string_unterminated(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect unterminated strings?"""
    code = '"hello'
    with pytest.raises(SyntaxError, match=r"Unterminated string starting at position 0"):
        parser.parse(code)

def test_missing_semicolon(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect missing semicolons?"""
    code = "42"
    with pytest.raises(SyntaxError, match=r"Unexpected end of input. Expected: SEMI"):
        parser.parse(code)
