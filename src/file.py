from main import *
import sys

try:
    f = open(sys.argv[1], "r")
except:
    print(cs(f"[INTERNAL] Error 402: Could not open file requested file", "rgb(255, 100, 100)"))
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