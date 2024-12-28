from errors import StarshipError


class StarshipToken:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __str__(self):
        return f"Token({self.type}, {self.value}, line {self.line})"


class StarshipLexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if self.text else None
        self.line = 1

        self.keywords = {
            "MISSION:",
            "CARGO:",
            "FLIGHT_PLAN:",
            "END_MISSION",
            "QUANTUM:",
            "ORBIT",
            "BEAM",
            "SCAN",
            "DOCK",
            "DETECTED",
            "ABORT_MISSION",
            "SUB_MISSION:",
            "REQUIRES:",
            "PROVIDES:",
            "RETURN",
            "SET",
            "LAUNCH",
            "NAVIGATE",
            "TO",
            "QUANTUM_LOOP",
            "STORE",
            "IN",
            "QUANTUM_CALCULATE:",
            "END_QUANTUM",
            "STABILIZE",
            "VERIFY",
            "EXTRACT",
            "INTO",
            "APPEND",
            "INITIALIZE",
            "IF",
            "WITH",
            "as",
            "TIMES:",
            "TIMES",
            "DISPLAY",
            "to",
            "with",
            "TO",
            "DOCK",
            "UNDOCK",
            "BOOST",
            "SPLIT",
        }

        self.types = {
            "METRIC",
            "SIGNAL",
            "BEACON",
            "CONSTELLATION",
            "VECTOR",
            "MATRIX",
            "QUANTUM_BUFFER",
        }

        self.operators = {
            "+": "PLUS",
            "-": "MINUS",
            "*": "MULTIPLY",
            "/": "DIVIDE",
            "=": "ASSIGN",
            "[": "LBRACKET",
            "]": "RBRACKET",
            ",": "COMMA",
            ":": "COLON",
            "(": "LPAREN",
            ")": "RPAREN",
            ".": "DOT",
        }

    def error(self):
        raise StarshipError(f'Invalid character "{self.current_char}"', self.line)

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            if self.current_char == "\n":
                self.line += 1

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_identifier(self):
        result = ""
        while self.current_char and (
            self.current_char.isalnum() or self.current_char in "_:"
        ):
            result += self.current_char
            self.advance()
        return result

    def get_string(self):
        result = ""
        self.advance()
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()
        return result

    def tokenize(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                tokens.append(StarshipToken("NUMBER", self.get_number(), self.line))
                if self.current_char == ".":
                    tokens.append(StarshipToken("DOT", ".", self.line))
                    self.advance()
                continue

            if self.current_char.isalpha():
                word = self.get_identifier()
                if word in self.keywords:
                    tokens.append(StarshipToken("KEYWORD", word, self.line))
                elif word in self.types:
                    tokens.append(StarshipToken("TYPE", word, self.line))
                else:
                    tokens.append(StarshipToken("IDENTIFIER", word, self.line))
                continue

            if self.current_char == '"':
                tokens.append(StarshipToken("STRING", self.get_string(), self.line))
                continue

            if self.current_char in self.operators:
                token_type = self.operators[self.current_char]
                tokens.append(StarshipToken(token_type, self.current_char, self.line))
                self.advance()
                continue

            self.error()

        return tokens
