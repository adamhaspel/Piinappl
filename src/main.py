###########
# IMPORTS #
###########

from stringcolor import *

#############
# CONSTANTS #
#############

# Token Types
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_EXP = "EXP"
TT_MOD = "MOD"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"
TT_GT = "GT"
TT_LT = "LT"
TT_GTE = "GTE"
TT_LTE = "LTE"
TT_EQEQ = "EQEQ"
TT_NEQ = "NEQ"
TT_COLON = "COLON"
TT_NUM = "NUM"
TT_STR = "STR"
TT_EQ = "EQ"
TT_PLUEQ = "PLUEQ"
TT_MINEQ = "MINEQ"
TT_MULEQ = "MULEQ"
TT_DIVEQ = "DIVEQ"
TT_EXPEQ = "EXPEQ"
TT_MODEQ = "MODEQ"
TT_EOF = "EOF"
TT_KEY = "KEY"
TT_IDENT = "IDENT"

# Keywords
KEYS = ["var", "const", "and", "or", "nor", "xor", "nand", "xnor", "not", "if", "elif", "else"]

# Characters
DIGITS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
LETTERS_DIGITS = LETTERS + DIGITS

############
# POSITION #
############

class Position():
    def __init__(self, index, line, column, source="<file>"):
        self.index = index
        self.line = line
        self.column = column
        self.source = source
    
    def __repr__(self):
        return f"{self.line}:{self.column}"

##########
# ERRORS #
##########

class Error():
    def __init__(self, error_code, pos_start, pos_end, details, content):
        self.error_code = error_code
        if self.error_code == 101:
            self.error_name = "IllegalCharError"
        if self.error_code == 102:
            self.error_name = "InvalidNumError"
        if self.error_code == 103:
            self.error_name = "UnresolvedGroupErrorL"
        if self.error_code == 201:
            self.error_name = "UnresolvedGroupErrorP"
        if self.error_code == 202:
            self.error_name = "UnexpectedTokenError"
        if self.error_code == 203:
            self.error_name = "EOFError"
        if self.error_code == 204:
            self.error_name = "ExpectedTokenError"
        if self.error_code == 301:
            self.error_name = "IncompatibleOpError"
        if self.error_code == 302:
            self.error_name = "RuntimeError"
        if self.error_code == 303:
            self.error_name = "NumberError"
        if self.error_code == 304:
            self.error_name = "SymbolGetError"
        if self.error_code == 305:
            self.error_name = "ConstantError"
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details
        self.content = content
        
    def __repr__(self):
        result = cs(f"Error {self.error_code} - {self.error_name}: {self.details}\n", "rgb(250,100,100)")
        result += cs(f"   File {self.pos_start.index} in {self.pos_start.source}, line {self.pos_start.line + 1}\n", "rgb(250, 150, 150)")
        result += cs(f"      {self.content}\n", "rgb(250, 165, 165)")
        result += cs(f"      " + " " * (self.pos_start.column) + ("^" * (self.pos_end.column - self.pos_start.column + 1)), "rgb(250, 180, 180)")
        return result

##########
# TOKENS #
##########

class Token():
    def __init__(self, type, value, line, pos_start, pos_end=None):
        self.type = type
        self.value = value
        self.line = line
        self.pos_start = pos_start
        self.pos_end = pos_start if pos_end is None else pos_end
        
    def __repr__(self,):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    
#########
# NODES #
#########

class NumberNode():
    def __init__(self, tok, index):
        self.tok = tok
        self.pos_start = Position(index, self.tok.line, self.tok.pos_start)
        self.pos_end = Position(index, self.tok.line, self.tok.pos_end)
        
    def __repr__(self):
        return f"{self.tok}"
    
class StringNode():
    def __init__(self, tok, index):
        self.tok = tok
        self.pos_start = Position(index, self.tok.line, self.tok.pos_start)
        self.pos_end = Position(index, self.tok.line, self.tok.pos_end)
        
    def __repr__(self):
        return f"'{self.tok}'"
    
class BinaryOpNode():
    def __init__(self, node1, op, node2):
        self.node1 = node1
        self.op = op
        self.node2 = node2
        self.pos_start = self.node1.pos_start
        self.pos_end = self.node2.pos_end
        
    def __repr__(self):
        return f"({self.node1} {self.op} {self.node2})"

class IfNode():
    def __init__(self, cond, then, pos_end, elifs=None, _else=None):
        self.cond = cond
        self.then = then
        self.elifs = elifs
        self._else = _else
        self.pos_end = Position(None, pos_end, pos_end)

    def __repr__(self):
        return f'if {self.cond} then {self.then} elif {self.elifs} else {self._else}'

class UnaryOpNode():
    def __init__(self, op, node, index):
        self.op = op
        self.node = node
        self.pos_start = Position(index, self.op.line, self.op.pos_start)
        self.pos_end = self.node.pos_end
        
    def __repr__(self):
        return f"({self.op} {self.node})"
    
class VarDefNode():
    def __init__(self, key, name, eqtype, value, pos_end, index):
        self.key = key
        self.name = name
        self.eqtype = eqtype
        self.op = eqtype
        self.value = value
        self.node2 = value
        self.pos_start = Position(index, self.key.line, self.key.pos_start)
        self.pos_end = pos_end
        self.pos_end.column -= 1
        
    def __repr__(self):
        return f"({self.key} {self.name} {self.eqtype} {self.value})"

class VarGetNode():
    def __init__(self, name, index):
        self.name = name
        self.pos_start = Position(index, self.name.line, self.name.pos_start)
        self.pos_end = Position(index, self.name.line, self.name.pos_end)
        
    def __repr__(self):
        return f"{self.name}"
    
##########
# VALUES #
##########

class Value():
    def __init__(self, value, lexer):
        self.value = value
        self.lexer = lexer
        self.bool = bool(self.value)
        
    def add(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def sub(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def mul(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def div(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def eq(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value == other.value, self.lexer), None
        else:
            return Boolean(0, self.lexer), None
    
    def neq(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value != other.value, self.lexer), None
        else:
            return Boolean(1, self.lexer), None
        
    def lt(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value < other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def gt(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value > other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def gte(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value >= other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def lte(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value <= other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def exp(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def mod(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def _or(self, node, other):
        if (not self.bool and not other.bool):
            return Boolean(0, self.lexer), None
        return Boolean(1, self.lexer), None

    def _and(self, node, other):
        if (self.bool and other.bool):
            return Boolean(1, self.lexer), None
        return Boolean(0, self.lexer), None
    
    def _xor(self, node, other):
        if (self.bool != other.bool):
            return Boolean(1, self.lexer), None
        return Boolean(0, self.lexer), None

    def _nand(self, node, other):
        if (self.bool and other.bool):
            return Boolean(0, self.lexer), None
        return Boolean(1, self.lexer), None
    
    def _nor(self, node, other):
        if (self.bool or other.bool):
            return Boolean(0, self.lexer), None
        return Boolean(1, self.lexer), None
    
    def _xnor(self, node, other):
        if (self.bool == other.bool):
            return Boolean(1, self.lexer), None
        return Boolean(0, self.lexer), None
    
    def _not(self, node):
        return Boolean(not(self.bool), self.lexer), None

class NoneType(Value):
    def __init__(self, lexer):
        super().__init__(0, lexer)

    def lt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def gt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def gte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def lte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def __repr__(self):
        return "None"

class Boolean(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)

    def lt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def gt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def gte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def lte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def __repr__(self):
        return "True" if self.value else "False"

class String(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)
        self.bool = True
        
    def add(self, node, other):
        if isinstance(other, Number) or isinstance(other, String):
            return String(self.value + other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def mul(self, node, other):
        if isinstance(other, Number):
            try:
                return String(self.value * other.value, self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start), node.node2.pos_end, f'Invalid operation of String and non-integer', self.lexer.text.split("\n")[node.pos_start.line])
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def sub(self, node, other):
        if isinstance(other, Number):
            if other.value > len(self.value):
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start), node.node2.pos_end, f'Invalid operation of String and number longer than length', self.lexer.text.split("\n")[node.pos_start.line])
            try:
                return String(self.value[:-other.value], self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start), node.node2.pos_end, f'Invalid operation of String and non-integer', self.lexer.text.split("\n")[node.pos_start.line])
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
    
    def __repr__(self):
        return f"'{self.value}'"

class Number(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)
        if self.value % 1 == 0:
            self.value = int(self.value)
        self.bool = True
        
    def add(self, node, other):
        if isinstance(other, Number):
            return Number(self.value + other.value, self.lexer), None
        elif isinstance(other, String):
            return String(str(self.value) + other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def sub(self, node, other):
        if isinstance(other, Number):
            return Number(self.value - other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def mul(self, node, other):
        if isinstance(other, Number):
            return Number(self.value * other.value, self.lexer), None
        elif isinstance(other, String):
            try:
                return String(str(other.value) * self.value, self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start), node.node2.pos_end, f'Invalid operation of String and non-integer', self.lexer.text.split("\n")[node.pos_start.line])
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def div(self, node, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Error(302, Position(self.lexer.index, node.op.line, node.op.pos_start), node.node2.pos_end, 'Division by zero', self.lexer.text.split("\n")[node.pos_start.line])
            return Number(self.value / other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def exp(self, node, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])
        
    def mod(self, node, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Error(302, Position(self.lexer.index, node.op.line, node.op.pos_start), node.node2.pos_end, 'Division by zero', self.lexer.text.split("\n")[node.pos_start.line])
            return Number(self.value % other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n")[node.pos_start.line])

    def __repr__(self):
        return f"{self.value}"
    
###############
# SYMBOLTABLE #
###############

class SymbolTable():
    def __init__(self, parent=None):
        self.symbols = {}
        self.constants = {"None": NoneType(None), "True": Boolean(1, None), "False": Boolean(0, None)}
        self.parent = parent
        
    def get(self, name):
        value = self.symbols.get(name.value, None)
        if value is None and self.parent:
            return self.parent.get(name.value)
        if value == None:
            value = self.constants.get(name.value, None)
            if value is None and self.parent:
                return self.parent.get(name.value)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
        
    def set_constant(self, name, value):
        self.constants[name] = value
        
    def remove(self, name):
        del self.symbols[name]
 
#########
# LEXER #
#########

class Lexer():
    def __init__(self, text, index):
        self.text = text
        self.index = index
        
    def lex(self):
        self.lines = self.text.split("\n")
        out = []
        linepos = -1
        lines = []
        for i in self.lines:
            i = list(i)
            i.append("END")
            lines.append(i)
        self.lines = lines
        # Divide by lines
        for i in self.lines:
            linepos += 1
            pos = 0
            line = []
            # Divide by characters
            j = i[pos]
            while j != "END":
                if j == " ":
                    pos += 1
                    j = i[pos]
                    continue
                elif j == "+":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_PLUEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_PLUS, None, linepos, pos_start, pos_start))
                elif j == "-":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_MINEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_MINUS, None, linepos, pos_start, pos_start))
                elif j == "*":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_MULEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_MUL, None, linepos, pos_start, pos_start))
                elif j == "^":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_EXPEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_EXP, None, linepos, pos_start, pos_start))
                elif j == "/":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_DIVEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_DIV, None, linepos, pos_start, pos_start))
                elif j == "%":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_MODEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_MOD, None, linepos, pos_start, pos_start))
                elif j == "(":
                    line.append(Token(TT_LPAREN, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == ")":
                    line.append(Token(TT_RPAREN, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == "{":
                    line.append(Token(TT_LBRACE, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == "}":
                    line.append(Token(TT_RBRACE, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == ">":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_GTE, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_GT, None, linepos, pos_start, pos_start))
                elif j == "<":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_LTE, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_LT, None, linepos, pos_start, pos_start))
                elif j == "!":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "=":
                        line.append(Token(TT_NEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        return None, Error(101, Position(self.index, linepos, pos_start), Position(self.index, linepos, pos_start), f'Illegal character "!"', self.text.split("\n")[linepos])
                elif j == ":":
                    line.append(Token(TT_COLON, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == "=":
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    if j == "+":
                        line.append(Token(TT_PLUEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "-":
                        line.append(Token(TT_MINEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "*":
                        line.append(Token(TT_MULEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "/":
                        line.append(Token(TT_DIVEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "^":
                        line.append(Token(TT_EXPEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "%":
                        line.append(Token(TT_MODEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "=":
                        line.append(Token(TT_EQEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == ">":
                        line.append(Token(TT_GTE, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "<":
                        line.append(Token(TT_LTE, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    elif j == "!":
                        line.append(Token(TT_NEQ, None, linepos, pos_start, pos))
                        pos += 1
                        j = i[pos]
                    else:
                        line.append(Token(TT_EQ, None, linepos, pos_start, pos_start))
                elif j in ["'", '"']:
                    # Create Strings
                    stringtype = j
                    string = ""
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    while j != stringtype:
                        if j == "END":
                            return None, Error(103, Position(self.index, linepos, pos_start), Position(self.index, linepos, pos_start), f'Unresolved string literal', self.text.split("\n")[linepos])
                        string += j
                        pos += 1
                        j = i[pos]
                    line.append(Token(TT_STR, string, linepos, pos_start, pos))
                    pos += 1
                    j = i[pos]
                elif j in DIGITS + ".":
                    # Create Numbers
                    dot = 0
                    num = ""
                    if j == ".":
                        dot += 1
                    num += j
                    # Advance
                    pos_start = pos
                    pos += 1
                    j = i[pos]
                    while j in DIGITS + ".":
                        if j == ".":
                            dot += 1
                            if dot > 1:
                                return None, Error(102, Position(self.index, linepos, pos), Position(self.index, linepos, pos), "Too many dots in number", self.text.split("\n")[linepos])
                        num += j
                        pos += 1
                        j = i[pos]
                    # Check for errors
                    if num[-1] == ".":
                        return None, Error(102, Position(self.index, linepos, pos-1), Position(self.index, linepos, pos-1), "Number cannot end with a dot", self.text.split("\n")[linepos])
                    if dot == 1:
                        line.append(Token(TT_NUM, float(num), linepos, pos_start, pos-1))
                    else:
                        line.append(Token(TT_NUM, int(num), linepos, pos_start, pos-1))
                elif j in LETTERS:
                    # Create Identifiers and Keywords
                    ide = ""
                    pos_start = pos
                    while j in LETTERS_DIGITS + "_-":
                        ide += j
                        pos += 1
                        j = i[pos]
                    if ide in KEYS:
                        line.append(Token(TT_KEY, ide, linepos, pos_start, pos-1))
                    else:
                        line.append(Token(TT_IDENT, ide, linepos, pos_start, pos-1))
                else:
                    return None, Error(101, Position(self.index, linepos, pos), Position(self.index, linepos, pos), f'Illegal character "{j}"', self.text.split("\n")[linepos])
            # Add EOF Token
            line.append(Token(TT_EOF, None, linepos, pos, pos))
            # Reattach line to output
            out.append(line)
        return out, None
    
##########
# PARSER #
##########

class Parser():
    def __init__(self, tokens, index, lexer):
        self.tokens = tokens
        self.index = index
        self.lexer = lexer
        
    def advance(self):
        if self.current_tok.type != "EOF":
            self.current_tok = self.tokens[self.tokens.index(self.current_tok) + 1]
            return self.current_tok
        return None
        
    def parse(self):
        self.current_tok = self.tokens[0]
        node, error = self.expr()
        if error:
            return None, error
        if self.current_tok.type != "EOF":
            return None, Error(203, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Conjoined expression', self.lexer.text.split("\n")[self.current_tok.line])
        return node, None
    
    def expr(self):
        if self.current_tok.type == "KEY" and self.current_tok.value in ["var", "const", 'if']:
            if self.current_tok.value in ["var", "const"]:
                node, error = self.var(self.current_tok)
            elif self.current_tok.value in ["if"]:
                node, error = self.ifexpr(self.current_tok.line)
        else:
            node, error = self.andor()
        if error:
            return None, error
        return node, None
    
    def parse_mini(self):
        self.current_tok = self.tokens[0]
        if self.current_tok.type == "RBRACE":
            return None, None
        node, error = self.expr()
        if error:
            return None, error
        return node, None
    
    def var(self, key):
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Expected token: ":"', self.lexer.text.split("\n")[self.current_tok.line])
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), 'Expected token: "{"', self.lexer.text.split("\n")[self.current_tok.line])
        pos_start = self.current_tok.pos_start
        self.advance()
        if self.current_tok.type != "IDENT":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Expected token: "IDENT"', self.lexer.text.split("\n")[self.current_tok.line])
        name = self.current_tok
        self.advance()
        if self.current_tok.type not in ["EQ", "PLUEQ", "MINEQ", "MULEQ", "DIVEQ", "EXPEQ", "MODEQ"]:
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Expected token: "="', self.lexer.text.split("\n")[self.current_tok.line])
        eqtype = self.current_tok
        self.advance()
        node, error = self.andor()
        if error:
            return None, error
        if self.current_tok.type != "RBRACE":
            return None, Error(201, Position(self.index, self.current_tok.line, pos_start), Position(self.index, self.current_tok.line, pos_start), 'Unresolved grouping: "{"', self.lexer.text.split("\n")[self.current_tok.line])
        pos_end = Position(self.index, self.current_tok.line, self.current_tok.pos_end)
        self.advance()
        return VarDefNode(key, name, eqtype, node, pos_end, self.index), None
        
    def ifexpr(self, line):
        elifs = None
        _else = None
        tokens, error = Lexer(self.lexer.text, self.index).lex()
        if error:
            return None, error
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Expected token: ":"', self.lexer.text.split("\n")[self.current_tok.line])
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), 'Expected token: "{"', self.lexer.text.split("\n")[self.current_tok.line])
        pos_start = self.current_tok.pos_start
        self.advance()
        cond, error = self.andor()
        if error:
            return None, error
        if self.current_tok.type != "RBRACE":
            return None, Error(201, Position(self.index, self.current_tok.line, pos_start), Position(self.index, self.current_tok.line, pos_start), 'Unresolved grouping: "{"', self.lexer.text.split("\n")[self.current_tok.line])
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), 'Expected token: "{"', self.lexer.text.split("\n")[self.current_tok.line])
        pos_start = self.current_tok.pos_start
        linepos = self.current_tok.line
        self.advance()
        then = []
        finished = False
        if self.current_tok.type != "EOF":
            node, error = self.expr()
            if error:
                return None, error
            then.append(node)
            if self.current_tok.type == "RBRACE":
                finished = True
                self.advance()
        line = self.current_tok.line - 1
        if finished == False:
            line += 1
        tokens, line, then, finished = self.multiline(tokens, line, then, linepos, pos_start, finished)
        if not tokens:
            return None, line
        lineifnoelses = line
        tokifnoelses = self.current_tok
        try:
            line += 1
            while self.current_tok.type == "EOF":
                self.tokens = tokens[line]
                self.current_tok = self.tokens[0]
                line += 1
        except IndexError:
            line = lineifnoelses
        else:
            if finished == False:
                return None, Error(201, Position(self.index, self.current_tok.line, pos_start), Position(self.index, self.current_tok.line, pos_start), 'Unresolved grouping: "{"', self.lexer.text.split("\n")[self.current_tok.line])
            if self.current_tok.type == "KEY" and self.current_tok.value == "elif":
                elifs, error = self.ifexpr(line)
                if error:
                    return None, error
                line = elifs.pos_end.line
            elif self.current_tok.type == "KEY" and self.current_tok.value == "else":
                _else, error, line = self.elseexpr(tokens, line)
                if error:
                    return None, error
            else:
                line = lineifnoelses
                self.tokens = tokens[line]
                self.current_tok = tokifnoelses
        return IfNode(cond, then, line, elifs, _else), None
    
    def elseexpr(self, tokens, line):
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Expected token: ":"', self.lexer.text.split("\n")[self.current_tok.line]), None
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), 'Expected token: "{"', self.lexer.text.split("\n")[self.current_tok.line]), None
        pos_start = self.current_tok.pos_start
        linepos = self.current_tok.line
        self.advance()
        then = []
        finished = False
        if self.current_tok.type != "EOF":
            node, error = self.expr()
            if error:
                return None, error, line
            then.append(node)
            if self.current_tok.type == "RBRACE":
                finished = True
                self.advance()
        line = self.current_tok.line - 1
        if finished == False:
            line += 1
        tokens, line, then, finished = self.multiline(tokens, line, then, linepos, pos_start, finished)
        if not tokens:
            return None, line, None
        return then, None, line

    def multiline(self, tokens, line, then, linepos, pos_start, finished):
        line += 1
        while self.current_tok.type == "EOF" and finished == False:
            try:
                self.tokens = tokens[line]
                if len(self.tokens) == 1:
                    line += 1
                    continue
            except IndexError:
                return None, Error(201, Position(self.index, linepos, pos_start), Position(self.index, linepos, pos_start), 'Unresolved grouping: "{"', self.lexer.text.split("\n")[linepos]), None, None
            node, error = self.parse_mini()
            if error:
                return None, error, None, None
            then.append(node)
            if self.current_tok.type == "RBRACE":
                finished = True
                self.advance()
                break
            if node:
                line = node.pos_end.line + 1
            else:
                line += 1
        return tokens, line, then, finished

    def num(self):
        if self.current_tok.type == "NUM":
            # Numbers
            num = self.current_tok
            self.advance()
            return NumberNode(num, self.index), None
        elif self.current_tok.type == "IDENT":
            # Variables
            var = self.current_tok
            self.advance()
            return VarGetNode(var, self.index), None
        elif self.current_tok.type == "STR":
            # Strings
            string = self.current_tok
            self.advance()
            return StringNode(string, self.index), None
        elif self.current_tok.type == "LPAREN":
            # Parentheses
            lparen = self.current_tok
            self.advance()
            if self.current_tok.type == "RPAREN":
                # Empty Group
                return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), 'Expected expression', self.lexer.text.split("\n")[lparen.line])
            node, error = self.andor()
            if error:
                return None, error
            if self.current_tok.type != "RPAREN":
                # Unclosed Group
                return None, Error(201, Position(self.index, lparen.line, lparen.pos_start), Position(self.index, lparen.line, lparen.pos_end), 'Unresolved grouping: "("', self.lexer.text.split("\n")[lparen.line])
            node.pos_start = Position(self.index, lparen.line, lparen.pos_start)
            node.pos_end = Position(self.index, self.current_tok.line, self.current_tok.pos_end)
            self.advance() 
            return node, None
        elif (self.current_tok.type in ["PLUS", "MINUS"]) or (self.current_tok.type == "KEY" and self.current_tok.value == "not"):
            # Unary Operations
            op = self.current_tok
            self.advance()
            node, error = self.num()
            if error:
                return None, error
            return UnaryOpNode(op, node, self.index), None
        else:
            return None, Error(202, Position(self.index, self.current_tok.line, self.current_tok.pos_start), Position(self.index, self.current_tok.line, self.current_tok.pos_end), f'Unexpected token: "{self.current_tok}"', self.lexer.text.split("\n")[self.current_tok.line])
        
    def exp(self):
        node1, error = self.num()
        if error:
            return None, error
        
        return self.binaryoperation(node1, ["EXP"], self.num)
        
    def muldiv(self):
        node1, error = self.exp()
        if error:
            return None, error
        
        return self.binaryoperation(node1, ["MUL", "DIV", "MOD"], self.exp)

    def gtlt(self):
        node1, error = self.plusminus()
        if error:
            return None, error
        
        return self.binaryoperation(node1, ["GT", "LT", "GTE", "LTE", "EQEQ", "NEQ"], self.plusminus)
    
    def andor(self):
        node1, error = self.gtlt()
        if error:
            return None, error
        
        while self.current_tok.type == "KEY" and self.current_tok.value in ["and", "or", "xor", "nand", "nor", "xnor"]:
            op = self.current_tok
        
            self.advance()
            
            node2, error = self.gtlt()
            if error:
                return None, error
            
            node1 = BinaryOpNode(node1, op, node2)
        return node1, None

    def plusminus(self):
        node1, error = self.muldiv()
        if error:
            return None, error
        
        return self.binaryoperation(node1, ["PLUS", "MINUS"], self.muldiv)
    
    def binaryoperation(self, node1, ops, lower):
        # Continously checks for operator
        while self.current_tok.type in ops:
            op = self.current_tok
        
            self.advance()
            
            node2, error = lower()
            if error:
                return None, error
            
            node1 = BinaryOpNode(node1, op, node2)
        return node1, None

###############
# INTERPRETER #
###############

class Interpreter():
    def __init__(self, node, lexer, index, symboltable):
        self.node = node
        self.lexer = lexer
        self.index = index
        self.symboltable = symboltable
        
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)
    
    def visit_NumberNode(self, node):
        return Number(node.tok.value, self.lexer), None
    
    def visit_StringNode(self, node):
        return String(node.tok.value, self.lexer), None
    
    def visit_VarDefNode(self, node):
        value, error = self.visit(node.value)
        if error:
            return None, error
        if node.key.value == "var":
            if node.name.value in self.symboltable.constants:
                return None, Error(305, Position(self.index, node.name.line, node.name.pos_start), Position(self.index, node.name.line, node.name.pos_end), f'Constant "{node.name.value}" already defined', self.lexer.text.split("\n")[node.pos_start.line])
            if node.eqtype.type == "EQ":
                self.symboltable.set(node.name.value, value)
            else:
                existing = self.symboltable.get(node.name)
                if existing is None:
                    return None, Error(304, Position(self.index, node.name.line, node.name.pos_start), Position(self.index, node.name.line, node.name.pos_end), f'Variable "{node.name.value}" not defined', self.lexer.text.split("\n")[node.pos_start.line])
                existing.lexer = self.lexer
                if node.eqtype.type == "PLUEQ":
                    new_value, error = existing.add(node, value)
                elif node.eqtype.type == "MINEQ":
                    new_value, error = existing.sub(node, value)
                elif node.eqtype.type == "MULEQ":
                    new_value, error = existing.mul(node, value)
                elif node.eqtype.type == "DIVEQ":
                    new_value, error = existing.div(node, value)
                elif node.eqtype.type == "EXPEQ":
                    new_value, error = existing.exp(node, value)
                elif node.eqtype.type == "MODEQ":
                    new_value, error = existing.mod(node, value)
                if error:
                    return None, error
                self.symboltable.set(node.name.value, new_value)
        else:
            existing = self.symboltable.get(node.name)
            if existing != None or node.eqtype.type != "EQ":
                return None, Error(305, Position(self.index, node.name.line, node.name.pos_start), Position(self.index, node.name.line, node.name.pos_end), f'Constant "{node.name.value}" already defined', self.lexer.text.split("\n")[node.pos_start.line])
            self.symboltable.set_constant(node.name.value, value)
            return value, None
        return value, None
    
    def visit_VarGetNode(self, node):
        value = self.symboltable.get(node.name)
        if value is None:
            return None, Error(304, node.pos_start, node.pos_end, f'Variable "{node.name.value}" not defined', self.lexer.text.split("\n")[node.pos_start.line])
        value.lexer = self.lexer
        return value, None
    
    def visit_IfNode(self, node):
        cond, error = self.visit(node.cond)
        if error:
            return None, error
        
        if cond.bool:
            for i in node.then:
                if not i:
                    continue
                res, error = self.visit(i)
        else:
            if node.elifs:
                res, error = self.visit(node.elifs)
                if error: return None, error
            elif node._else:
                for i in node._else:
                    if not i:
                        continue
                    res, error = self.visit(i)
            else:
                return None, None
        return res, error
    
    def visit_BinaryOpNode(self, node):
        node1, error = self.visit(node.node1)
        if error:
            return None, error
        node2, error = self.visit(node.node2)
        if error:
            return None, error
        if node.op.type == "PLUS":
            return node1.add(node, node2)
        elif node.op.type == "MINUS":
            return node1.sub(node, node2)
        elif node.op.type == "MUL":
            return node1.mul(node, node2)
        elif node.op.type == "DIV":
            return node1.div(node, node2)
        elif node.op.type == "EXP":
            return node1.exp(node, node2)
        elif node.op.type == "MOD":
            return node1.mod(node, node2)
        elif node.op.type == "EQEQ":
            return node1.eq(node, node2)
        elif node.op.type == "NEQ":
            return node1.neq(node, node2)
        elif node.op.type == "GT":
            return node1.gt(node, node2)
        elif node.op.type == "LT":
            return node1.lt(node, node2)
        elif node.op.type == "GTE":
            return node1.gte(node, node2)
        elif node.op.type == "LTE":
            return node1.lte(node, node2)
        elif node.op.type == "KEY":
            if node.op.value == "and":
                return node1._and(node, node2)
            elif node.op.value == "or":
                return node1._or(node, node2)
            elif node.op.value == "xor":
                return node1._xor(node, node2)
            elif node.op.value == "nand":
                return node1._nand(node, node2)
            elif node.op.value == "nor":
                return node1._nor(node, node2)
            elif node.op.value == "xnor":
                return node1._xnor(node, node2)

    def visit_UnaryOpNode(self, node):
        if node.op.type == "PLUS":
            return self.visit(node.node)
        if node.op.type == "MINUS":
            node1, error = self.visit(node.node)
            if error:
                return None, error
            return node1.mul(node, Number(-1, self.lexer))
        if node.op.type == "KEY" and node.op.value == "not":
            node1, error = self.visit(node.node)
            if error:
                return None, error
            return node1._not(node)