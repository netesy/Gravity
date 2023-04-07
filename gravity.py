# Define the syntax of the language
keywords = ["if", "else", "while", "for", "function"]
operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]

# Write a lexer
def lexer(code):
    tokens = []
    current_token = ""
    i = 0
    while i < len(code):
        char = code[i]
        if char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char.isdigit() or char.isalpha():
            current_token += char
        elif char in operators:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            raise Exception("Invalid character: " + char)
        i += 1
    if current_token:
        tokens.append(current_token)
    return tokens


# Write a parser
def parse(tokens):
    ast = []
    stack = []
    for token in tokens:
        if token == "(":
            stack.append(ast)
            ast = []
        elif token == ")":
            node = ast
            ast = stack.pop()
            ast.append(node)
        elif token in keywords:
            ast.append((token,))
        elif token in operators:
            ast.append(token)
        elif token.isdigit():
            ast.append(int(token))
        elif token.isalpha():
            ast.append(("var", token))
    return ast


def debug(code):
    tokens = lexer(code)
    print("Tokens:", tokens)
    ast = parse(tokens)
    print("AST:", ast)
    interpret(ast)


def interpret(ast):
    variables = {}
    i = 0
    while i < len(ast):
        node = ast[i]
        if isinstance(node, tuple):
            if node[0] == "function":
                name = node[1]
                args = node[2]
                code = node[3]
                variables[name] = (args, code)
        else:
            if node[0] == "print":
                print(eval_expression(node[1], variables))
            elif node[0] == "var":
                variables[node[1]] = eval_expression(node[2], variables)
            elif node[0] == "assign":
                variables[node[1]] = eval_expression(node[2], variables)
            elif node[0] == "return":
                return eval_expression(node[1], variables)
            elif node[0] == "if":
                condition = eval_expression(node[1], variables)
                if condition:
                    interpret(node[2])
                elif len(node) > 3 and node[3][0] == "else":
                    interpret(node[3][1])
            elif node[0] == "while":
                while eval_expression(node[1], variables):
                    interpret(node[2])
            elif node[0] == "for":
                variable = node[1]
                start = eval_expression(node[2], variables)
                end = eval_expression(node[3], variables)
                code = node[4]
                for value in range(start, end + 1):
                    variables[variable] = value
                    interpret(code)
        i += 1


def eval_expression(expr, variables):
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, str):
        if expr in variables:
            return variables[expr]
        else:
            raise Exception("Undefined variable: " + expr)
    elif expr[0] == "+":
        return eval_expression(expr[1], variables) + eval_expression(expr[2], variables)
    elif expr[0] == "-":
        return eval_expression(expr[1], variables) - eval_expression(expr[2], variables)
    elif expr[0] == "*":
        return eval_expression(expr[1], variables) * eval_expression(expr[2], variables)
    elif expr[0] == "/":
        return eval_expression(expr[1], variables) / eval_expression(expr[2], variables)
    elif expr[0] == "==":
        return eval_expression(expr[1], variables) == eval_expression(
            expr[2], variables
        )
    elif expr[0] == "!=":
        return eval_expression(expr[1], variables) != eval_expression(
            expr[2], variables
        )
    elif expr[0] == "<":
        return eval_expression(expr[1], variables) < eval_expression(expr[2], variables)
    elif expr[0] == ">":
        return eval_expression(expr[1], variables) > eval_expression(expr[2], variables)
    elif expr[0] == "<=":
        return eval_expression(expr[1], variables) <= eval_expression(
            expr[2], variables
        )
    elif expr[0] == ">=":
        return eval_expression(expr[1], variables) >= eval_expression(
            expr[2], variables
        )
    elif expr[0] == "and":
        return eval_expression(expr[1], variables) and eval_expression(
            expr[2], variables
        )
    elif expr[0] == "or":
        return eval_expression(expr[1], variables) or eval_expression(
            expr[2], variables
        )
    else:
        raise Exception("Invalid expression")


def run(code):
    tokens = lexer(code)
    ast = parse(tokens)
    debug(ast)
