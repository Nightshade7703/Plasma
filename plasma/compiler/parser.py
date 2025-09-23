"""
Parses .pls files for correct syntax.
"""
class PlasmaTokenizer:
    """Class for tokenizing Plasma code."""
    def __init__(self, code: str):
        self.code = code
        self.cursor = 0

    def isEOF(self):
        """Checks if the cursor has reached the end of the file."""
        return self.cursor == len(self.code)

    def has_more_tokens(self):
        """Checks if the provided code still has tokens."""
        return self.cursor < len(self.code)

    def get_next_token(self):
        """Obtains the next token."""
        if not self.has_more_tokens():
            return None

        while self.cursor < len(self.code) and self.code[self.cursor].isspace():
            self.cursor += 1

        if not self.has_more_tokens():
            return None

        char = self.code[self.cursor]

        # Integer
        if char.isdigit():
            integer = ''
            while self.cursor < len(self.code) and self.code[self.cursor].isdigit():
                integer += self.code[self.cursor]
                self.cursor += 1
            return {
                'type': 'INT',
                'value': integer,
            }

        # String
        if char == '"':
            string = ''
            self.cursor += 1  # Skip opening quote
            start_pos = self.cursor
            while self.cursor < len(self.code) and self.code[self.cursor] != '"':
                string += self.code[self.cursor]
                self.cursor += 1
            if self.cursor >= len(self.code):
                raise SyntaxError(f"Unterminated string starting at position {start_pos -1}")
            string += self.code[self.cursor]  # Include closing quote in token
            self.cursor += 1  # Skip closing quote
            return {
                'type': 'STR',
                'value': string,
            }

        # Semicolon
        if char == ';':
            self.cursor += 1
            return {
                'type': 'SEMI',
                'value': ';',
            }

        self.cursor += 1
        raise SyntaxError(f"Invalid character at position {self.cursor - 1}: '{char}'")

class PlasmaParser:
    """Class for compiler parsing logic."""
    def __init__(self):
        """Initializes the code variable."""
        self.code = ''
        self.tokenizer = PlasmaTokenizer('')
        self.lookahead = None

    def parse(self, code:str):
        """Parses the code provided by the source parameter."""
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
        """Returns a literal of type int or str."""
        if self.lookahead is None:
            raise SyntaxError("Unexpected end of input in literal")
        if self.lookahead['type'] == 'INT':
            return self.integer()
        if self.lookahead['type'] == 'STR':
            return self.string()
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

    def string(self):
        """Returns a string literal."""
        token = self.eat('STR')
        return {
            'type': 'string_literal',
            'value': token['value'][0:-1],  # Strip quotes
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
