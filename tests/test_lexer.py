import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from main import *

def test_lexer_produces_tokens_set_1():
    lexer = Lexer("1 + 2 * (3 - 4) ^ 5 / 6 %", "<test>")
    tokens, error = lexer.lex()

    assert error is None
    
    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("NUM", 1, 0, 0, 0),
        ("PLUS", None, 0, 2, 2),
        ("NUM", 2, 0, 4, 4),
        ("MUL", None, 0, 6, 6),
        ("LPAREN", None, 0, 8, 8),
        ("NUM", 3, 0, 9, 9),
        ("MINUS", None, 0, 11, 11),
        ("NUM", 4, 0, 13, 13),
        ("RPAREN", None, 0, 14, 14),
        ("EXP", None, 0, 16, 16),
        ("NUM", 5, 0, 18, 18),
        ("DIV", None, 0, 20, 20),
        ("NUM", 6, 0, 22, 22),
        ("MOD", None, 0, 24, 24),
        ("EOF", None, 0, 25, 25)
    ]
    
def test_lexer_produces_tokens_set_2():
    lexer = Lexer("x = += -= *= /= ^= %=\nvar: {x =+ =- =* =/ =^ =% const}", "<test>")
    tokens, error = lexer.lex()

    assert error is None
    
    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("IDENT", "x", 0, 0, 0),
        ("EQ", None, 0, 2, 2),
        ("PLUEQ", None, 0, 4, 5),
        ("MINEQ", None, 0, 7, 8),
        ("MULEQ", None, 0, 10, 11),
        ("DIVEQ", None, 0, 13, 14),
        ("EXPEQ", None, 0, 16, 17),
        ("MODEQ", None, 0, 19, 20),
        ("EOF", None, 0, 21, 21),
    ]
    
    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[1]] == [
        ("KEY", "var", 1, 0, 2),
        ("COLON", None, 1, 3, 3),
        ("LBRACE", None, 1, 5, 5),
        ("IDENT", "x", 1, 6, 6),
        ("PLUEQ", None, 1, 8, 9),
        ("MINEQ", None, 1, 11, 12),
        ("MULEQ", None, 1, 14, 15),
        ("DIVEQ", None, 1, 17, 18),
        ("EXPEQ", None, 1, 20, 21),
        ("MODEQ", None, 1, 23, 24),
        ("KEY", "const", 1, 26, 30),
        ("RBRACE", None, 1, 31, 31),
        ("EOF", None, 1, 32, 32)
    ]

def test_lexer_produces_tokens_set_3():
    lexer = Lexer("x > y < z >= w <= v != u =< => =! ==", "<test>")
    tokens, error = lexer.lex()

    assert error is None

    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("IDENT", "x", 0, 0, 0),
        ("GT", None, 0, 2, 2),
        ("IDENT", "y", 0, 4, 4),
        ("LT", None, 0, 6, 6),
        ("IDENT", "z", 0, 8, 8),
        ("GTE", None, 0, 10, 11),
        ("IDENT", "w", 0, 13, 13),
        ("LTE", None, 0, 15, 16),
        ("IDENT", "v", 0, 18, 18),
        ("NEQ", None, 0, 20, 21),
        ("IDENT", "u", 0, 23, 23),
        ("LTE", None, 0, 25, 26),
        ("GTE", None, 0, 28, 29),
        ("NEQ", None, 0, 31, 32),
        ("EQEQ", None, 0, 34, 35),
        ("EOF", None, 0, 36, 36)
    ]

def test_lexer_produces_tokens_set_4():
    lexer = Lexer("and or not nor xor xnor nand [,] in if else elif func cfunc return unpack", "<test>")
    tokens, error = lexer.lex()

    assert error is None

    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("KEY", "and", 0, 0, 2),
        ("KEY", "or", 0, 4, 5),
        ("KEY", "not", 0, 7, 9),
        ("KEY", "nor", 0, 11, 13),
        ("KEY", "xor", 0, 15, 17),
        ("KEY", "xnor", 0, 19, 22),
        ("KEY", "nand", 0, 24, 27),
        ("LSQUARE", None, 0, 29, 29),
        ("COMMA", None, 0, 30, 30),
        ("RSQUARE", None, 0, 31, 31),
        ("KEY", "in", 0, 33, 34),
        ("KEY", "if", 0, 36, 37),
        ("KEY", "else", 0, 39, 42),
        ("KEY", "elif", 0, 44, 47),
        ("KEY", "func", 0, 49, 52),
        ("KEY", "cfunc", 0, 54, 58),
        ("KEY", "return", 0, 60, 65),
        ("KEY", "unpack", 0, 67, 72),
        ("EOF", None, 0, 73, 73),
    ]

def test_lexer_produces_tokens_set_5():
    lexer = Lexer("for while loop break continue restart step . class cclass attr", "<test>")
    tokens, error = lexer.lex()

    assert error is None

    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("KEY", "for", 0, 0, 2),
        ("KEY", "while", 0, 4, 8),
        ("KEY", "loop", 0, 10, 13),
        ("KEY", "break", 0, 15, 19),
        ("KEY", "continue", 0, 21, 28),
        ("KEY", "restart", 0, 30, 36),
        ("KEY", "step", 0, 38,41),
        ("DOT", None, 0, 43, 43),
        ("KEY", "class", 0, 45, 49),
        ("KEY", "cclass", 0, 51, 56),
        ("KEY", "attr", 0, 58,61),
        ("EOF", None, 0, 62, 62)
    ]
    
def test_lexer_produces_tokens_set_6():
    lexer = Lexer("try but then raise check as", "<test>")
    tokens, error = lexer.lex()

    assert error is None

    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("KEY", "try", 0, 0, 2),
        ("KEY", "but", 0, 4, 6),
        ("KEY", "then", 0, 8, 11),
        ("KEY", "raise", 0, 13, 17),
        ("KEY", "check", 0, 19, 23),
        ("KEY", "as", 0, 25,26),
        ("EOF", None, 0, 27, 27)
    ]

def test_complex_numbers():
    lexer = Lexer("3.14 + 271", "<test>")
    tokens, error = lexer.lex()

    assert error is None
    
    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("NUM", 3.14, 0, 0, 3),
        ("PLUS", None, 0, 5, 5),
        ("NUM", 271, 0, 7, 9),
        ("EOF", None, 0, 10, 10)
    ]
    
def test_strings():
    lexer = Lexer('"Hello, World!" \'I am joe\'', "<test>")
    tokens, error = lexer.lex()

    assert error is None
    
    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("STR", "Hello, World!", 0, 0, 14),
        ("STR", "I am joe", 0, 16, 25),
        ("EOF", None, 0, 26, 26)
    ]
    
def test_error_101_inst_1():
    lexer = Lexer("4\n3 $", "<test>")
    tokens, error = lexer.lex()

    assert tokens is None
    
    assert error.error_code == 101
    assert error.pos_start.line == 1
    assert error.pos_start.column == 2
    assert error.pos_end.line == 1
    assert error.pos_end.column == 2
    assert error.details == 'Illegal character "$"'

def test_error_101_inst_2():
    lexer = Lexer("!", "<test>")
    tokens, error = lexer.lex()

    assert tokens is None
    
    assert error.error_code == 101
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 0
    assert error.details == 'Illegal character "!"'

def test_if():
    lexer = Lexer('if else elif', "<test>")
    tokens, error = lexer.lex()

    assert error is None
    
    assert [(t.type, t.value, t.line, t.pos_start, t.pos_end) for t in tokens[0]] == [
        ("KEY", "if", 0, 0, 1),
        ("KEY", "else", 0, 3, 6),
        ("KEY", "elif", 0, 8, 11),
        ('EOF', None, 0, 12, 12)
    ]
    
def test_error_102():
    lexer = Lexer("3.14.15", "<test>")
    tokens, error = lexer.lex()

    assert tokens is None
    
    assert error.error_code == 102
    assert error.error_name == "InvalidNumError"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 4
    assert error.pos_end.line == 0
    assert error.pos_end.column == 4
    assert error.details == 'Too many dots in number'
    
def test_error_103():
    lexer = Lexer('"Hello', "<test>")
    tokens, error = lexer.lex()

    assert tokens is None
    
    assert error.error_code == 103
    assert error.error_name == "UnresolvedGroupErrorL"
    assert error.pos_start.line == 0
    assert error.pos_start.column == 0
    assert error.pos_end.line == 0
    assert error.pos_end.column == 0
    assert error.details == 'Unresolved string literal'