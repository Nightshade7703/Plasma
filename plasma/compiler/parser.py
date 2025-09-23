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
            ('FLOAT', r'\d+\.\d+'),             # float: digit { digit } . digit { digit }
            ('INT', r'\d+'),                    # integer: digit { digit }
            ('STR', r'"[^"]*"|\'[^\']*\''),     # string: " { character } " (letter | digit)
            ('BOOL', r'true|false'),            # boolean: true | false
            ('SEMI', r';'),                     # semicolon
            ('WHITESPACE', r'\s+'),             # whitespace (to skip)
            ('COMMENT', r'//[^\n]*'),           # C-style comments (to skip)
        ]
        # Compile regex with all patterns
        self.regex = re.compile(
            '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns)
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

        # Find the next match starting from cursor
        match = self.regex.match(self.code, self.cursor)
        if not match:
            raise SyntaxError(
                f"Invalid character at position {self.cursor}: '{self.code[self.cursor]}'"
            )

        # Get the matched token
        for name, value in match.groupdict().items():
            if value is not None and name != 'WHITESPACE':
                self.cursor = match.end()
                return {
                    'type': name,
                    'value': value,
                }
            if value is not None and name == 'WHITESPACE':
                self.cursor = match.end()
                return self.get_next_token()  # Skip whitespace and try next token

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
        return self.program()

    def program(self):
        """Returns a program based on the rule program = literal ;"""
        node = {
            'type': 'program',
            'body': self.literal(),
        }
        self.eat('SEMI')
        return node

    def literal(self):
        """Returns a literal of type int, float, str, or bool."""
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
        raise SyntaxError(f"Unexpected token type: {self.lookahead['type']}. Expected: INT or STR")

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
        return {
            'type': 'string_literal',
            'value': token['value'][1:-1],  # Strip quotes
        }

    def boolean(self):
        """Returns a true or false literal."""
        token = self.eat('BOOL')
        return {
            'type': 'boolean_literal',
            'value': token['value'] == 'true',  # Convert 'true'/'false' to True/False
        }

    def eat(self, token_type):
        """Expects a token of a given type."""
        token = self.lookahead
        if token is None:
            raise SyntaxError(f'Unexpected end of input. Expected: {token_type}')
        if token['type'] != token_type:
            raise SyntaxError(f'Unexpected token: {token['value']}. Expected: {token_type}')
        self.lookahead = self.tokenizer.get_next_token()
        return token
