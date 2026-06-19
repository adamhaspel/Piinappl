import sys
from pathlib import Path

# Ensure src is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from main import *

def test_number_and_bin_op():
    lexer = Lexer("1 + 2 ^ 5 / 6", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, BinaryOpNode)
    assert isinstance(node.node1, NumberNode)
    assert node.node1.tok.value == 1
    assert node.op.type == "PLUS"
    assert isinstance(node.node2, BinaryOpNode)
    assert isinstance(node.node2.node2, NumberNode)
    assert node.node2.node2.tok.value == 6
    assert isinstance(node.node2.node1, BinaryOpNode)
    assert isinstance(node.node2.node1.node1, NumberNode)
    assert node.node2.node1.node1.tok.value == 2
    assert node.node2.node1.op.type == "EXP"
    assert isinstance(node.node2.node1.node2, NumberNode)
    assert node.node2.node1.node2.tok.value == 5
    assert node.node2.op.type == "DIV"
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 12

def test_call_node():
    lexer = Lexer("1[2][3]", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    assert isinstance(node, ListCallNode)
    assert isinstance(node.call, Number)
    assert node.call.tok.value == 3
    assert isinstance(node.node, ListCallNode)
    assert isinstance(node.node.call, Number)
    assert node.node.call.tok.value == 2
    assert isinstance(node.node.node, Number)
    assert node.node.node.tok.value == 1
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 6
    
def test_unary_op():
    lexer = Lexer("-5 % 6", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, BinaryOpNode)
    assert node.op.type == "MOD"
    assert isinstance(node.node1, UnaryOpNode)
    assert node.node1.op.type == "MINUS"
    assert isinstance(node.node1.node, NumberNode)
    assert node.node1.node.tok.value == 5
    assert isinstance(node.node2, NumberNode)
    assert node.node2.tok.value == 6
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 5
    
def test_string():
    lexer = Lexer('"Hello, World!" - 4', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, BinaryOpNode)
    assert node.op.type == "MINUS"
    assert isinstance(node.node1, StringNode)
    assert node.node1.tok.value == "Hello, World!"
    assert isinstance(node.node2, NumberNode)
    assert node.node2.tok.value == 4
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 18
    
def test_parentheses():
    lexer = Lexer("(1 + 2) * 3", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<shell>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, BinaryOpNode)
    assert node.op.type == "MUL"
    assert isinstance(node.node1, BinaryOpNode)
    assert node.node1.op.type == "PLUS"
    assert isinstance(node.node1.node1, NumberNode)
    assert node.node1.node1.tok.value == 1
    assert isinstance(node.node1.node2, NumberNode)
    assert node.node1.node2.tok.value == 2
    assert isinstance(node.node2, NumberNode)
    assert node.node2.tok.value == 3
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 10

def test_logical_keys():
    lexer = Lexer("not True or False and not False", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, BinaryOpNode)
    assert node.op.value == "and"
    assert isinstance(node.node1, BinaryOpNode)
    assert node.node1.op.value == "or"
    assert isinstance(node.node1.node1, UnaryOpNode)
    assert node.node1.node1.op.value == "not"
    assert isinstance(node.node1.node1.node, VarGetNode)
    assert node.node1.node1.node.name.value == "True"
    assert isinstance(node.node1.node2, VarGetNode)
    assert node.node1.node2.name.value == "False"
    assert isinstance(node.node2, UnaryOpNode)
    assert node.node2.op.value == "not"
    assert isinstance(node.node2.node, VarGetNode)
    assert node.node2.node.name.value == "False"
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 30

def test_comparison_ops():
    lexer = Lexer("3 > 2 != 2 <= 3 == 4 < 6 >= 8 in 9", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None

    assert isinstance(node, BinaryOpNode)
    assert node.op.type == "KEY"
    assert node.op.value == "in"
    oldnode = node
    node = node.node1
    assert isinstance(node, BinaryOpNode)
    assert node.op.type == "GTE"
    assert isinstance(node.node1, BinaryOpNode)
    assert node.node1.op.type == "LT"
    assert isinstance(node.node1.node1, BinaryOpNode)
    assert node.node1.node1.op.type == "EQEQ"
    assert isinstance(node.node1.node1.node1, BinaryOpNode)
    assert node.node1.node1.node1.op.type == "LTE"
    assert isinstance(node.node1.node1.node1.node1, BinaryOpNode)
    assert node.node1.node1.node1.node1.op.type == "NEQ"
    assert isinstance(node.node1.node1.node1.node1.node1, BinaryOpNode)
    assert node.node1.node1.node1.node1.node1.op.type == "GT"
    assert isinstance(node.node1.node1.node1.node1.node1.node1, NumberNode)
    assert node.node1.node1.node1.node1.node1.node1.tok.value == 3
    assert isinstance(node.node1.node1.node1.node1.node1.node2, NumberNode)
    assert node.node1.node1.node1.node1.node1.node2.tok.value == 2
    assert isinstance(node.node1.node1.node1.node1.node2, NumberNode)
    assert node.node1.node1.node1.node1.node2.tok.value == 2
    assert isinstance(node.node1.node1.node1.node2, NumberNode)
    assert node.node1.node1.node1.node2.tok.value == 3
    assert isinstance(node.node1.node1.node2, NumberNode)
    assert node.node1.node1.node2.tok.value == 4
    assert isinstance(node.node1.node2, NumberNode)
    assert node.node1.node2.tok.value == 6
    assert isinstance(node.node2, NumberNode)
    assert node.node2.tok.value == 8
    assert isinstance(oldnode.node2, NumberNode)
    assert oldnode.node2.tok.value == 9
    assert node.node2.tok.value == 8
    assert oldnode.pos_start.line == 0
    assert oldnode.pos_start.column == 0
    assert oldnode.pos_end.line == 0
    assert oldnode.pos_end.column == 33

    
def test_multiline():
    lexer = Lexer("4\n5", "<test>")
    tokens, error = lexer.lex()
    
    parser0 = Parser(tokens[0], "<shell>", lexer)
    node0, error = parser0.parse()
    
    assert error is None
    
    parser1 = Parser(tokens[1], "<shell>", lexer)
    node1, error = parser1.parse()
    
    assert error is None
    
    assert isinstance(node0, NumberNode)
    assert node0.tok.value == 4
    assert node0.pos_start.line == 0
    assert node0.pos_start.column == 0
    assert node0.pos_end.line == 0
    assert node0.pos_end.column == 0
    assert isinstance(node1, NumberNode)
    assert node1.tok.value == 5
    assert node1.pos_start.line == 1
    assert node1.pos_start.column == 0
    assert node1.pos_end.line == 1
    assert node1.pos_end.column == 0

def test_list():
    lexer = Lexer("[4, 5, 6, 7]", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    assert isinstance(node, ListNode)
    assert str(node.contents) == "[NUM:4, NUM:5, NUM:6, NUM:7]"
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 11

def test_empty_list():
    lexer = Lexer("[]", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    assert isinstance(node, ListNode)
    assert str(node.contents) == "[]"
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 1
    
def test_error_201_inst_1():
    lexer = Lexer("(1 + 1", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 0
    assert error.details == 'Unresolved grouping: "("'
    
def test_error_202_inst_1():
    lexer = Lexer("1 + * 2", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 202
    assert error.error_name == "UnexpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    assert error.details == 'Unexpected token: "MUL"'
    
def test_error_203():
    lexer = Lexer("1 + (2 * 3) 4 + 4", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 203
    assert error.error_name == "EOFError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 12
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12
    assert error.details == 'Conjoined expression'
    
def test_vardef_node():
    lexer = Lexer("var: {x = 5}\nconst: {y = 5}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, VarDefNode)
    assert node.name.value == "x"
    assert isinstance(node.value, NumberNode)
    assert node.value.tok.value == 5
    assert node.eqtype.type == "EQ"
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 10
    assert node.key.value == "var"
    
    parser = Parser(tokens[1], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, VarDefNode)
    assert node.name.value == "y"
    assert isinstance(node.value, NumberNode)
    assert node.value.tok.value == 5
    assert node.eqtype.type == "EQ"
    assert node.pos_start.line == 1
    assert node.pos_start.column == 0
    assert node.pos_end.line == 1
    assert node.pos_end.column == 12
    assert node.key.value == "const"

def test_func_def_node_monoline():
    lexer = Lexer("cfunc: {hi(a, b, c)} {1 + 2 + 3}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    assert isinstance(node, FuncDefNode)
    assert node.key.value == "cfunc" 
    assert node.ident.value == "hi" 
    assert [(t.value, t.pos_start, t.pos_end) for t in node.args] == [
        ("a", 11, 11),
        ("b", 14, 14),
        ("c", 17, 17)
    ]
    assert isinstance(node.then[0], BinaryOpNode)
    assert node.pos_end.line == 0

def test_call_node():
    lexer = Lexer("hi(a, 2, 'hi' + 6)", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    assert isinstance(node, CallNode)
    assert node.var.value == "hi" 
    assert isinstance(node.args[0], VarGetNode)
    assert isinstance(node.args[1], NumberNode)
    assert isinstance(node.args[2], BinaryOpNode)
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 17

def test_return_node():
    lexer = Lexer("return: {1, 2}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    assert isinstance(node, ReturnNode)
    assert [(t.tok.value, t.pos_start.column, t.pos_end.column) for t in node.nodes] == [
        (1, 9, 9),
        (2, 12, 12)
    ]
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 13

def test_error_204_inst_7():
    lexer = Lexer("func", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    assert error.details == 'Expected token: ":"'

def test_error_204_inst_8():
    lexer = Lexer("func:", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 5
    assert error.pos_end.line == 0
    assert error.pos_end.column == 5
    assert error.details == 'Expected token: "{"'

def test_error_204_inst_9():
    lexer = Lexer("func: {", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 7
    assert error.pos_end.line == 0
    assert error.pos_end.column == 7
    assert error.details == 'Expected token: IDENT'

def test_error_204_inst_10():
    lexer = Lexer("func: {hi", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 9
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9
    assert error.details == 'Expected token: "("'

def test_error_204_inst_11():
    lexer = Lexer("func: {hi()}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 12
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12
    assert error.details == 'Expected token: "{"'

def test_error_204_inst_12():
    lexer = Lexer("return: ", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_end.line == 0
    assert error.pos_end.column == 8
    assert error.details == 'Expected token: "{"'

def test_error_201_inst_10():
    lexer = Lexer("func: {hi(", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 9
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9
    assert error.details == 'Unresolved grouping: "("'

def test_error_201_inst_11():
    lexer = Lexer("func: {hi()", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 6
    assert error.pos_end.line == 0
    assert error.pos_end.column == 6
    assert error.details == 'Unresolved grouping: "{"'

def test_error_201_inst_10():
    lexer = Lexer("return: {hi()", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 8
    assert error.pos_end.line == 0
    assert error.pos_end.column == 8
    assert error.details == 'Unresolved grouping: "{"'

def test_error_201_inst_12():
    lexer = Lexer("func: {hi()}{", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 12
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12
    assert error.details == 'Unresolved grouping: "{"'
    
def test_varget_node():
    lexer = Lexer("x", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert error is None
    
    assert isinstance(node, VarGetNode)
    assert node.name.value == "x"
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 0
    
def test_error_204_inst_1():
    lexer = Lexer("var", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 3
    assert error.pos_end.line == 0
    assert error.pos_end.column == 3
    assert error.details == 'Expected token: ":"'
    
def test_error_204_inst_2():
    lexer = Lexer("var:", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    assert error.details == 'Expected token: "{"'
    
def test_error_204_inst_3():
    lexer = Lexer("var: {", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 6
    assert error.pos_end.line == 0
    assert error.pos_end.column == 6
    assert error.details == 'Expected token: "IDENT"'

def test_error_204_inst_4():
    lexer = Lexer("var: {x", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 7
    assert error.pos_end.line == 0
    assert error.pos_end.column == 7
    assert error.details == 'Expected token: "="'

def test_error_202_inst_2():
    lexer = Lexer("var: {x =", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 202
    assert error.error_name == "UnexpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 9
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9
    assert error.details == 'Unexpected token: "EOF"'

def test_error_202_inst_3():
    lexer = Lexer("var: {x =}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 202
    assert error.error_name == "UnexpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 9
    assert error.pos_end.line == 0
    assert error.pos_end.column == 9
    assert error.details == 'Unexpected token: "RBRACE"'

def test_error_204_inst_5():
    lexer = Lexer("()", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 1
    assert error.pos_end.line == 0
    assert error.pos_end.column == 1
    assert error.details == 'Expected expression'

def test_error_204_inst_6():
    lexer = Lexer("[1 2]", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 3
    assert error.pos_end.line == 0
    assert error.pos_end.column == 3
    assert error.details == 'Expected token: ","'

def test_if_simple():
    lexer = Lexer('if: {1 == 1} {5}', "<test>")
    tokens, error = lexer.lex()

    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()

    assert error is None
    assert isinstance(node, IfNode)
    assert isinstance(node.cond, BinaryOpNode)
    assert node.cond.op.type == "EQEQ"
    assert isinstance(node.then, list)
    assert isinstance(node.then[0], NumberNode)
    assert node.then[0].tok.value == 5

def test_else_and_elif():
    lexer = Lexer('if: {1 == 2} {5} elif: {2 == 2} {6} else: {7}', "<test>")
    tokens, error = lexer.lex()

    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()

    assert error is None
    assert isinstance(node, IfNode)
    assert isinstance(node.cond, BinaryOpNode)
    assert isinstance(node.elifs, IfNode)
    assert isinstance(node.elifs.then, list)
    assert isinstance(node.elifs.then[0], NumberNode)
    assert node.elifs.then[0].tok.value == 6
    assert isinstance(node.elifs._else, list)
    assert isinstance(node.elifs._else[0], NumberNode)
    assert node.elifs._else[0].tok.value == 7

def test_error_201_inst_13():
    lexer = Lexer("var: {x = 1 + 2 * (3 - 4)", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 5
    assert error.pos_end.line == 0
    assert error.pos_end.column == 5
    assert error.details == "Unresolved grouping: \"{\""

def test_error_201_inst_3():
    lexer = Lexer('if: {1 == 1 {5}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    assert error.details == "Unresolved grouping: \"{\""

def test_error_201_inst_4():
    lexer = Lexer('if: {True } {1 + 2 * 3', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 12
    assert error.pos_end.line == 0
    assert error.pos_end.column == 12
    assert error.details == "Unresolved grouping: \"{\""

def test_error_201_inst_5():
    lexer = Lexer('if: {False } {5 } elif: {x == 3 {6} else: {7}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 24
    assert error.pos_end.line == 0
    assert error.pos_end.column == 24
    assert error.details == "Unresolved grouping: \"{\""
    
def test_error_201_inst_6():
    lexer = Lexer('if: {False } {5} elif: {True} {var: {x = 10 * 2} else: {7}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 30
    assert error.pos_end.line == 0
    assert error.pos_end.column == 30
    assert error.details == "Unresolved grouping: \"{\""

def test_error_201_inst_7():
    lexer = Lexer('if: {False } {5 } elif: {False } {6 } else: {1 + 3', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 44
    assert error.pos_end.line == 0
    assert error.pos_end.column == 44
    assert error.details == "Unresolved grouping: \"{\""
    

def test_error_201_inst_8():
    lexer = Lexer('if: {True} {5} else: {var: {y = (x - 4}}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 32
    assert error.pos_end.line == 0
    assert error.pos_end.column == 32
    assert error.details == "Unresolved grouping: \"(\""

def test_error_201_inst_9():
    lexer = Lexer('[1, 2', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 0
    assert error.details == "Unresolved grouping: \"[\""

def test_error_201_inst_14():
    lexer = Lexer('1[1', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 1
    assert error.pos_end.line == 0
    assert error.pos_end.column == 1
    assert error.details == "Unresolved grouping: \"[\""

def test_dict_node_empty():
    lexer = Lexer('{}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()

    assert error is None
    assert isinstance(node, DictNode)
    assert [(t.tok, t.pos_start, t.pos_end) for t in node.contents] == []
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 1

def test_dict_node_1():
    lexer = Lexer('{"one": 1}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()

    assert error is None
    assert isinstance(node, DictNode)
    assert [(t.tok.value, t.pos_start.column, t.pos_end.column, node.contents[t].tok.value, node.contents[t].pos_start.column, node.contents[t].pos_end.column) for t in node.contents] == [
        ("one", 1, 5, 1, 8, 8)
    ]
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 9

def test_dict_node_2():
    lexer = Lexer('{"one": 1, "two": 2}', "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()

    assert error is None
    assert isinstance(node, DictNode)
    assert [(t.tok.value, t.pos_start.column, t.pos_end.column, node.contents[t].tok.value, node.contents[t].pos_start.column, node.contents[t].pos_end.column) for t in node.contents] == [
        ("one", 1, 5, 1, 8, 8),
        ("two", 11, 15, 2, 18, 18)
    ]
    assert node.pos_start.line == 0
    assert node.pos_start.column == 0
    assert node.pos_end.line == 0
    assert node.pos_end.column == 19

def test_error_201_inst_15():
    lexer = Lexer("{1 + 1:2", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 201
    assert error.error_name == "UnresolvedGroupErrorP"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 0
    assert error.details == 'Unresolved grouping: "{"'

def test_error_204_inst_13():
    lexer = Lexer("{ 1}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 204
    assert error.error_name == "ExpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 3
    assert error.pos_end.line == 0
    assert error.pos_end.column == 3
    assert error.details == 'Expected token: ":"'

def test_error_202_inst_4():
    lexer = Lexer("{ 1:}", "<test>")
    tokens, error = lexer.lex()
    
    parser = Parser(tokens[0], "<test>", lexer)
    node, error = parser.parse()
    
    assert node is None
    
    assert error.error_code == 202
    assert error.error_name == "UnexpectedTokenError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    assert error.details == 'Unexpected token: "RBRACE"'
