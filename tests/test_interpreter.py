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
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between Boolean and Number"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 0
    assert error.pos_end.line == 1
    assert error.pos_end.column == 11

def test_error_301_inst_9():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("[3] - True", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between List and Boolean"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9

def test_error_301_inst_10():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("[3] * True", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between List and Boolean"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9

def test_error_301_inst_10():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("[3] in True", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between List and Boolean"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10

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

def test_error_303_inst_6():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("['hello'] - .5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 303
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of List and non-integger"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 10
    assert error.pos_end.line == 0
    assert error.pos_end.column == 13

def test_error_303_inst_6():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer("['hello'] - 5.5", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 303
    assert error.error_name == "NumberError"
    assert error.details == "Invalid operation of List and number longer than length"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 10
    assert error.pos_end.line == 0
    assert error.pos_end.column == 14

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

def test_list():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('[3, None, "hi", True, 4 - 4, [1, "bye"]]', "<test>")
    tokens, error = lexer.lex()

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, List)
    assert [(t.__class__.__name__, t.value) for t in result.value[:-1]] == [
        ("Number", 3),
        ("NoneType", None),
        ("String", "hi"),
        ("Boolean", True),
        ("Number", 0),
    ]
    assert [(t.__class__.__name__, t.value) for t in result.value[-1].value] == [
        ("Number", 1),
        ("String", "bye")
    ]

def test_list_ops():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('[1, 2, 3, "a", "b", None] + ([4, 5, 6] * 2) - -2 - 2', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert [(t.__class__.__name__, t.value) for t in result.value] == [
        ("Number", 3),
        ("String", "a"),
        ("String", "b"),
        ("NoneType", None),
        ("Number", 4),
        ("Number", 5),
        ("Number", 6),
        ("Number", 4),
    ]

def test_in_list():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('1 in ([1, 2, 3, "a", "b", None] + ([4, 5, 6] * 2) - -2 - 2)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == 0

def test_in_string_and_num():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('1 in "1" and 12 in 3123 and "hi" in "hibyewhy" and True in "TrueFalse"', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == 1

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

def test_func_call_no_args():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {greet()} { return: { 5 } }\ngreet()', "<test>")
    tokens, error = lexer.lex()
    
    # Define function
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 5


def test_func_call_1_arg():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {add_ten(x)} { return: { x + 10 } }\nadd_ten(5)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 15

def test_func_return_in_if():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {add_ten(x)} { if: {1 == 1} {return: { x + 10 } }}\nadd_ten(5)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 15


def test_func_call_multiple_args():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {add(x, y)} { return: { x + y } }\nadd(3, 7)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 10



def test_cfunc_constant_function():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('cfunc: {multiply(x, y)} { return: { x * y } }\nmultiply(4, 5)\nvar: {multiply = 4}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 20

    parser = Parser(tokens[2], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is not None



def test_func_nested():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {double(x)} { return: { x * 2 } }\nfunc: {quad(x)} { return: { double(double(x)) } }\nquad(3)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[2], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 12



def test_return_multiple_values():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {get_coords()} { return: { 1, 2, 3 } }\nget_coords()', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, List)
    assert [(v.__class__.__name__, v.value) for v in result.value] == [
        ("Number", 1),
        ("Number", 2),
        ("Number", 3)
    ]


def test_error_304_inst_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('undefined_func(5)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 304
    assert error.error_name == "SymbolGetError"
    assert "undefined_func" in error.details
    assert "not defined" in error.details


def test_error_306_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {add(x, y)} { x + y }\nadd(5)', "<test>")
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
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert "takes 2 arguments" in error.details
    assert "1 was given" in error.details


def test_error_306_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {add(x, y)} { x + y }\nadd(1, 2, 3)', "<test>")
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
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert "takes 2 arguments" in error.details
    assert "3 were given" in error.details


def test_error_306_inst_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('var: {x = 5}\nundefined_func()', "<test>")
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
    assert error.error_code == 304
    assert error.error_name == "SymbolGetError"
    assert "undefined_func" in error.details


def test_error_307():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('return: { 5 }', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 307
    assert error.error_name == "ReturnError"
    assert "must be used in a function" in error.details

def test_unpack():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('unpack: {x, y = [1, 2]}\nx + y', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 3


def test_unpack_more():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('unpack: {a, b, c = [10, 20, 30]}\nb', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 20


def test_unpack_from_function_return():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {get_pair()} { return: { [5, 10] } }\nunpack: {p1, p2 = get_pair()}\np1', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[2], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 5


def test_error_308_inst_1():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('unpack: {x = [1, 2]}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 308
    assert error.error_name == "UnpackError"
    assert "Cannot unpack 1 item" in error.details


def test_error_308_inst_2():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('unpack: {x, y = 5}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 308
    assert error.error_name == "UnpackError"
    assert "Cannot unpack non-iterable" in error.details
    assert "Number" in error.details


def test_error_308_inst_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('unpack: {x, y, z = [1, 2]}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 308
    assert error.error_name == "UnpackError"
    assert "Cannot unpack 2 values into 3 objects" in error.details


def test_error_308_inst_4():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('unpack: {x, y = [1, 2, 3]}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 308
    assert error.error_name == "UnpackError"
    assert "Cannot unpack 3 values into 2 objects" in error.details


def test_error_305_inst_3():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('cfunc: {x()} { 5 }\nvar: {x = 10}', "<test>")
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
    assert error.error_code == 305
    assert error.error_name == "ConstantError"
    assert "already defined" in error.details


#####################
# INTEGRATION TESTS #
#####################

def test_integration_func_return_unpack():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {get_pair()} { return: { [100, 200] } }\nunpack: {a, b = get_pair()}\na + b', "<test>")
    tokens, error = lexer.lex()
    
    # Define function
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[2], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 300


def test_integration_multiple_functions():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('func: {double(x)} { return: { x * 2 } }\nfunc: {triple(x)} { return: { x * 3 } }\ndouble(5) + triple(5)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    
    parser = Parser(tokens[2], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 25

def test_print(capsys):
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('print("hi" + 9)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    captured = capsys.readouterr().out
    assert captured[:-1] == "hi9"

def test_until():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('until(5)\nuntil(2, 5)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    assert isinstance(_, List)
    assert [(t.__class__.__name__, t.value) for t in _.value] == [
        ("Number", 0),
        ("Number", 1),
        ("Number", 2),
        ("Number", 3),
        ("Number", 4)
    ]
    
    
    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is None
    assert [(t.__class__.__name__, t.value) for t in _.value] == [
        ("Number", 2),
        ("Number", 3),
        ("Number", 4)
    ]
    
def test_error_306_inst_4():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('until(5.5)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_start.line == 0
    assert error.pos_end.column == 9
    assert "takes whole integer arguments" in error.details

def test_error_306_inst_4():
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('until(1,2,3)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_start.line == 0
    assert error.pos_end.column == 11
    assert "until takes 2 arguments; 3 were given instead" in error.details
    

def test_reprs(capsys):
    GlobalSymbolTable = SymbolTable()
    lexer = Lexer('print(print)\nprint(True)\nprint(None)', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    captured = capsys.readouterr().out
    assert captured[:-1] == "<Function print>"

    parser = Parser(tokens[1], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    captured = capsys.readouterr().out
    assert captured[:-1] == "True"

    parser = Parser(tokens[2], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    captured = capsys.readouterr().out
    assert captured[:-1] == "None"