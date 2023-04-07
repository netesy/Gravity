from gravity import lexer, parse, debug, interpret


code = """
function sum(a, b) {
    return a + b;
}

function main() {
    var x = 1;
    var y = 2;
    if (x < y) {
        x = sum(x, y);
    } else {
        x = sum(y, x);
    }
    print(x);
}
"""

tokens = lexer(code)
ast = parse(tokens)
interpret(ast)
