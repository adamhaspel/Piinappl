from main import *
from stringcolor import *
import sys
import pytest

GlobalSymbolTable = SymbolTable()

green = "rgb(190, 230, 130)"
red = "rgb(255, 100, 100)"

print(cs(f"Piinappl x.x.x (stable @xxx xx, xxxx) on {sys.platform}", green))
print(cs(f"Copyright (c) {2026} Adam Haspel. All rights reserved.", green))
if not "--test" in sys.argv:
    if "-t" in sys.argv:
        print(cs("Running tests...", green))
        arg = ""
    else:
        arg = "-p no:terminal"
    if pytest.main([arg, "tests"]) > 0:
        print(cs("[INTERNAL] Error 401: Tests failed. Shell will not start.", "rgb(255, 100, 100)"))
        sys.exit(1)

text = ""
line = -1

while True:
    try:
        text += (input(">>> ")+"\n")
    except KeyboardInterrupt:
        print("")
        continue
    except EOFError:
        print("")
        break

    line += 1

    lexer = Lexer(text, "<shell>")
    tokens, error = lexer.lex()

    if error:
        if error.pos_start.line == line:
            print(error)
    else:
        tokens = tokens[line]
        nodes = []
        parser = Parser(tokens, "<shell>", lexer)
        node, error = parser.parse()

        if error:
            print(error)
            continue
        else:
            if node == None:
                continue
            interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
            result, error = interpreter.visit(node)

            if error:
                print(error)
            else:
                print(result)