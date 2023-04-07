# Define the syntax of the language
keywords = ["if", "else", "while", "for", "function"]
operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]
whitespace = [" ", "\t", "\n"]
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

# Write a lexer
def lexer(code):
    tokens = []
    current_token = ""
    i = 0
    while i < len(code):
        char = code[i]
        if char in whitespace:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in digits:
            current_token += char
        elif char in letters:
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
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "if":
            condition = tokens[i + 1]
            code = parse(tokens[i + 2 :])
            ast.append(("if", condition, code))
            i += len(code) + 2
        elif token == "else":
            code = parse(tokens[i + 1 :])
            ast.append(("else", code))
            break
        elif token == "while":
            condition = tokens[i + 1]
            code = parse(tokens[i + 2 :])
            ast.append(("while", condition, code))
            break
        elif token == "for":
            variable = tokens[i + 1]
            start = tokens[i + 3]
            end = tokens[i + 5]
            code = parse(tokens[i + 6 :])
            ast.append(("for", variable, start, end, code))
            break
        elif token == "function":
            name = tokens[i + 1]
            args = []
            j = i + 3
            while tokens[j] != ")":
                args.append(tokens[j])
                j += 1
            code = parse(tokens[j + 2 :])
            ast.append(("function", name, args, code))
            break
        else:
            ast.append(token)
        i += 1
    return ast


def interpret(ast):
    variables = {}
    for node in ast:
        if isinstance(node, tuple):
            if node[0] == "if":
                if eval_expression(node[1], variables):
                    interpret(node[2])
                elif node[0] == "else":
                    interpret(node[1])
            elif node[0] == "while":
                while eval_expression(node[1], variables):
                    interpret(node[2])
            elif node[0] == "for":
                variable = node[1]
                start = eval_expression(node[2], variables)
                end = eval_expression(node[3], variables)
                for value in range(start, end + 1):
                    variables[variable] = value
                    interpret(node[4])
            elif node[0] == "function":
                name = node[1]
                args = node[2]
                code = node[3]
                variables[name] = (args, code)
        else:
            if node in variables:
                interpret(variables[node])
            else:
                print(node)


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
