from main import *
from stringcolor import *
import sys
import pytest

GlobalSymbolTable = SymbolTable()
green = "rgb(190, 230, 130)"
red = "rgb(255, 100, 100)"

ARGS = ['-t', '--test']

if not "--test" in sys.argv:
    if "-t" in sys.argv:
        print(cs("Running tests...", green))
        arg = ""
    else:
        arg = "-p no:terminal"
    if pytest.main([arg, "tests"]) > 0:
        print(cs("[INTERNAL] Error 401: Tests failed. Shell will not start.", "rgb(255, 100, 100)"))
        sys.exit(1)

if len(sys.argv) > 1:
    if sys.argv[1][0] != "-":
        for i in sys.argv[2:]:
            if i not in ARGS:
                print(cs(f'[INTERNAL] Error 403: Unknown system argument "{i}"', "rgb(255, 100, 100)"))
                sys.exit(1)
        try:
            f = open(sys.argv[1], "r")
        except:
            print(cs(f"[INTERNAL] Error 402: Could not open requested file", "rgb(255, 100, 100)"))
            sys.exit(1)

        text = f.read()
        lexer = Lexer(text, sys.argv[1])
        tokens, error = lexer.lex()
        GlobalSymbolTable = SymbolTable()

        if error:
            print(error)
            sys.exit(1)

        line = 0
        while line < len(tokens):
            try:
                if len(tokens[line]) == 1:
                    line += 1
                    continue
                parser = Parser(tokens[line], sys.argv[1], lexer)
                node, error = parser.parse()

                if error:
                    print(error)
                    sys.exit(1)

                # print(node)

                interpreter = Interpreter(node, lexer, sys.argv[1], GlobalSymbolTable)
                result, error = interpreter.visit(node)

                if error:
                    print(error)
                    sys.exit(1)

                # print(result)

                line = node.pos_end.line + 1
            except KeyboardInterrupt:
                print('\n')
                break
        sys.exit(1)

for i in sys.argv[1:]:
    if i not in ARGS:
        print(cs(f'[INTERNAL] Error 403: Unknown system argument "{i}"', "rgb(255, 100, 100)"))
        sys.exit(1)

print(cs(f"Piinappl x.x.x (stable @xx xx, xxxx) on {sys.platform}", green))
print(cs(f"Copyright (c) {2026} Adam Haspel. All rights reserved.", green))

text = ""
line = -1

while True:
    try:
        text += (input(">>> ")+"\n")

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
                    if result:
                        print(result.__repr__())
    except KeyboardInterrupt:
        print("")
        continue
    except EOFError:
        print("")
        break