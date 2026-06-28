import sys
from pathlib import Path

# Ensure src is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from main import *

def test_interpreter():
    lexer = Lexer("((3 * 6 - 2 ^ (2 + 2)) / 10) % .15", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert round(result.value, 10) == .05
    
def test_interpreter_unary():
    lexer = Lexer("-5 + +3", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == -2

def test_comparison_1():
    lexer = Lexer("3 > 2 and 4 <= 5 or 6 == 7", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == True
    
def test_number_built_in():
    lexer = Lexer("Number('2.3') + 4", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 6.3
    
def test_string_built_in():
    lexer = Lexer("String([4, 3]) + 'hi'", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, String)
    assert result.value == '[4, 3]hi'
    
def test_nonetype_built_in():
    lexer = Lexer("NoneType()", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, NoneType)
    
def test_boolean_built_in():
    lexer = Lexer("Boolean([4, 3]) and Boolean(None)", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert not result.value
    
def test_list_built_in():
    lexer = Lexer("List({4:2, 1: 3}) + [6]", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert [(t.__class__.__name__, t.value) for t in result.value] == [
        ("Number", 4),
        ("Number", 1),
        ("Number", 6)
    ]
    
def test_dictionary_built_in():
    lexer = Lexer("Dictionary({4:2, 1: 3}) + {6: 5}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Dictionary)
    assert [(t.__class__.__name__, t.value, result.value[t].value) for t in result.value] == [
        ("Number", 4,2),
        ("Number", 1,3),
        ("Number", 6,5)
    ]
    
def test_type_built_in():
    lexer = Lexer("Type(4)('7.8')", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 7.8

def test_comparison_1():
    lexer = Lexer("3 > 2 and 4 <= 5 or 6 == 7", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == True

def test_comparison_2():
    lexer = Lexer("(3 < 2 nand 4 =< 5 nor (6 xnor 6) != 7) xor (not 6)", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == False
    
def test_error_301_inst_1():
    lexer = Lexer("4 + 4\n'hello' ^ 5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('"abc" + (1 * "def" * 3) - 2', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, String)
    assert result.value == "abcdefdefd"
    
def test_error_301_inst_3():
    lexer = Lexer("'hello' % 5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("5 - 'hello'", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("True + 1", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("None * 'a'", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("True < 'a'", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("var: {x = True}\nvar: {x -= 1}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("[3] - True", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("[3] * True", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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

def test_error_301_inst_11():
    lexer = Lexer("[3] in True", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    
def test_is_eq():
    lexer = Lexer("4 is 3", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert not result.value
    
def test_is_type():
    lexer = Lexer("4 is Number", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value
    
def test_is_instance():
    lexer = Lexer("class: {Hi()} {}\nvar: {hi = Hi()}\n[hi is Hi, hi is Number, Hi is Hi]", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert result.value[0].value
    assert not result.value[1].value
    assert result.value[2].value
    
def test_is_super():
    lexer = Lexer("class: {Hi()} {}\nclass: {Bye(Hi)} {}\nvar: {bye = Bye()}\n[bye is Hi, bye is Bye, Hi() is bye]", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert result.value[0].value
    assert result.value[1].value
    assert not result.value[2].value

def test_error_309_inst_5():
    lexer = Lexer("{ 1: 1} - 2", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.details == "Item not in dictionary index"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 10
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10

def test_error_301_inst_12():
    lexer = Lexer("{} * 2", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between Dictionary and Number"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 5

def test_string_div():
    lexer = Lexer("'hellomynameisbob' / 3", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, String)
    assert result.value == 'hlymsb'

def test_list_div():
    lexer = Lexer("[1, 2, 3, 4, 5] / -2", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert result.value[0].value == 5
    assert result.value[1].value == 3
    assert result.value[2].value == 1

def test_error_301_inst_2():
    lexer = Lexer("[] % 2", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 301
    assert error.error_name == "IncompatibleOpError"
    assert error.details == "Unsupported operation between List and Number"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 5

def test_error_302_inst_1():
    lexer = Lexer("5 / 0", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("5 % (4 - 4)", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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

def test_error_302_inst_3():
    lexer = Lexer("[3] / 0", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 6

def test_error_302_inst_4():
    lexer = Lexer("for: {i [3, 4, 5] step 0} {}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    assert error.pos_start.column == 23
    assert error.pos_end.line == 0
    assert error.pos_end.column == 23

def test_error_310_inst_1():
    lexer = Lexer("loop: {'hi'} {}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 310
    assert error.error_name == "LoopError"
    assert error.details == "Loop only takes number loops"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 7
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10

def test_error_310_inst_2():
    lexer = Lexer("loop: {4.44} {}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 310
    assert error.error_name == "LoopError"
    assert error.details == "Loop only takes integer loops"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 7
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10

def test_error_310_inst_3():
    lexer = Lexer("for: {i [] step True} {}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 310
    assert error.error_name == "LoopError"
    assert error.details == "For only takes number steps"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 16
    assert error.pos_end.line == 0
    assert error.pos_end.column == 19

def test_error_310_inst_4():
    lexer = Lexer("for: {i [] step 4.33} {}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 310
    assert error.error_name == "LoopError"
    assert error.details == "For only takes integer steps"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 16
    assert error.pos_end.line == 0
    assert error.pos_end.column == 19

def test_error_310_inst_5():
    lexer = Lexer("for: {i 33} {}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 310
    assert error.error_name == "LoopError"
    assert error.details == "For only takes string, dictionary and list loops"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9
    
def test_error_303_inst_1():
    lexer = Lexer("'hello' * 5.5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("'hello' - 4.5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("'hello' - 5.5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("['hello'] - .5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("['hello'] - 5.5", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("var:{x = 4.5}\n'hello' - x", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("var: {x = 3}\nconst:{y = 2}\nx * y", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None

    assert isinstance(result, Number)
    assert result.value == 6

def test_class():
    lexer = Lexer('''class: {AddPlus()} {
    func: {_init(self, num)} {
        attr: {self.num = num}
    }
    func: {exec(self, num)} {
        return: {self.num + num}
    }
}
const: {addplus = AddPlus(4)}
attr: {addplus.num = 900}
addplus.exec(8).length + addplus.exec(27)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None
        line = node.pos_end.line + 1

    assert isinstance(result, Number)
    assert result.value == 930

def test_class_super():
    lexer = Lexer('''class: {AddPlus()} {
    func: {_init(self, num)} {
        attr: {self.num = num}
    }
    func: {exec(self, num)} {
        return: {self.num + num}
    }
}
class: {AddMinus(AddPlus)} {
    func: {exec(self, num)} {
        return: {self.num - num}
    }
}
const: {addplus = AddMinus(4)}
attr: {addplus.num = 900}
addplus.exec(8).length + addplus.exec(27)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None
        line = node.pos_end.line + 1

    assert isinstance(result, Number)
    assert result.value == 876

def test_class_super_attr():
    lexer = Lexer('''class: {AddPlus()} {
    func: {_init(self, num)} {
        attr: {self.num = num}
    }
    func: {exec(self, num)} {
        return: {self.num + num}
    }
}
class: {AddMinus(AddPlus)} {
    func: {exec(self, num)} {
        return: {self.num - num}
    }
}
class: {AddTimes(AddMinus)} {
    func: {exec(self, num)} {
        return: {self.num * num}
    }
}
AddTimes(4).super(3).super
AddTimes(4).super(3).super(9).exec(4)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    res = []
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None
        res.append(result)
        line = node.pos_end.line + 1

    assert isinstance(res[3], ClassObject)
    assert res[3].name == "AddPlus"
    assert isinstance(res[4], Number)
    assert res[4].value == 13

def test_error_304_inst_4():
    lexer = Lexer('''class: {AddMinus(AddPlus)} {
    func: {exec(self, num)} {
        return: {self.num - num}
    }
}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 304
    assert error.error_name == "SymbolGetError"
    assert error.details == 'Variable "AddPlus" not defined'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 17
    assert error.pos_end.line == 0
    assert error.pos_end.column == 23

def test_error_313_inst_1():
    lexer = Lexer('''var: {AddPlus = 4}
class: {AddMinus(AddPlus)} {
    func: {exec(self, num)} {
        return: {self.num - num}
    }
}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 313
    assert error.error_name == "ClassError"
    assert error.details == 'Class super must be a class object'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 17
    assert error.pos_end.line == 1
    assert error.pos_end.column == 23

def test_error_313_inst_2():
    lexer = Lexer('''class: {AddMinus()} {
    func: {exec(num)} {
        return: {self.num - num}
    }
}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 313
    assert error.error_name == "ClassError"
    assert error.details == 'First argument must be self'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 16
    assert error.pos_end.line == 1
    assert error.pos_end.column == 18

def test_error_313_inst_3():
    lexer = Lexer('''class: {AddMinus()} {
    func: {exec()} {
        return: {self.num - num}
    }
}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 313
    assert error.error_name == "ClassError"
    assert error.details == 'First argument must be self'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 11
    assert error.pos_end.line == 1
    assert error.pos_end.column == 14

def test_error_305_inst_4():
    lexer = Lexer('''const: {AddMinus = 4}
class: {AddMinus()} {}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 305
    assert error.error_name == "ConstantError"
    assert error.details == 'Constant "AddMinus" already defined'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 8
    assert error.pos_end.line == 1
    assert error.pos_end.column == 15

def test_error_305_inst_5():
    lexer = Lexer('''const: {AddMinus = 4}
cclass: {AddMinus()} {}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 305
    assert error.error_name == "ConstantError"
    assert error.details == 'Constant "AddMinus" already defined'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 9
    assert error.pos_end.line == 1
    assert error.pos_end.column == 16

def test_error_312_inst_6():
    lexer = Lexer('''class: {AddMinus()} {
    func: {_init(self, num)} {
        return: {self.num - num}
    }
}
AddMinus()''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Function _init takes 2 arguments; 1 was given instead'
    assert error.pos_start.line == 5
    assert error.pos_start.column == 0
    assert error.pos_end.line == 5
    assert error.pos_end.column == 9
    
def test_arg_cond():
    lexer = Lexer('''func: {yay(a is Number)} {
        None
    }
yay(4)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is None
    
def test_arg_preexisiting_override():
    lexer = Lexer('''func: {yay(a, b=4)} {
        return: {a / b}
    }
yay(4,2)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is None
    assert isinstance(result, Number)
    assert result.value == 2
    
def test_arg_preexisiting():
    lexer = Lexer('''func: {yay(a, b=4)} {
        return: {a / b}
    }
yay(4)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is None
    assert isinstance(result, Number)
    assert result.value == 1

def test_error_306_inst_6():
    lexer = Lexer('''func: {yay(a is Number)} {
        None
    }
yay('4')''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Argument does not satisfy condition: a is Number'
    assert error.pos_start.line == 3
    assert error.pos_start.column == 4
    assert error.pos_end.line == 3
    assert error.pos_end.column == 6
    
def test_error_306_inst_7():
    lexer = Lexer('''func: {yay(a > 6)} {
        None
    }
yay(4)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Argument does not satisfy condition: a > 6'
    assert error.pos_start.line == 3
    assert error.pos_start.column == 4
    assert error.pos_end.line == 3
    assert error.pos_end.column == 4
    
def test_error_306_inst_8():
    lexer = Lexer('''func: {yay(a > 6)} {
        None
    }
yay('whee')''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Argument does not satisfy condition: a > 6'
    assert error.pos_start.line == 3
    assert error.pos_start.column == 4
    assert error.pos_end.line == 3
    assert error.pos_end.column == 9
    
def test_error_306_inst_9():
    lexer = Lexer('''func: {yay(a, b = 4)} {
        None
    }
yay()''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Function yay takes 1 - 2 arguments; 0 were given instead'
    assert error.pos_start.line == 3
    assert error.pos_start.column == 0
    assert error.pos_end.line == 3
    assert error.pos_end.column == 4
    
def test_error_306_inst_10():
    lexer = Lexer('''func: {yay(a, b = 4)} {
        None
    }
yay(1, 2, 3)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Function yay takes 1 - 2 arguments; 3 were given instead'
    assert error.pos_start.line == 3
    assert error.pos_start.column == 0
    assert error.pos_end.line == 3
    assert error.pos_end.column == 11
    
def test_error_306_inst_11():
    lexer = Lexer('''ClassInstance()''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Object ClassInstance is not callable'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 14
    
def test_error_306_inst_12():
    lexer = Lexer('''NoneType(3)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Class NoneType takes 0 arguments; 1 was given instead'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 10
    
def test_error_306_inst_13():
    lexer = Lexer('''String()''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Class String takes 1 argument; 0 were given instead'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 7
    
def test_error_306_inst_14():
    lexer = Lexer('''Number('4.4.4')''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Class Number cannot convert selected value'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 14
    
def test_error_306_inst_15():
    lexer = Lexer('''func: {h(a, b, c)} {
}
h(4, c = 8, 9)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Positional argument given after keyword argument'
    assert error.pos_start.line == 2
    assert error.pos_start.column == 12
    assert error.pos_end.line == 2
    assert error.pos_end.column == 12
    
def test_error_306_inst_16():
    lexer = Lexer('''func: {h(a, b, c=None)} {
}
h(4, d = 8)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 306
    assert error.error_name == "CallError"
    assert error.details == 'Keyword argument not in function'
    assert error.pos_start.line == 2
    assert error.pos_start.column == 5
    assert error.pos_end.line == 2
    assert error.pos_end.column == 9
    
def test_kwargs():
    lexer = Lexer('''func: {yay(a, b)} {
        return: {a / b}
    }
yay(b = 4, a = 3)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is None
    assert isinstance(result, Number)
    assert result.value == .75
    
def test_kwargs_and_pos():
    lexer = Lexer('''func: {yay(a, b)} {
        return: {a / b}
    }
yay(8, b = 4)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is None
    assert isinstance(result, Number)
    assert result.value == 2
    
def test_kwargs_canceling():
    lexer = Lexer('''func: {yay(a, b)} {
        return: {a / b}
    }
yay(8, b = 4, b = 6)''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1

    assert error is None
    assert isinstance(result, Number)
    assert result.value == (8/6)

def test_empty_multi_line():
    lexer = Lexer('''if: {True} {} elif: {False} {} else: {}
for: {i []} {}
loop: {2} {}
while: {False} {}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None

def test_var_eqs():
    lexer = Lexer("var: {x = 3}\nvar:{x += 2}\nvar: {x /= 3}\nvar:{x *= 2}\nvar:{x -= 6}\nvar: {x %= 7}\nx", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

        assert error is None

    assert isinstance(result, Number)
    assert round(result.value, 3) == 4.333

def test_error_303_inst_5():
    lexer = Lexer("var: {x = 'hi'}\nvar: {x -= 4.4}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("var: {x += 4.4}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("x", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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

def test_error_312_inst_1():
    lexer = Lexer("'hi'.'bye'", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 312
    assert error.error_name == "AttributeError"
    assert error.details == 'Attribute must be identifier'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 5
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9
    
def test_if_attributes():
    lexer = Lexer("if: {print.boogoo} {5}\nif: {4.length} {6}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    res = []
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        res.append(result)
        
        assert error is None
        
    assert res[0] is None
    assert isinstance(res[1], Number)
    assert res[1].value == 6
    
def test_error_312_inst_7():
    lexer = Lexer("if: {print.notreal + 1} {5}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 312
    assert error.error_name == "AttributeError"
    assert error.details == 'Function print does not have attribute "notreal"'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 11
    assert error.pos_end.line == 0
    assert error.pos_end.column == 17

def test_error_312_inst_2():
    lexer = Lexer("print.notreal", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 312
    assert error.error_name == "AttributeError"
    assert error.details == 'Function print does not have attribute "notreal"'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 6
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12

def test_error_312_inst_3():
    lexer = Lexer("attr: {a = 6}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 312
    assert error.error_name == "AttributeError"
    assert error.details == 'Not a valid attribute'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 7
    assert error.pos_end.line == 0
    assert error.pos_end.column == 7

def test_error_312_inst_4():
    lexer = Lexer("attr: {5.length = 6}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()

        assert error is None
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 312
    assert error.error_name == "AttributeError"
    assert error.details == 'Cannot edit attributes of type Number'
    assert error.pos_start.line == 0
    assert error.pos_start.column == 7
    assert error.pos_end.line == 0
    assert error.pos_end.column == 7

def test_error_312_inst_5():
    lexer = Lexer("class: {H()} {}\nattr: {H().l += 6}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()

        assert error is None
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)

    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 312
    assert error.error_name == "AttributeError"
    assert error.details == 'Object H does not have attribute "l"'
    assert error.pos_start.line == 1
    assert error.pos_start.column == 11
    assert error.pos_end.line == 1
    assert error.pos_end.column == 11

def test_error_305_inst_1():
    lexer = Lexer("const: {x = 3}\nvar: {x = 5}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer("const: {x = 3}\nconst: {x = 5}", "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('if: { True} { var: {x = 5}}\nx', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 5

def test_list():
    lexer = Lexer('[3, None, "hi", True, 4 - 4, [1, "bye"]]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

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

def test_dict():
    lexer = Lexer('{3: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Dictionary)
    assert [(t.__class__.__name__, t.value, result.value[t].__class__.__name__, str(result.value[t].value)) for t in result.value] == [
        ("String", 'hi', "Boolean", "True"),
        ("Number", 3, "String", "not none"),
        ("Number", 0, "List", "[1, 'bye']"),
    ]

def test_dict_ops():
    lexer = Lexer('{3: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]} - 0 + { True: 1}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Dictionary)
    assert [(t.__class__.__name__, t.value, result.value[t].__class__.__name__, str(result.value[t].value)) for t in result.value] == [
        ("String", "hi", "Boolean", "True"),
        ("Number", 3, "String", "not none"),
        ("Boolean", True, "Number", "1"),
    ]

def test_dict_eq():
    lexer = Lexer('{3: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]} == {3: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]}\n{4: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]} == {3: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    res = []

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        res.append(result)
        assert error is None

    assert isinstance(res[0], Boolean)
    assert res[0].value == True
    assert isinstance(res[1], Boolean)
    assert res[1].value == False

def test_list_eq():
    lexer = Lexer('[4, 5, [6, 7]] == [4, 5, [6, 8]]\n[4, 5, [6, 7]] == [4, 5, [6, 7]]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    res = []

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        res.append(result)
        assert error is None

    assert isinstance(res[0], Boolean)
    assert res[0].value == False
    assert isinstance(res[1], Boolean)
    assert res[1].value == True

def test_list_comp():
    lexer = Lexer('[4, 5, [6, 7]] < [1] \n[4, 5, [6, 7]] <= [4, 5, [6, 7]]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    res = []

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        res.append(result)
        assert error is None

    assert isinstance(res[0], Boolean)
    assert res[0].value == False
    assert isinstance(res[1], Boolean)
    assert res[1].value == True

def test_dict_comp():
    lexer = Lexer('{3: None, "hi": True, 3:"not none"} > { } \n{1: 1} <= {}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    res = []

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        res.append(result)
        assert error is None

    assert isinstance(res[0], Boolean)
    assert res[0].value == True
    assert isinstance(res[1], Boolean)
    assert res[1].value == False

def test_dict_to_list_comp():
    lexer = Lexer('{3: None, "hi": True, 3:"not none"} > [] \n[1, 1] <= { }', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

    res = []

    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        res.append(result)
        assert error is None

    assert isinstance(res[0], Boolean)
    assert res[0].value == True
    assert isinstance(res[1], Boolean)
    assert res[1].value == False

def test_list_ops():
    lexer = Lexer('[1, 2, 3, "a", "b", None] + ([4, 5, 6] * 2) - -2 - 2', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('1 in ([1, 2, 3, "a", "b", None] + ([4, 5, 6] * 2) - -2 - 2)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == 0

def test_in_dict():
    lexer = Lexer('True in {3: None, "hi": True, 3:"not none", 4 - 4: [1, "bye"]} - 0 + { True: 1}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == True

def test_in_string_and_num():
    lexer = Lexer('1 in "1" and 12 in 3123 and "hi" in "hibyewhy" and True in "TrueFalse"', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value == 1

def test_attr_length():
    lexer = Lexer('"hellomate".length', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 9

def test_attr_digits():
    lexer = Lexer('4.4.digits', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 2

def test_attr_keys():
    lexer = Lexer('{2: 3, 4: 1}.keys', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert [(t.__class__.__name__, t.value) for t in result.value] == [
        ("Number", 2),
        ("Number", 4)
    ]

def test_attr_index_dict():
    lexer = Lexer('{2: 3, 6: "hi", 4: 1}.index("hi")', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 6

def test_attr_index_list():
    lexer = Lexer('[2, 3, 6, "hi", 4, 1].index("hi")', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 3

def test_attr_values():
    lexer = Lexer('{2: 3, 4: 1}.values', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is None
    assert isinstance(result, List)
    assert [(t.__class__.__name__, t.value) for t in result.value] == [
        ("Number", 3),
        ("Number", 1)
    ]

def test_if_execution_else_and_elif_1():
    lexer = Lexer('''if: {1 == 2} {var: {x = 5}}
elif: {2 == 2} { var: {x = 6}}
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

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
    lexer = Lexer('''if: {1 == 2} {var: {x = 5}}
elif: {2 != 2} { var: {x = 6}}
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

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
    lexer = Lexer('''if: {2 == 2} {var: {x = 5}}
elif: {2 == 2} { var: {x = 6}}
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

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
    lexer = Lexer('''if: {2 == 2} {
    var: {x = 5}
} elif: {2 == 2} { var: {x = 6}
} 
else: {var: {x = 7}}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)

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
    lexer = Lexer('func: {greet()} { return: { 5 } }\ngreet()', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert error is None
    assert isinstance(result, Number)
    assert result.value == 5


def test_func_call_1_arg():
    lexer = Lexer('func: {add_ten(x)} { return: { x + 10 } }\nadd_ten(5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 15

def test_func_return_in_if():
    lexer = Lexer('func: {add_ten(x)} { if: {1 == 1} {return: { x + 10 } }}\nadd_ten(5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 15


def test_func_call_multiple_args():
    lexer = Lexer('func: {add(x, y)} { return: { x + y } }\nadd(3, 7)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 10

def test_loop():
    lexer = Lexer('var: {x = 4}\nloop: {x - 2} {var: {x += 2}}\nx', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 8

def test_while():
    lexer = Lexer('var: {x = 2}\nwhile: {x < 10} {var: {x += 1}}\nx', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 10

def test_for():
    lexer = Lexer('var: {x = 0}\nfor: {i [1, None, 2, None, 3, None, 4, None, 5] step 2} {var: {x += i}}\nx', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    for i in tokens:
        parser = Parser(i, "<shell>", lexer)
        node, error = parser.parse()
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        assert error is None
    
    assert isinstance(result, Number)
    assert result.value == 15

def test_continue():
    lexer = Lexer('''var: {x = 0}
for: {i [1, 2, 3, 4, 5]} {
    if: {i == 3} {
        continue
    }
    var: {x += i}
}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    assert result.value == 12

def test_break():
    lexer = Lexer('''var: {x = 0}
for: {i [1, 2, 3, 4, 5]} {
    if: {i == 4} {
        break
    }
    var: {x += i}
}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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

def test_restart():
    lexer = Lexer('''var: {x = 0}
for: {i [1, 2, 3, 4, 5]} {
    var: {x += i}
    if: {x <= 20} {
        restart
    }
}
x''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    assert result.value == 35

def test_error_311():
    lexer = Lexer('break', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()

    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert isinstance(error, Error)
    assert error.error_code == 311
    assert error.error_name == "LoopKeyError"
    assert "must be used in a loop" in error.details
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4

def test_cfunc_constant_function():
    lexer = Lexer('cfunc: {multiply(x, y)} { return: { x * y } }\nmultiply(4, 5)\nvar: {multiply = 4}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('func: {double(x)} { return: { x * 2 } }\nfunc: {quad(x)} { return: { double(double(x)) } }\nquad(3)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('func: {get_coords()} { return: { 1, 2, 3 } }\nget_coords()', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('undefined_func(5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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

def test_list_call():
    lexer = Lexer('["try", [1, 4, 5], None][1][2]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    assert isinstance(result, Number)
    assert result.value == 5

def test_dict_call():
    lexer = Lexer('{ 1: {2 :4, 6: 9}, None: 7}[1][2]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    assert isinstance(result, Number)
    assert result.value == 4

def test_error_309_inst_7():
    lexer = Lexer('{ 1: {2 :4, 6: 9}, None: 7}[47.7][2]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 28
    assert error.pos_end.column == 31
    assert "Item not in dictionary index" in error.details

def test_error_309_inst_8():
    lexer = Lexer('{ 1: {2 :4, 6: 9}, None: 7}.index(27)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 34
    assert error.pos_end.column == 35
    assert "Item not in dictionary values" in error.details

def test_error_309_inst_9():
    lexer = Lexer('[1, 2, 3, 4, 5].index(True)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 22
    assert error.pos_end.column == 25
    assert "Item not in list" in error.details

def test_error_309_inst_1():
    lexer = Lexer('1[1]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 0
    assert error.pos_end.column == 0
    assert "Cannot index type" in error.details
    assert "Number" in error.details

def test_error_309_inst_2():
    lexer = Lexer('""[None]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 3
    assert error.pos_end.column == 6
    assert "Cannot index with type" in error.details
    assert "NoneType" in error.details

def test_error_309_inst_3():
    lexer = Lexer('[1][1.1]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 4
    assert error.pos_end.column == 6
    assert "Cannot index with non-integer" in error.details

def test_error_309_inst_4():
    lexer = Lexer('[1][24]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 4
    assert error.pos_end.column == 5
    assert "Out of index range" in error.details

def test_error_309_inst_6():
    lexer = Lexer('[1][-24]', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)
    
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 309
    assert error.error_name == "IndexError"
    assert error.pos_start.column == 4
    assert error.pos_end.column == 6
    assert "Out of index range" in error.details

def test_error_306_inst_1():
    lexer = Lexer('func: {add(x, y)} { x + y }\nadd(5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('func: {add(x, y)} { x + y }\nadd(1, 2, 3)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('var: {x = 5}\nundefined_func()', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('return: { 5 }', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('unpack: {x, y = [1, 2]}\nx + y', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('unpack: {a, b, c = [10, 20, 30]}\nb', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('func: {get_pair()} { return: { [5, 10] } }\nunpack: {p1, p2 = get_pair()}\np1', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('unpack: {x = [1, 2]}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('unpack: {x, y = 5}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('unpack: {x, y, z = [1, 2]}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('unpack: {x, y = [1, 2, 3]}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('cfunc: {x()} { 5 }\nvar: {x = 10}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('func: {get_pair()} { return: { [100, 200] } }\nunpack: {a, b = get_pair()}\na + b', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('func: {double(x)} { return: { x * 2 } }\nfunc: {triple(x)} { return: { x * 3 } }\ndouble(5) + triple(5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('print("hi" + 9)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    result, error = interpreter.visit(node)

    assert error is None
    captured = capsys.readouterr().out
    assert captured[:-1] == "hi9"

def test_until():
    lexer = Lexer('until(5)\nuntil(2, 5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('until(5.5)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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

def test_error_306_inst_5():
    lexer = Lexer('until(1,2,3)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    lexer = Lexer('print(print)\nprint(True)\nprint(None)', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
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
    
def test_try_but_1(capsys):
    lexer = Lexer('''try: {5}
but: {AttributeError} {print(5)}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == "6\n9"
    
def test_try_but_2(capsys):
    lexer = Lexer('''try: {5/0}
but: {AttributeError} {print(5)}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == "9"
    
def test_try_but_3(capsys):
    lexer = Lexer('''try: {5/0}
but: {RuntimeError} {print(5)}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == "5\n9"
    
def test_try_but_4(capsys):
    lexer = Lexer('''try: {5/0}
but: {RuntimeError as e} {print(e)}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == f"<ClassInstance RuntimeError at 0x{GlobalSymbolTable.symbols.get('e').id}>\n9"
    
def test_try_but_5(capsys):
    lexer = Lexer('''try: {print.abut}
but: {Error as e} {print(e)}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == f"<ClassInstance AttributeError at 0x{GlobalSymbolTable.symbols.get('e').id}>\n9"
    
def test_try_but_6(capsys):
    lexer = Lexer('''var: {x = Error}
                  try: {print.abut}
but: {x as e} {print(e)}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == f"<ClassInstance AttributeError at 0x{GlobalSymbolTable.symbols.get('e').id}>\n9"
    
def test_try_but_7(capsys):
    lexer = Lexer('''try: {print}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == f"6\n9"
    
def test_try_but_8(capsys):
    lexer = Lexer('''try: {print.e}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
        assert error is None
    
    captured = capsys.readouterr().out
    assert captured[:-1] == f"9"
    
def test_error_raised_inst_1():
    lexer = Lexer('raise: {Error("hi")}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 'raised'
    assert error.error_name == "NoName"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_start.line == 0
    assert error.pos_end.column == 19
    assert "hi" in error.details
    
def test_error_raised_inst_2():
    lexer = Lexer('raise: {AttributeError("hi")}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 'raised'
    assert error.error_name == "AttributeError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_start.line == 0
    assert error.pos_end.column == 28
    assert "hi" in error.details
    
def test_error_raised_inst_3():
    lexer = Lexer('raise: {"hi"}', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    assert error is None
    interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
    _, error = interpreter.visit(node)
    assert error is not None
    assert isinstance(error, Error)
    assert error.error_code == 'raised'
    assert error.error_name == "NoName"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_start.line == 0
    assert error.pos_end.column == 12
    assert "hi" in error.details
    
def test_try_but_9():
    lexer = Lexer('''var: {x = Error}
                  try: {print.abut}
but: {x as e} {raise: {e}}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is not None
    
    assert error.error_code == "raised"
    assert error.error_name == "AttributeError"
    assert error.pos_start.line == 2
    assert error.pos_start.column == 15
    assert error.pos_start.line == 2
    assert error.pos_end.column == 24
    assert "Function print does not have attribute" in error.details
    
def test_check_true():
    lexer = Lexer('''check: {1 == 1}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is None
    assert isinstance(result, Boolean)
    assert result.value
    
def test_error_315_inst_1():
    lexer = Lexer('''check: {1 == 2 - 2}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is not None
    
    assert error.error_code == 315
    assert error.error_name == "CheckError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_start.line == 0
    assert error.pos_end.column == 17
    assert "1 == 0" in error.details
    
def test_error_315_inst_2():
    lexer = Lexer('''check: {3 < 4 and 1 == 2 - 2}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is not None
    
    assert error.error_code == 315
    assert error.error_name == "CheckError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_start.line == 0
    assert error.pos_end.column == 27
    assert "True and False" in error.details
    
def test_error_314_inst_1():
    lexer = Lexer('''try: {print.abut}
but: {4 as e} {raise: {e}}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is not None
    
    assert error.error_code == 314
    assert error.error_name == "TryButError"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 6
    assert error.pos_start.line == 1
    assert error.pos_end.column == 6
    assert "But exception must be Error object" in error.details
    
def test_error_314_inst_2():
    lexer = Lexer('''try: {print.abut}
but: {String as e} {raise: {e}}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is not None
    
    assert error.error_code == 314
    assert error.error_name == "TryButError"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 6
    assert error.pos_start.line == 1
    assert error.pos_end.column == 11
    assert "But exception must be Error object" in error.details
    
def test_error_314_inst_3():
    lexer = Lexer('''try: {print.abut}
but: {Type as e} {raise: {e}}
else: {print(6)}
then: {print(9)}''', "<test>")
    tokens, error = lexer.lex()
    GlobalSymbolTable = SymbolTable(lexer)
    
    line = 0
    while line < len(tokens):
        parser = Parser(tokens[line], "<shell>", lexer)
        node, error = parser.parse()
        
        interpreter = Interpreter(node, lexer, "<shell>", GlobalSymbolTable)
        result, error = interpreter.visit(node)
        line = node.pos_end.line + 1
    
    assert error is not None
    
    assert error.error_code == 314
    assert error.error_name == "TryButError"
    assert error.pos_start.line == 1
    assert error.pos_start.column == 6
    assert error.pos_start.line == 1
    assert error.pos_end.column == 9
    assert "But exception must be Error object" in error.details