"""
Parses .pls files for correct syntax.
"""
import re

class PlasmaTokenizer:
    """Class for tokenizing Plasma code."""
    def __init__(self, code: str):
        self.code = code
        self.cursor = 0
        self.indent_stack = [0]
        # Regex patterns for tokens
        self.token_patterns = [
            ('FLOAT', r'-?\d+\.\d+'),
            ('INT', r'-?\d+'),
            ('STR', r'"(?:[^"\\]|\\.)*"' + r'|\'(?:[^\'\\]|\\.)*\''),
            ('BOOL', r'true|false'),
            ('TYPE', r'int|float|str|bool|void'),
            ('RETURN', r'return'),
            ('OPERATOR', r'[+\-*/]|[=!<>]?=|[<>]'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('SEMI', r';'),
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'\s+'),
            ('COMMENT', r'//[^\n]*'),
        ]
        self.regex = re.compile(
            '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns),
            re.ASCII,
        )

    def has_more_tokens(self):
        """Checks if the provided code still has tokens."""
        return self.cursor < len(self.code)

    def get_next_token(self):
        """Obtains the next token using regex."""
        if not self.has_more_tokens():
            return None

        match = self.regex.match(self.code, self.cursor)

        if not match:
            raise SyntaxError(
                f"Invalid character at position {self.cursor}: '{self.code[self.cursor]}'")

        for name, value in match.groupdict().items():
            if value is not None:
                if name in ('WHITESPACE', 'COMMENT'):
                    self.cursor = match.end()
                    return self.get_next_token()
                if name == 'NEWLINE':
                    self.cursor = match.end()
                    return self._handle_indentation()
                if name == 'IDENTIFIER' and value in {'true', 'false', 'int', 'float', 'str',
                                                      'bool', 'void', 'if', 'elif', 'else',
                                                      'while', 'for', 'in', 'range', 'return'}:
                    raise SyntaxError(f"Unexpected keyword '{value}' cannot be used as an " \
                                      f"identifier at position {self.cursor - len(value)}")
                self.cursor = match.end()
                return {
                    'type': name,
                    'value': value,
                }

        raise SyntaxError(
            f"Invalid character at position {self.cursor}: '{self.code[self.cursor]}'")

    def _handle_indentation(self):
        """Handles INDENT/DEDENT after a newline."""
        # Measure indentation (spaces after newline)
        indent_match = re.match(r'[ \t]*', self.code[self.cursor:])
        indent_size = len(indent_match.group(0))
        self.cursor += indent_size

        # Skip blank lines or lines with only comments
        if re.match(r'//[^\n]*', self.code[self.cursor:]) or self.cursor >= len(self.code):
            return self.get_next_token()

        current_indent = self.indent_stack[-1]

        if indent_size > current_indent:
            self.indent_stack.append(indent_size)
            return {'type': 'INDENT', 'value': ''}
        if indent_size < current_indent:
            dedents = []
            while indent_size < self.indent_stack[-1]:
                self.indent_stack.pop()
                dedents.append({'type': 'DEDENT', 'value': ''})
            if indent_size != self.indent_stack[-1]:
                raise SyntaxError(f"Inconsistent indentation at position {self.cursor}")
            if dedents:
                return dedents[0]
        return self.get_next_token()  # No change, continue

class PlasmaParser:
    """Class for compiler parsing logic."""
    def __init__(self):
        """Initializes the code variable, tokenizer, and lookahead."""
        self.code = ''
        self.tokenizer = PlasmaTokenizer('')
        self.lookahead = None

    def parse(self, code:str):
        """Parses the code provided by the code parameter."""
        self.code = code
        self.tokenizer = PlasmaTokenizer(code)
        self.lookahead = self.tokenizer.get_next_token()
        return self._program()

    def _program(self):
        """Parses a program based on the rule program = { statement } ;"""
        node = {
            'type': 'program',
            'body': [],
        }
        # Parse statements until EOF
        while self.lookahead and self.lookahead['type'] is not None:
            stmt = self._statement()
            node['body'].append(stmt)
            # Require SEMI after each statement
            if self.lookahead and self.lookahead['type'] == 'SEMI':
                self._eat('SEMI')
            else:
                raise SyntaxError("Expected semicolon after statement")
        return node

    def _statement(self):
        """Parses a statement (variable_declaration, function_declaration, if_statement,
        while_statement, for_statement, or return_statement)"""
        # Check for data type or specific keyword
        if self.lookahead['type'] == 'TYPE':
            return self._variable_declaration()
        if self.lookahead['type'] == 'RETURN':
            return self._return_statement()
        return self._expression()

    def _variable_declaration(self):
        """Checks for a function declaration and parses a variable declaration if no LPAREN."""
        decl_type = self._eat('TYPE')['value']
        # Check for function declaration (type & IDENTIFIER followed by LPAREN)
        if self.lookahead['type'] == 'IDENTIFIER' and (self._lookahead_next()
                and self._lookahead_next()['type'] == 'LPAREN'):
            return self._function_declaration(decl_type)
        if self.lookahead['type'] == 'IDENTIFIER':
            if decl_type in ('int', 'float', 'str', 'bool'):
                if self._lookahead_next() and (self._lookahead_next()['type'] == 'OPERATOR' and
                        self._lookahead_next()['value'] == '='):
                    name = self._eat('IDENTIFIER')['value']
                    self._eat('OPERATOR')
                    return {
                        'type': 'variable_declaration',
                        'var_type': decl_type,
                        'name': name,
                        'operator': '=',
                        'expression': self._expression(),
                    }
                raise SyntaxError("Assignment operator not found. Expected: '='")
            if decl_type == 'void':
                raise SyntaxError("Keyword 'void' cannot be used to declare variables. " \
                                  "Expected: int, float, str, or bool")
        raise SyntaxError(f"Unexpected token after type '{decl_type}'. Expected: IDENTIFIER")

    def _function_declaration(self, return_type):
        """Parses a function declaration with parameters if applicable."""
        name = self._eat('IDENTIFIER')['value']
        self._eat('LPAREN')
        params = []
        if self.lookahead and self.lookahead['type'] != 'RPAREN':
            params.append(self._parameter())
            while self.lookahead and self.lookahead['type'] == 'COMMA':
                self._eat('COMMA')
                params.append(self._parameter())
        self._eat('RPAREN')
        self._eat('COLON')
        self._eat('INDENT')
        body = []
        while self.lookahead and self.lookahead['type'] != 'DEDENT':
            body.append(self._statement())
            if self.lookahead and self.lookahead['type'] == 'SEMI':
                self._eat('SEMI')
        self._eat('DEDENT')
        return {
            'type': 'function_declaration',
            'return_type': return_type,
            'name': name,
            'parameters': params,
            'body': body,
        }

    def _parameter(self):
        """Parses a parameter."""
        param_type = self._eat('TYPE')['value']
        name = self._eat('IDENTIFIER')['value']
        return {'type': 'parameter', 'param_type': param_type, 'name': name}

    def _return_statement(self):
        """Parses a return statement."""
        self._eat('RETURN')
        if self.lookahead['type'] == 'SEMI':
            return {'type': 'return_statement', 'expression': self._expression()}

    def _expression(self):
        """Parses an expression (comparative_expression or function_call)."""
        # Check for function call (IDENTIFIER followed by LPAREN)
        if self.lookahead['type'] == 'IDENTIFIER' and (self._lookahead_next()
                and self._lookahead_next()['type'] == 'LPAREN'):
            return self._function_call()
        # Otherwise, parse addative expression
        return self._comparative_expression()

    def _comparative_expression(self):
        """Parses comparison expressions (==, !=, <, >, <=, >=) with low precedence."""
        left = self._additive_expression()
        while self.lookahead and (self.lookahead['type'] == 'OPERATOR' and
                self.lookahead['value'] in ('==', '!=', '<', '>', '<=', '>=')):
            operator = self._eat('OPERATOR')['value']
            right = self._additive_expression()
            left = {
                'type': 'binary_expression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    def _additive_expression(self):
        """Parses addative expressions (+, -) with middle precedence."""
        left = self._multiplicative_expression()
        while self.lookahead and (self.lookahead['type'] == 'OPERATOR' and
                self.lookahead['value'] in ('+', '-')):
            operator = self._eat('OPERATOR')['value']
            right = self._multiplicative_expression()
            left = {
                'type': 'binary_expression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    def _multiplicative_expression(self):
        """Parses multiplicative expressions (*, /) with higher precedence."""
        left = self._primary_expression()
        while self.lookahead and (self.lookahead['type'] == 'OPERATOR' and
            self.lookahead['value'] in ('*', '/')):
            operator = self._eat('OPERATOR')['value']
            right = self._primary_expression()
            left = {
                'type': 'binary_expression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    def _primary_expression(self):
        """Parses primary expressions (literal or identifier)."""
        if self.lookahead['type'] in ('INT', 'FLOAT', 'STR', 'BOOL'):
            return self._literal()
        if self.lookahead['type'] == 'IDENTIFIER':
            return self._identifier()
        raise SyntaxError(f"Unexpected token type: {self.lookahead['type']}. " \
                          "Expected: INT, FLOAT, STR, BOOL, or IDENTIFIER")

    def _literal(self):
        """Returns a literal (int, float, str, or bool)."""
        if self.lookahead is None:
            raise SyntaxError("Unexpected end of input in literal")
        if self.lookahead['type'] == 'INT':
            return self._integer()
        if self.lookahead['type'] == 'FLOAT':
            return self._float()
        if self.lookahead['type'] == 'STR':
            return self._string()
        if self.lookahead['type'] == 'BOOL':
            return self._boolean()
        raise SyntaxError(f"Unexpected token type: {self.lookahead['type']}. " \
                          "Expected: INT, FLOAT, STR, BOOL")

    def _integer(self):
        """Returns an integer literal."""
        token = self._eat('INT')
        try:
            return {
                'type': 'integer_literal',
                'value': int(token['value']),
            }
        except ValueError as exc:
            raise SyntaxError(f"Invalid integer literal: '{token['value']}") from exc

    def _float(self):
        """Returns a float literal."""
        token = self._eat('FLOAT')
        try:
            return {
                'type': 'float_literal',
                'value': float(token['value']),
            }
        except ValueError as exc:
            raise SyntaxError(f"Invalid float literal: '{token['value']}") from exc

    def _string(self):
        """Returns a string literal."""
        token = self._eat('STR')
        raw_value = token['value'][1:-1]
        value = re.sub(r'\\([\'"\\nt])', lambda m: {
            '\\': '\\', 'n': '\n', 't': '\t', '"': '"', "'": "'"}[m.group(1)], raw_value)
        return {
            'type': 'string_literal',
            'value': value
        }

    def _boolean(self):
        """Returns a true or false literal."""
        token = self._eat('BOOL')
        return {
            'type': 'boolean_literal',
            'value': token['value'] == 'true',  # Convert 'true'/'false' to True/False
        }

    def _identifier(self):
        """Returns an identifier."""
        token = self._eat('IDENTIFIER')
        return {
            'type': 'identifier',
            'value': token['value'],
        }

    def _function_call(self):
        """Returns a function call."""
        name = self._eat('IDENTIFIER')['value']
        self._eat('LPAREN')
        args = []
        if self.lookahead and self.lookahead['type'] != 'RPAREN':
            args.append(self._expression())
            while self.lookahead and self.lookahead['type'] == 'COMMA':
                self._eat('COMMA')
                args.append(self._expression())
        self._eat('RPAREN')
        return {
            'type': 'function_call',
            'name': name,
            'arguments': args,
        }

    def _lookahead_next(self):
        """Returns the next token without consuming it."""
        current_cursor = self.tokenizer.cursor
        token = self.tokenizer.get_next_token()
        self.tokenizer.cursor = current_cursor
        return token

    def _eat(self, token_type):
        """Expects a token of a given type."""
        token = self.lookahead
        if token is None:
            raise SyntaxError(f'Unexpected end of input. Expected: {token_type}')
        if token['type'] != token_type:
            raise SyntaxError(f'Unexpected token: {token['value']}. Expected: {token_type}')
        self.lookahead = self.tokenizer.get_next_token()
        return token
