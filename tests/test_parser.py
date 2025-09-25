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
    """Do integers pass as statements?"""
    code = "42;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'integer_literal'
    assert tree['body'][0]['value'] == 42

def test_valid_negative_integer(parser):  # pylint: disable=redefined-outer-name
    """Do negative integers pass as statements?"""
    code = "-42;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'integer_literal'
    assert tree['body'][0]['value'] == -42

def test_valid_float(parser):  # pylint: disable=redefined-outer-name
    """Do floats pass as statements?"""
    code = "3.14;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'float_literal'
    assert tree['body'][0]['value'] == 3.14

def test_valid_negative_float(parser):  # pylint: disable=redefined-outer-name
    """Do floats pass as statements?"""
    code = "-3.14;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'float_literal'
    assert tree['body'][0]['value'] == -3.14

def test_valid_string_double_quotes(parser):  # pylint: disable=redefined-outer-name
    """Do double-quote strings pass as statements?"""
    code = '"hello";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'string_literal'
    assert tree['body'][0]['value'] == 'hello'

def test_valid_string_single_quotes(parser):  # pylint: disable=redefined-outer-name
    """Do single-quote strings pass as statements?"""
    code = "'hello';"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'string_literal'
    assert tree['body'][0]['value'] == 'hello'

def test_valid_string_with_space(parser):  # pylint: disable=redefined-outer-name
    """Do strings with spaces pass as statements?"""
    code = '"Hello World";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'string_literal'
    assert tree['body'][0]['value'] == 'Hello World'

def test_valid_string_with_escaped_apostrophy(parser):  # pylint: disable=redefined-outer-name
    """Do strings with escaped characters pass as statements?"""
    code = "'How\\'s it going?';"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'string_literal'
    assert tree['body'][0]['value'] == 'How\'s it going?'

def test_valid_string_with_escaped_newline(parser):  # pylint: disable=redefined-outer-name
    """Do strings with escaped characters pass as statements?"""
    code = '"Hello\\nWorld";'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'string_literal'
    assert tree['body'][0]['value'] == 'Hello\nWorld'

def test_true_literal(parser):  # pylint: disable=redefined-outer-name
    """Does true; pass as a program?"""
    code = 'true;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'boolean_literal'
    assert tree['body'][0]['value'] is True

def test_false_literal(parser):  # pylint: disable=redefined-outer-name
    """Does false; pass as a program?"""
    code = 'false;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'boolean_literal'
    assert tree['body'][0]['value'] is False

def test_valid_identifier(parser):  # pylint: disable=redefined-outer-name
    """Do identifiers pass as statements?"""
    code = 'x;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'identifier'
    assert tree['body'][0]['value'] == 'x'

def test_valid_multi_char_identifier(parser):  # pylint: disable=redefined-outer-name
    """Does a multi character identifier pass as a program?"""
    tree = parser.parse('abc;')
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'identifier'
    assert tree['body'][0]['value'] == 'abc'

def test_valid_binary_expression(parser):  # pylint: disable=redefined-outer-name
    """Do binary expressions pass as statements?"""
    code = '42 + 8;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'binary_expression'
    assert tree['body'][0]['operator'] == '+'
    assert tree['body'][0]['left']['type'] == 'integer_literal'
    assert tree['body'][0]['left']['value'] == 42
    assert tree['body'][0]['right']['type'] == 'integer_literal'
    assert tree['body'][0]['right']['value'] == 8

def test_valid_mixed_binary_expression(parser):  # pylint: disable=redefined-outer-name
    """Do mixed binary expressions pass as statements?"""
    code = 'x > 0;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'binary_expression'
    assert tree['body'][0]['operator'] == '>'
    assert tree['body'][0]['left']['type'] == 'identifier'
    assert tree['body'][0]['left']['value'] == 'x'
    assert tree['body'][0]['right']['type'] == 'integer_literal'
    assert tree['body'][0]['right']['value'] == 0

def test_valid_function_call(parser):  # pylint: disable=redefined-outer-name
    """Do function calls pass as statements?"""
    code = 'add(10, 20);'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'function_call'
    assert tree['body'][0]['name'] == 'add'
    assert len(tree['body'][0]['arguments']) == 2
    assert tree['body'][0]['arguments'][0]['type'] == 'integer_literal'
    assert tree['body'][0]['arguments'][0]['value'] == 10
    assert tree['body'][0]['arguments'][1]['type'] == 'integer_literal'
    assert tree['body'][0]['arguments'][1]['value'] == 20

def test_valid_function_call_no_args(parser):  # pylint: disable=redefined-outer-name
    """Do function calls w/o arguments pass as statements?"""
    code = 'foo();'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'function_call'
    assert tree['body'][0]['name'] == 'foo'
    assert len(tree['body'][0]['arguments']) == 0

def test_valid_multiplicative_precedence(parser):  # pylint: disable=redefined-outer-name
    """Is the order of operations applied properly?"""
    code = '2 + 3 * 4;'
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'binary_expression'
    assert tree['body'][0]['operator'] == '+'
    assert tree['body'][0]['left']['type'] == 'integer_literal'
    assert tree['body'][0]['left']['value'] == 2
    assert tree['body'][0]['right']['type'] == 'binary_expression'
    assert tree['body'][0]['right']['operator'] == '*'
    assert tree['body'][0]['right']['left']['type'] == 'integer_literal'
    assert tree['body'][0]['right']['left']['value'] == 3
    assert tree['body'][0]['right']['right']['type'] == 'integer_literal'
    assert tree['body'][0]['right']['right']['value'] == 4

def test_valid_variable_declaration(parser):  # pylint: disable=redefined-outer-name
    """Do variable declarations pass as statements?"""
    code = "int x = 42;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'variable_declaration'
    assert tree['body'][0]['var_type'] == 'int'
    assert tree['body'][0]['name'] == 'x'
    assert tree['body'][0]['operator'] == '='
    assert tree['body'][0]['expression']['type'] == 'integer_literal'
    assert tree['body'][0]['expression']['value'] == 42

def test_valid_multi_statement(parser):  # pylint: disable=redefined-outer-name
    """Do multiple statements pass as a program?"""
    code = "int x = 42; int y = 20;"
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 2
    assert tree['body'][0]['type'] == 'variable_declaration'
    assert tree['body'][0]['var_type'] == 'int'
    assert tree['body'][0]['name'] == 'x'
    assert tree['body'][0]['operator'] == '='
    assert tree['body'][0]['expression']['type'] == 'integer_literal'
    assert tree['body'][0]['expression']['value'] == 42
    assert tree['body'][1]['type'] == 'variable_declaration'
    assert tree['body'][1]['var_type'] == 'int'
    assert tree['body'][1]['name'] == 'y'
    assert tree['body'][1]['operator'] == '='
    assert tree['body'][1]['expression']['type'] == 'integer_literal'
    assert tree['body'][1]['expression']['value'] == 20

def test_valid_multi_statement_with_newlines(parser):  # pylint: disable=redefined-outer-name
    """Do multiple statements separated by newlines pass as a program?"""
    code = """
int x = 42;
int y = 20;
add(10, 20);
"""
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 3
    assert tree['body'][0]['type'] == 'variable_declaration'
    assert tree['body'][0]['var_type'] == 'int'
    assert tree['body'][0]['name'] == 'x'
    assert tree['body'][0]['operator'] == '='
    assert tree['body'][0]['expression']['type'] == 'integer_literal'
    assert tree['body'][0]['expression']['value'] == 42
    assert tree['body'][1]['type'] == 'variable_declaration'
    assert tree['body'][1]['var_type'] == 'int'
    assert tree['body'][1]['name'] == 'y'
    assert tree['body'][1]['operator'] == '='
    assert tree['body'][1]['expression']['type'] == 'integer_literal'
    assert tree['body'][1]['expression']['value'] == 20
    assert tree['body'][2]['type'] == 'function_call'
    assert tree['body'][2]['name'] == 'add'
    assert len(tree['body'][2]['arguments']) == 2
    assert tree['body'][2]['arguments'][0]['type'] == 'integer_literal'
    assert tree['body'][2]['arguments'][0]['value'] == 10
    assert tree['body'][2]['arguments'][1]['type'] == 'integer_literal'
    assert tree['body'][2]['arguments'][1]['value'] == 20

def test_valid_function_declaration(parser):  # pylint: disable=redefined-outer-name
    """Do function declarations pass as statements?"""
    code = """
int add(int a, int b):
    return a + b;
"""
    tree = parser.parse(code)
    pretty_print(tree)
    assert tree is not None
    assert tree['type'] == 'program'
    assert len(tree['body']) == 1
    assert tree['body'][0]['type'] == 'function_declaration'
    assert tree['body'][0]['return_type'] == 'int'
    assert tree['body'][0]['name'] == 'add'
    assert len(tree['body'][0]['parameters']) == 2
    assert tree['body'][0]['parameters'][0]['type'] == 'parameter'
    assert tree['body'][0]['parameters'][0]['param_type'] == 'int'
    assert tree['body'][0]['parameters'][0]['name'] == 'a'
    assert tree['body'][0]['parameters'][1]['type'] == 'parameter'
    assert tree['body'][0]['parameters'][1]['param_type'] == 'int'
    assert tree['body'][0]['parameters'][1]['name'] == 'b'
    assert len(tree['body'][0]['body']) == 1
    assert tree['body'][0]['body'][0]['type'] == 'return_statement'
    assert tree['body'][0]['body'][0]['expression']['type'] == 'binary_expression'
    assert tree['body'][0]['body'][0]['expression']['operator'] == '+'
    assert tree['body'][0]['body'][0]['expression']['left']['type'] == 'identifier'
    assert tree['body'][0]['body'][0]['expression']['left']['value'] == 'a'
    assert tree['body'][0]['body'][0]['expression']['right']['type'] == 'identifier'
    assert tree['body'][0]['body'][0]['expression']['right']['value'] == 'b'

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
    code = "int x = 42; int y = 20"
    with pytest.raises(SyntaxError, match=r"Expected semicolon after statement"):
        parser.parse(code)

def test_invalid_void_variable(parser):  # pylint: disable=redefined-outer-name
    """Can parser detect invalid vaiable type?"""
    code = "void x = 42;"
    with pytest.raises(SyntaxError, match=r"Keyword 'void' cannot be used to declare variables. " \
                                          r"Expected: int, float, str, or bool"):
        parser.parse(code)
