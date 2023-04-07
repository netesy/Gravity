from .lexer import Lexer, Token


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, type_):
        if self.current_token.type == type_:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        if self.current_token.type == "INTEGER":
            token = self.current_token
            self.eat("INTEGER")
            return ("INTEGER", token.value)
        elif self.current_token.type == "VARIABLE":
            token = self.current_token
            self.eat("VARIABLE")
            return ("VARIABLE", token.value)
        elif self.current_token.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.expr()
            self.eat("RPAREN")
            return expr

    def term(self):
        result = self.factor()

        while self.current_token.type in ("MULTIPLY", "DIVIDE"):
            token = self.current_token
            if token.type == "MULTIPLY":
                self.eat("MULTIPLY")
                result = ("MULTIPLY", result, self.factor())
            elif token.type == "DIVIDE":
                self.eat("DIVIDE")
                result = ("DIVIDE", result, self.factor())

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token
            if token.type == "PLUS":
                self.eat("PLUS")
                result = ("PLUS", result, self.term())
            elif token.type == "MINUS":
                self.eat("MINUS")
                result = ("MINUS", result, self.term())

        return result
