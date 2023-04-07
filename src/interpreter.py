from .lexer import Lexer
from .parser_1 import Parser


class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast = parser.parse()
        return self._eval(ast)

    def _eval(self, node):
        if node.type == "PROGRAM":
            for statement in node.statements:
                self._eval(statement)
        elif node.type == "NUM":
            return node.value
        elif node.type == "BINOP":
            left_value = self._eval(node.left)
            right_value = self._eval(node.right)
            if node.op.type == "PLUS":
                return left_value + right_value
            elif node.op.type == "MINUS":
                return left_value - right_value
            elif node.op.type == "MULTIPLY":
                return left_value * right_value
            elif node.op.type == "DIVIDE":
                return left_value / right_value
            else:
                raise Exception("Invalid operator")
        elif node.type == "UNARYOP":
            operand_value = self._eval(node.operand)
            if node.op.type == "PLUS":
                return operand_value
            elif node.op.type == "MINUS":
                return -operand_value
            else:
                raise Exception("Invalid operator")
        elif node.type == "ASSIGNMENT":
            self.variables[node.variable.value] = self._eval(node.expression)
        elif node.type == "VARIABLE":
            if node.value not in self.variables:
                raise Exception("Variable not found: {}".format(node.value))
            return self.variables[node.value]
        elif node.type == "IF":
            condition_value = self._eval(node.condition)
            if condition_value:
                self._eval(node.if_block)
            elif node.else_block:
                self._eval(node.else_block)
        else:
            raise Exception("Invalid node type: {}".format(node.type))
