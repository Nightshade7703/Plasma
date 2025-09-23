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

def test_valid_negative_integer(parser):  # pylint: disable=redefined-outer-name
    """Do negative integers pass as programs?"""
    code = "-42;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'integer_literal'
    assert tree['body']['value'] == -42

def test_valid_float(parser):  # pylint: disable=redefined-outer-name
    """Do floats pass as programs?"""
    code = "3.14;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'float_literal'
    assert tree['body']['value'] == 3.14

def test_valid_negative_float(parser):  # pylint: disable=redefined-outer-name
    """Do floats pass as programs?"""
    code = "-3.14;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'float_literal'
    assert tree['body']['value'] == -3.14

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

def test_valid_string_with_escaped_apostrophy(parser):  # pylint: disable=redefined-outer-name
    """Do strings with escaped characters pass as programs?"""
    code = "'How\\'s it going?';"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'string_literal'
    assert tree['body']['value'] == 'How\'s it going?'

def test_valid_string_with_escaped_newline(parser):  # pylint: disable=redefined-outer-name
    """Do strings with escaped characters pass as programs?"""
    code = '"Hello\\nWorld";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'string_literal'
    assert tree['body']['value'] == 'Hello\nWorld'

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

def test_valid_identifier(parser):  # pylint: disable=redefined-outer-name
    """Do identifiers pass as programs?"""
    code = 'x;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'identifier'
    assert tree['body']['value'] == 'x'

def test_valid_multi_char_identifier(parser):  # pylint: disable=redefined-outer-name
    """Does a multi character identifier pass as a program?"""
    tree = parser.parse('abc;')
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'identifier'
    assert tree['body']['value'] == 'abc'

def test_valid_binary_expression(parser):  # pylint: disable=redefined-outer-name
    """Do binary expressions pass as programs?"""
    code = '42 + 8;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'binary_expression'
    assert tree['body']['operator'] == '+'
    assert tree['body']['left']['type'] == 'integer_literal'
    assert tree['body']['left']['value'] == 42
    assert tree['body']['right']['type'] == 'integer_literal'
    assert tree['body']['right']['value'] == 8

def test_valid_mixed_binary_expression(parser):  # pylint: disable=redefined-outer-name
    """Do mixed binary expressions pass as programs?"""
    code = 'x > 0;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'binary_expression'
    assert tree['body']['operator'] == '>'
    assert tree['body']['left']['type'] == 'identifier'
    assert tree['body']['left']['value'] == 'x'
    assert tree['body']['right']['type'] == 'integer_literal'
    assert tree['body']['right']['value'] == 0

def test_valid_function_call(parser):  # pylint: disable=redefined-outer-name
    """Do function calls pass as programs?"""
    code = 'add(10, 20);'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'function_call'
    assert tree['body']['name'] == 'add'
    assert len(tree['body']['arguments']) == 2
    assert tree['body']['arguments'][0]['type'] == 'integer_literal'
    assert tree['body']['arguments'][0]['value'] == 10
    assert tree['body']['arguments'][1]['type'] == 'integer_literal'
    assert tree['body']['arguments'][1]['value'] == 20

def test_valid_function_call_no_args(parser):  # pylint: disable=redefined-outer-name
    """Do function calls w/o arguments pass as programs?"""
    code = 'foo();'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'function_call'
    assert tree['body']['name'] == 'foo'
    assert len(tree['body']['arguments']) == 0

def test_valid_multiplicative_precedence(parser):  # pylint: disable=redefined-outer-name
    """Is the order of operations applied properly?"""
    code = '2 + 3 * 4;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert tree['body']['type'] == 'binary_expression'
    assert tree['body']['operator'] == '+'
    assert tree['body']['left']['type'] == 'integer_literal'
    assert tree['body']['left']['value'] == 2
    assert tree['body']['right']['type'] == 'binary_expression'
    assert tree['body']['right']['operator'] == '*'
    assert tree['body']['right']['left']['type'] == 'integer_literal'
    assert tree['body']['right']['left']['value'] == 3
    assert tree['body']['right']['right']['type'] == 'integer_literal'
    assert tree['body']['right']['right']['value'] == 4

# Test invalid syntax
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
