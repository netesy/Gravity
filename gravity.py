from src.interpreter import Interpreter


def run(code):
    interpreter = Interpreter()
    result = interpreter.interpret("x = 2 + 3 * 4\ny = -x\nif y < 0: print('negative')")
    print(result)
