from main import *
from stringcolor import *
import sys

GlobalSymbolTable = SymbolTable()

print(cs(f"Piinappl x.x.x (stable @xxx xx, xxxx) on {sys.platform}", "rgb(200, 250, 220)"))
print(cs(f"Copyright (c) {2026} Adam Haspel. All rights reserved.", "rgb(200, 250, 220)"))

while True:
    try:
        text = input(">>> ")
    except KeyboardInterrupt:
        print("")
        continue
    except EOFError:
        print("")
        break

    lexer = Lexer(text, "<shell>")
    tokens, error = lexer.lex()

    if error:
        print(error)
    else:
        nodes = []
        for i in tokens:
            parser = Parser(i, "<shell>", lexer)
            node, error = parser.parse()

            if error:
                print(error)
                break
            nodes.append(node)
        if not error:
            for i in nodes:
                interpreter = Interpreter(i, lexer, "<shell>", GlobalSymbolTable)
                result, error = interpreter.visit(i)

                if error:
                    print(error)
                else:
                    print(result)