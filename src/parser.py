from .lexer import *
from .types import *


# AST nodes
class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class IfStatement(AST):
    def __init__(self, condition, true_statement, false_statement=None):
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement


class FunctionDeclaration(AST):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body


class FunctionInvocation(AST):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class ClassDeclaration(AST):
    def __init__(self, name, body):
        self.name = name
        self.body = body


class ClassAttribute(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ClassMethod(AST):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body


class ReturnStatement(AST):
    def __init__(self, value):
        self.value = value


# Parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == VARIABLE:
            if self.lexer.peek()[1] == LPAREN:
                return self.function_call()
            else:
                return self.variable()
        elif token.type == FN:
            return self.function_definition()
        elif token.type == CLASS:
            return self.class_definition()

    def term(self):
        node = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif token.type == DIVIDE:
                self.eat(DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def return_statement(self):
        self.eat(RETURN)
        value = self.expr()
        return ReturnStatement(value)

    def statement(self):
        if self.current_token.type == IF:
            return self.if_statement()
        elif self.current_token.type == FN:
            return self.function_definition()
        elif self.current_token.type == CLASS:
            return self.class_declaration()
        elif self.current_token.type == RETURN:
            return self.return_statement()
        else:
            node = self.expr()
            self.eat(SEMICOLON)
            return node

    def statement_list(self):
        statements = [self.statement()]

        while self.current_token.type != ENDOF:
            statements.append(self.statement())

        return statements

    def variable(self):
        node = Variable(self.current_token)
        self.eat(VARIABLE)
        return node

    def function_call(self):
        name = self.current_token.value
        self.eat(VARIABLE)
        self.eat(LPAREN)
        args = []
        if self.current_token.type != RPAREN:
            args.append(self.expr())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                args.append(self.expr())
        self.eat(RPAREN)
        return FunctionInvocation(name, args)

    def function_definition(self):
        self.eat(FN)
        name = self.current_token.value
        self.eat(VARIABLE)
        self.eat(LPAREN)
        args = []
        if self.current_token.type != RPAREN:
            args.append(self.current_token.value)
            self.eat(VARIABLE)
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                args.append(self.current_token.value)
                self.eat(VARIABLE)
        self.eat(RPAREN)
        self.eat(ARROW)
        body = self.expr()
        return FunctionDeclaration(name, args, body)

    def if_statement(self):
        self.eat(IF)
        condition = self.comparison_expr()
        self.eat(COLON)
        true_statement = self.expr()
        false_statement = None
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat(COLON)
            false_statement = self.expr()
        return IfStatement(condition, true_statement, false_statement)

    def class_definition(self):
        self.eat(CLASS)
        name = self.current_token.value
        self.eat(VARIABLE)
        self.eat(LBRACE)
        attributes = []
        methods = []

        while self.current_token.type != RBRACE:
            if self.current_token.type == VARIABLE:
                attribute_name = self.current_token.value
                self.eat(VARIABLE)
                self.eat(EQUALS)
                attribute_value = self.expr()
                attributes.append(ClassAttribute(attribute_name, attribute_value))
                self.eat(SEMICOLON)
            elif self.current_token.type == FN:
                method_name = self.current_token.value
                self.eat(FN)
                self.eat(LPAREN)
                args = []
                if self.current_token.type != RPAREN:
                    args.append(self.current_token.value)
                    self.eat(VARIABLE)
                    while self.current_token.type == COMMA:
                        self.eat(COMMA)
                        args.append(self.current_token.value)
                        self.eat(VARIABLE)
                self.eat(RPAREN)
                self.eat(ARROW)
                body = self.expr()
                methods.append(ClassMethod(method_name, args, body))
                self.eat(SEMICOLON)

        self.eat(RBRACE)
        return ClassDeclaration(name, attributes + methods)

    def parse(self):
        node = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return node

    def comparison_expr(self):
        node = self.expr()

        if self.current_token.type in (EQUALS, IF, ELSE):
            token = self.current_token
            if token.type == EQUALS:
                self.eat(EQUALS)
                return Variable(token)
            elif token.type == IF:
                return self.if_statement()
            elif token.type == ELSE:
                self.eat(ELSE)
                self.eat(COLON)
                return self.block()

        if self.current_token.type in (
            LESS_THAN,
            GREATER_THAN,
            LESS_THAN_EQUAL,
            GREATER_THAN_EQUAL,
        ):
            token = self.current_token
            if token.type == LESS_THAN:
                self.eat(LESS_THAN)
            elif token.type == GREATER_THAN:
                self.eat(GREATER_THAN)
            elif token.type == LESS_THAN_EQUAL:
                self.eat(LESS_THAN_EQUAL)
            elif token.type == GREATER_THAN_EQUAL:
                self.eat(GREATER_THAN_EQUAL)

            return BinOp(left=node, op=token, right=self.expr())

        return node


# def if_statement(self):
#     self.eat(IF)
#     condition = self.comparison_expr()
#     self.eat(COLON)
#     true_statement = self.block()

#     false_statement = None
#     if self.current_token.type == ELSE:
#         self.eat(ELSE)
#         self.eat(COLON)
#         false_statement = self.block()

#     return IfStatement(condition, true_statement, false_statement)

# def block(self):
#     nodes = []
#     while self.current_token.type not in (RBRACE, EOF):
#         nodes.append(self.statement())
#         self.eat(NEWLINE)

#     return nodes

# def function_definition(self):
#     self.eat(FN)
#     name = self.current_token.value
#     self.eat(VARIABLE)
#     self.eat(LPAREN)
#     args = []
#     if self.current_token.type != RPAREN:
#         args.append(self.variable().value)
#         while self.current_token.type == COMMA:
#             self.eat(COMMA)
#             args.append(self.variable().value)
#     self.eat(RPAREN)
#     self.eat(ARROW)
#     body = self.block()
#     return FunctionDeclaration(name, args, body)

# def function_call(self):
#     name = self.variable().value
#     self.eat(LPAREN)
#     args = []
#     if self.current_token.type != RPAREN:
#         args.append(self.expr())
#         while self.current_token.type == COMMA:
#             self.eat(COMMA)
#             args.append(self.expr())
#     self.eat(RPAREN)
#     return FunctionInvocation(name, args)

# def class_definition(self):
#     self.eat(CLASS)
#     name = self.current_token.value
#     self.eat(VARIABLE)
#     self.eat(LBRACE)
#     body = []
#     while self.current_token.type != RBRACE:
#         if self.current_token.type == VARIABLE:
#             body.append(self.attribute_declaration())
#         elif self.current_token.type == FN:
#             body.append(self.method_declaration())
#         else:
#             self.error()
#     self.eat(RBRACE)
#     return ClassDeclaration(name, body)

# def attribute_declaration(self):
#     name = self.variable()
#     self.eat(EQUALS)
#     value = self.expr()
#     return ClassAttribute(name, value)

# def method_declaration(self):
#     self.eat(FN)
#     name = self.current_token.value
#     self.eat(VARIABLE)
#     self.eat(LPAREN)
#     args = []
#     if self.current_token.type != RPAREN:
#         args.append(self.variable().value)
#         while self.current_token.type == COMMA:
#             self.eat(COMMA)
#         elif token.type == LESS_THAN:
#             self.eat(LESS_THAN)
#         elif token.type == GREATER_THAN:
#             self.eat(GREATER_THAN)
#         elif token.type == LESS_THAN_EQUAL:
#             self.eat(LESS_THAN_EQUAL)
#         elif token.type == GREATER_THAN_EQUAL:
#             self.eat(GREATER_THAN_EQUAL)

#         node = BinOp(left=node, op=token, right=self.expr())

#     return node
