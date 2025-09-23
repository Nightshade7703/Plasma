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

def test_valid_float(parser):  # pylint: disable=redefined-outer-name
    """Do floats pass as programs?"""
    code = "3.14;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'float_literal'
    assert tree['body']['value'] == 3.14

def test_valid_string_double_quotes(parser):  # pylint: disable=redefined-outer-name
    """Do double-quote strings pass as programs?"""
    code = '"hello";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'string_literal'
    assert tree['body']['value'] == 'hello'

def test_valid_string_single_quotes(parser):  # pylint: disable=redefined-outer-name
    """Do single-quote strings pass as programs?"""
    code = "'hello';"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'string_literal'
    assert tree['body']['value'] == 'hello'

def test_valid_string_with_space(parser):  # pylint: disable=redefined-outer-name
    """Do strings with spaces pass as programs?"""
    code = '"Hello World";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'string_literal'
    assert tree['body']['value'] == 'Hello World'

def test_true_literal(parser):  # pylint: disable=redefined-outer-name
    """Does true; pass as a program?"""
    code = 'true;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'boolean_literal'
    assert tree['body']['value'] is True

def test_false_literal(parser):  # pylint: disable=redefined-outer-name
    """Does false; pass as a program?"""
    code = 'false;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'boolean_literal'
    assert tree['body']['value'] is False

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

def test_invalid_float_multiple_decimal_points(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect invalid floats with multiple decimal points?"""
    code = "3.1.4;"
    with pytest.raises(SyntaxError, match=r"Invalid character at position 3: '.'"):
        parser.parse(code)

def test_invalid_string_unterminated(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect unterminated strings?"""
    code = '"hello'
    with pytest.raises(SyntaxError, match=r"Invalid character at position \d+:"):
        parser.parse(code)

def test_missing_semicolon(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect missing semicolons?"""
    code = "42"
    with pytest.raises(SyntaxError, match=r"Unexpected end of input. Expected: SEMI"):
        parser.parse(code)
