"""
Parses .pls files for correct syntax.
"""
import re

class PlasmaTokenizer:
    """Class for tokenizing Plasma code."""
    def __init__(self, code: str):
        self.code = code
        self.cursor = 0
        # Regex patterns for tokens
        self.token_patterns = [
            ('FLOAT', r'-?\d+\.\d+'),
            ('INT', r'-?\d+'),
            ('STR', r'"(?:[^"\\]|\\.)*"' + r'|\'(?:[^\'\\]|\\.)*\''),
            ('BOOL', r'true|false'),
            ('OPERATOR', r'[+\-*/]|[=!<>]=|[<>]'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('SEMI', r';'),
            ('WHITESPACE', r'\s+'),
        ]
        self.regex = re.compile(
            '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns),
            re.ASCII,
        )

    def is_eof(self):
        """Checks if the cursor has reached the end of the file."""
        return self.cursor >= len(self.code)

    def has_more_tokens(self):
        """Checks if the provided code still has tokens."""
        return self.cursor < len(self.code)

    def get_next_token(self):
        """Obtains the next token using regex."""
        if not self.has_more_tokens():
            return None

        print(f"Cursor: {self.cursor}, Code: {self.code[self.cursor]}")
        match = self.regex.match(self.code, self.cursor)
        print(f"Match: {match.groupdict() if match else 'None'}")

        if not match:
            raise SyntaxError(
                f"Invalid character at position {self.cursor}: '{self.code[self.cursor]}'")

        for name, value in match.groupdict().items():
            if value is not None and name != 'WHITESPACE':
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
            if value is not None and name == 'WHITESPACE':
                self.cursor = match.end()
                return self.get_next_token()  # Skip whitespace/comment and try next token

        raise SyntaxError(
            f"Invalid character at position {self.cursor}: '{self.code[self.cursor]}'")

class PlasmaParser:
    """Class for compiler parsing logic."""
    def __init__(self):
        """Initializes the code variable, tokenizer, and lookahead."""
        self.code = ''
        self.tokenizer = PlasmaTokenizer('')
        self.lookahead = None
        self.lookahead_next = {}

    def parse(self, code:str):
        """Parses the code provided by the code parameter."""
        self.code = code
        self.tokenizer = PlasmaTokenizer(code)
        self.lookahead = self.tokenizer.get_next_token()
        return self.program()

    def program(self):
        """Returns a program based on the rule program = expression ;"""
        node = {
            'type': 'program',
            'body': self.expression(),
        }
        self.eat('SEMI')
        return node

    def expression(self):
        """Returns an expression (addative_expression or function_call)."""
        if self.lookahead is None:
            raise SyntaxError("Unexpected end of input in expression")

        # Check for function call (IDENTIFIER followed by LPAREN)
        if self.lookahead['type'] == 'IDENTIFIER' and (self._lookahead_next()
                and self._lookahead_next()['type'] == 'LPAREN'):
            return self.function_call()
        # Otherwise, parse addative expression
        return self.comparison_expression()

    def comparison_expression(self):
        """Parses comparison expressions (==, !=, <, >, <=, >=) with low precedence."""
        left = self.addative_expression()
        while self.lookahead and (self.lookahead['type'] == 'OPERATOR' and
                self.lookahead['value'] in ('==', '!=', '<', '>', '<=', '>=')):
            operator = self.eat('OPERATOR')['value']
            right = self.addative_expression()
            left = {
                'type': 'binary_expression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    def addative_expression(self):
        """Parses addative expressions (+, -) with middle precedence."""
        left = self.multiplicative_expression()
        while self.lookahead and (self.lookahead['type'] == 'OPERATOR' and
                self.lookahead['value'] in ('+', '-')):
            operator = self.eat('OPERATOR')['value']
            right = self.multiplicative_expression()
            left = {
                'type': 'binary_expression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    def multiplicative_expression(self):
        """Parses multiplicative expressions (*, /) with higher precedence."""
        left = self.primary_expression()
        while self.lookahead and (self.lookahead['type'] == 'OPERATOR' and
            self.lookahead['value'] in ('*', '-')):
            operator = self.eat('OPERATOR')['value']
            right = self.primary_expression()
            left = {
                'type': 'binary_expression',
                'operator': operator,
                'left': left,
                'right': right,
            }
        return left

    def primary_expression(self):
        """Parses primary expressions (literal or identifier)."""
        if self.lookahead['type'] in ('INT', 'FLOAT', 'STR', 'BOOL'):
            return self.literal()
        if self.lookahead['type'] == 'IDENTIFIER':
            return self.identifier()
        raise SyntaxError(f"Unexpected token type: {self.lookahead['type']}. " \
                          "Expected: INT, FLOAT, STR, BOOL, or IDENTIFIER")

    def literal(self):
        """Returns a literal (int, float, str, or bool)."""
        if self.lookahead is None:
            raise SyntaxError("Unexpected end of input in literal")
        if self.lookahead['type'] == 'INT':
            return self.integer()
        if self.lookahead['type'] == 'FLOAT':
            return self._float()
        if self.lookahead['type'] == 'STR':
            return self.string()
        if self.lookahead['type'] == 'BOOL':
            return self.boolean()
        raise SyntaxError(f"Unexpected token type: {self.lookahead['type']}. " \
                          "Expected: INT, FLOAT, STR, BOOL")

    def integer(self):
        """Returns an integer literal."""
        token = self.eat('INT')
        try:
            return {
                'type': 'integer_literal',
                'value': int(token['value']),
            }
        except ValueError as exc:
            raise SyntaxError(f"Invalid integer literal: '{token['value']}") from exc

    def _float(self):
        """Returns a float literal."""
        token = self.eat('FLOAT')
        try:
            return {
                'type': 'float_literal',
                'value': float(token['value']),
            }
        except ValueError as exc:
            raise SyntaxError(f"Invalid float literal: '{token['value']}") from exc

    def string(self):
        """Returns a string literal."""
        token = self.eat('STR')
        raw_value = token['value'][1:-1]
        value = re.sub(r'\\([\'"\\nt])', lambda m: {
            '\\': '\\', 'n': '\n', 't': '\t', '"': '"', "'": "'"}[m.group(1)], raw_value)
        return {
            'type': 'string_literal',
            'value': value
        }

    def boolean(self):
        """Returns a true or false literal."""
        token = self.eat('BOOL')
        return {
            'type': 'boolean_literal',
            'value': token['value'] == 'true',  # Convert 'true'/'false' to True/False
        }

    def identifier(self):
        """Returns an identifier."""
        token = self.eat('IDENTIFIER')
        return {
            'type': 'identifier',
            'value': token['value'],
        }

    def function_call(self):
        """Returns a function call."""
        name = self.eat('IDENTIFIER')['value']
        self.eat('LPAREN')
        args = []
        if self.lookahead and self.lookahead['type'] != 'RPAREN':
            args.append(self.expression())
            while self.lookahead and self.lookahead['type'] == 'COMMA':
                self.eat('COMMA')
                args.append(self.expression())
        self.eat('RPAREN')
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

    def eat(self, token_type):
        """Expects a token of a given type."""
        token = self.lookahead
        if token is None:
            raise SyntaxError(f'Unexpected end of input. Expected: {token_type}')
        if token['type'] != token_type:
            raise SyntaxError(f'Unexpected token: {token['value']}. Expected: {token_type}')
        self.lookahead = self.tokenizer.get_next_token()
        return token
