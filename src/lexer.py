from .types import *

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def variable(self):
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return (INTEGER, self.integer())

            if self.current_char.isalpha():
                variable = self.variable()
                if variable == "if":
                    return (IF, variable)
                elif variable == "else":
                    return (ELSE, variable)
                elif variable == "fn":
                    return (FN, variable)
                elif variable == "class":
                    return (CLASS, variable)
                else:
                    return (VARIABLE, variable)

            if self.current_char == "+":
                self.advance()
                return (PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return (MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return (MULTIPLY, "*")

            if self.current_char == "/":
                self.advance()
                return (DIVIDE, "/")

            if self.current_char == "(":
                self.advance()
                return (LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return (RPAREN, ")")

            if self.current_char == ":":
                self.advance()
                return (COLON, ":")

            if self.current_char == ";":
                self.advance()
                return (SEMICOLON, ";")

            if self.current_char == "=":
                self.advance()
                return (EQUALS, "=")

            if self.current_char == ",":
                self.advance()
                return (COMMA, ",")

            if self.current_char == ".":
                self.advance()
                return (DOT, ".")

            if self.current_char == "{":
                self.advance()
                return (LBRACE, "{")

            if self.current_char == "}":
                self.advance()
                return (RBRACE, "}")

            if self.current_char == "-":
                if self.peek() == ">":
                    self.advance()
                    self.advance()
                    return (ARROW, "->")
                else:
                    self.error()

            self.error()

        return None
