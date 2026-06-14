import sys
from pathlib import Path

# Ensure src is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from main import *

def test_interpreter():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("((3 * 6 - 2 ^ (2 + 2)) / 10) % .15", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert round(result.value, 10) == .05
    
def test_interpreter_unary():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("-5 + +3", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == -2

def test_comparison_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("3 > 2 and 4 <= 5 or 6 == 7", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == True

def test_comparison_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("(3 < 2 nand 4 =< 5 nor (6 xnor 6) != 7) xor (not 6)", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == False
    
def test_error_301_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("4 + 4\n'hello' ^ 5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between String and Number"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 0
    assert error.pos_end.line == 1
    assert error.pos_end.column == 10
    
def test_string_ops():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('"abc" + (1 * "def" * 3) - 2', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, String)
    assert result.value == "abcdefdefd"
    
def test_error_301_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("'hello' / 5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between String and Number"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10
    
def test_error_301_inst_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("'hello' % 5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between String and Number"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10
    
def test_error_301_inst_4():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("5 - 'hello'", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between Number and String"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10

def test_error_301_inst_5():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("True + 1", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between Boolean and Number"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 7

def test_error_301_inst_6():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("None * 'a'", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between NoneType and String"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9

def test_error_301_inst_7():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("True < 'a'", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between Boolean and String"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9

def test_error_301_inst_8():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("var: {x = True}\nvar: {x -= 1}", "<test>")
    tokens, error = lexer.lex()
    
    # First token defines the variable
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None

    # Second token attempts an incompatible +=
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between Boolean and Number"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 0
    assert error.pos_end.line == 1
    assert error.pos_end.column == 11

def test_error_302_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("5 / 0", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 302
    assert error.error_name == "RuntimeError"
    assert error.details == "Division by zero"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 2
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    
def test_error_302_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("5 % (4 - 4)", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 302
    assert error.error_name == "RuntimeError"
    assert error.details == "Division by zero"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 2
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10
    
def test_error_303_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("'hello' * 5.5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 303
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of String and non-integer"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12
    
def test_error_303_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("'hello' - 4.5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 303
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of String and non-integer"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12
    
def test_error_303_inst_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("'hello' - 5.5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 303
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of String and number longer than length"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12

def test_error_303_inst_4():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("var:{x = 4.5}\n'hello' - x", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None

    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 303
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of String and non-integer"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 8
    assert error.pos_end.line == 1
    assert error.pos_end.column == 10

def test_variables():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("var: {x = 3}\nconst:{y = 2}\nx * y", "<test>")
    tokens, error = lexer.lex()
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None

    assert isinstance(result, Number)
    assert result.value == 6

def test_var_eqs():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("var: {x = 3}\nvar:{x += 2}\nvar: {x /= 3}\nvar:{x *= 2}\nvar:{x -= 6}\nvar: {x %= 7}\nx", "<test>")
    tokens, error = lexer.lex()
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None

    assert isinstance(result, Number)
    assert round(result.value, 3) == 4.333

def test_error_303_inst_5():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("var: {x = 'hi'}\nvar: {x -= 4.4}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None

    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is not None

    assert isinstance(error, Error)
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of String and number longer than length"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 8
    assert error.pos_end.line == 1
    assert error.pos_end.column == 13

def test_error_304_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("var: {x += 4.4}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 304
    assert error.error_name == "SymbolGetError"
    assert error.details == 'Variable "x" not defined'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 6
    assert error.pos_end.line == 0
    assert error.pos_end.column == 6

def test_error_304_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("x", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 304
    assert error.error_name == "SymbolGetError"
    assert error.details == 'Variable "x" not defined'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 0

def test_error_305_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("const: {x = 3}\nvar: {x = 5}", "<test>")
    tokens, error = lexer.lex()
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 305
    assert error.error_name == "ConstantError"
    assert error.details == 'Constant "x" already defined'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 6
    assert error.pos_end.line == 1
    assert error.pos_end.column == 6

def test_error_305_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("const: {x = 3}\nconst: {x = 5}", "<test>")
    tokens, error = lexer.lex()
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 305
    assert error.error_name == "ConstantError"
    assert error.details == 'Constant "x" already defined'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 8
    assert error.pos_end.line == 1
    assert error.pos_end.column == 8

def test_if_execution():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('if: { True} { var: {x = 5}}\nx', "<test>")
    tokens, error = lexer.lex()

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 5


def test_if_execution_else_and_elif_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('''if: {1 == 2} {var: {x = 5}}
elif: {2 == 2} { var: {x = 6}}
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()

    line = 0
    while line < len(tokens):
        if len(tokens[line]) == 1:
            line += 1
            continue
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        assert error is None
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
        line = node.pos_end.line + 1

    assert isinstance(result, Number)
    assert result.value == 6

def test_if_execution_else_and_elif_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('''if: {1 == 2} {var: {x = 5}}
elif: {2 != 2} { var: {x = 6}}
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()

    line = 0
    while line < len(tokens):
        if len(tokens[line]) == 1:
            line += 1
            continue
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        assert error is None
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
        line = node.pos_end.line + 1

    assert isinstance(result, Number)
    assert result.value == 7

def test_if_execution_else_and_elif_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('''if: {2 == 2} {var: {x = 5}}
elif: {2 == 2} { var: {x = 6}}
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()

    line = 0
    while line < len(tokens):
        if len(tokens[line]) == 1:
            line += 1
            continue
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        assert error is None
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
        line = node.pos_end.line + 1

    assert isinstance(result, Number)
    assert result.value == 5

def test_if_execution_else_and_elif_4():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('''if: {2 == 2} {
    var: {x = 5}
} elif: {2 == 2} { var: {x = 6}
} 
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()

    line = 0
    while line < len(tokens):
        if len(tokens[line]) == 1:
            line += 1
            continue
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        assert error is None
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
        line = node.pos_end.line + 1

    assert isinstance(result, Number)
    assert result.value == 5