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
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_COMMA = "COMMA"
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
KEYS = ["var", "const", "unpack", "and", "or", "nor", "xor", "nand", "xnor", "not", "if", "elif", "else", "in", "func", "cfunc", "return"]

# Characters
DIGITS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
LETTERS_DIGITS = LETTERS + DIGITS

############
# POSITION #
############

class Position():
    def __init__(self, index, line, column, source):
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
        if self.error_code == 306:
            self.error_name = "CallError"
        if self.error_code == 307:
            self.error_name = "ReturnError"
        if self.error_code == 308:
            self.error_name = "UnpackError"
        if self.error_code == 309:
            self.error_name = "IndexError"
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details
        self.content = content
        self.source = self.pos_start.source
        
    def __repr__(self):
        # print(self.source.pos_start)
        if self.source != "<file>":
            error = []
            result = ""
            result += cs(f"Error {self.error_code} - {self.error_name}: {self.details}\n", "rgb(250,100,100)")
            result += cs(f"   File {self.pos_start.index} in {self.source.var.value}, line {self.pos_start.line + 1}\n", "rgb(250, 150, 150)")
            result += cs(f"      {self.content[self.pos_start.line]}\n", "rgb(250, 165, 165)")
            result += cs(f"      " + " " * (self.pos_start.column) + ("^" * (self.pos_end.column - self.pos_start.column + 1)), "rgb(250, 180, 180)")
            result += "\n"
            error.append(result)
            while self.source != "<file>":
                result = ""
                try:
                    result += cs(f"   File {self.pos_start.index} in {self.source.pos_start.source.var.value}, line {self.source.pos_start.line + 1}\n", "rgb(250, 150, 150)")
                except:
                    result += cs(f"   File {self.pos_start.index} in {self.source.pos_start.source}, line {self.source.pos_start.line + 1}\n", "rgb(250, 150, 150)")
                result += cs(f"      {self.content[self.source.pos_start.line]}\n", "rgb(250, 165, 165)")
                result += cs(f"      " + " " * (self.source.pos_start.column) + ("^" * (self.source.pos_end.column - self.source.pos_start.column + 1)) + "\n", "rgb(250, 180, 180)")
                self.source = self.source.pos_start.source
                error.append(result)
            string = ""
            error.append(cs("Traceback:\n", "rgb(250, 100, 100)"))
            error.reverse()
            for i in error:
                string += i
            return string[:-1]
        else:
            result = cs(f"Error {self.error_code} - {self.error_name}: {self.details}\n", "rgb(250,100,100)")
            result += cs(f"   File {self.pos_start.index} in {self.source}, line {self.pos_start.line + 1}\n", "rgb(250, 150, 150)")
            result += cs(f"      {self.content[self.pos_start.line]}\n", "rgb(250, 165, 165)")
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
    def __init__(self, tok, index, source):
        self.tok = tok
        self.pos_start = Position(index, self.tok.line, self.tok.pos_start, source)
        self.pos_end = Position(index, self.tok.line, self.tok.pos_end, source)
        
    def __repr__(self):
        return f"{self.tok}"
    
class StringNode():
    def __init__(self, tok, index, source):
        self.tok = tok
        self.pos_start = Position(index, self.tok.line, self.tok.pos_start, source)
        self.pos_end = Position(index, self.tok.line, self.tok.pos_end, source)
        
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
    
class ListNode():
    def __init__(self, l, contents, r, index, source):
        self.l = l
        self.r = r
        self.contents = contents
        self.pos_start = Position(index, l.line, l.pos_start, source)
        self.pos_end = Position(index, r.line, r.pos_end, source)

class IfNode():
    def __init__(self, cond, then, pos_end, elifs=None, _else=None, source="<file>"):
        self.cond = cond
        self.then = then
        self.elifs = elifs
        self._else = _else
        self.pos_end = Position(None, pos_end, pos_end, source)

    def __repr__(self):
        return f'if {self.cond} then {self.then} elif {self.elifs} else {self._else}'
    
class FuncDefNode():
    def __init__(self, key, ident, args, then, pos_end, source="<file>"):
        self.key = key
        self.ident = ident
        self.args = args
        self.then = then
        self.pos_end = Position(None, pos_end, pos_end, source)

    def __repr__(self):
        return f'{self.key} {self.ident}({str(self.args)}) -> {self.then}'
    
class ReturnNode():
    def __init__(self, key, nodes, pos_end,index, source):
        self.key = key
        self.nodes = nodes
        self.pos_start = Position(index, self.key.line, self.key.pos_start, source)
        self.pos_end = Position(index, self.key.line, pos_end, source)

    def __repr__(self):
        return f'return {self.nodes}'

class UnaryOpNode():
    def __init__(self, op, node, index, source):
        self.op = op
        self.node = node
        self.pos_start = Position(index, self.op.line, self.op.pos_start, source)
        self.pos_end = self.node.pos_end
        
    def __repr__(self):
        return f"({self.op} {self.node})"
    
class ListCallNode():
    def __init__(self, node, call, rsquare, index, source):
        self.node = node
        self.call = call
        self.pos_start = self.node.pos_start
        self.pos_end = Position(index, rsquare.line, rsquare.pos_end, source)
        
    def __repr__(self):
        return f"({self.node}[{self.call}])"
    
class VarDefNode():
    def __init__(self, key, name, eqtype, value, pos_end, index, source):
        self.key = key
        self.name = name
        self.eqtype = eqtype
        self.op = eqtype
        self.value = value
        self.node2 = value
        self.pos_start = Position(index, self.key.line, self.key.pos_start, source)
        self.pos_end = pos_end
        self.pos_end.column -= 1
        
    def __repr__(self):
        return f"({self.key} {self.name} {self.eqtype} {self.value})"
    
class UnpackNode():
    def __init__(self, key, name, eqtype, value, pos_end, index, source):
        self.key = key
        self.name = name
        self.eqtype = eqtype
        self.op = eqtype
        self.value = value
        self.node2 = value
        self.pos_start = Position(index, self.key.line, self.key.pos_start, source)
        self.pos_end = pos_end
        self.pos_end.column -= 1
        
    def __repr__(self):
        return f"({self.key} {self.name} {self.eqtype} {self.value})"
    
class CallNode():
    def __init__(self, var, args, pos_end, index, source):
        self.var= var
        self.args = args
        self.pos_start = Position(index, self.var.line, self.var.pos_start, source)
        self.pos_end = Position(index, self.var.line, pos_end, source)

class VarGetNode():
    def __init__(self, name, index, source):
        self.name = name
        self.pos_start = Position(index, self.name.line, self.name.pos_start, source)
        self.pos_end = Position(index, self.name.line, self.name.pos_end, source)
        
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
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def sub(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def mul(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def div(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

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
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def gt(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value > other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def gte(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value >= other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def lte(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(self.value <= other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def _in(self, node, other):
        if isinstance(other, List):
            for i in other.value:
                res, error = self.eq(node, i)
                if error:
                    return None, error
                if res.bool:
                    return Boolean(1, self.lexer), None
            return Boolean(0, self.lexer), None
        if isinstance(other, String):
            if str(self.value) in other.value:
                return Boolean(1, self.lexer), None
            return Boolean(0, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def exp(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def mod(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
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
        self.value = None

    def lt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def gt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def gte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def lte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def __repr__(self):
        return "None"

class Function(Value):
    def __init__(self, name, args, value, lexer):
        super().__init__(value, lexer)
        self.bool = True
        self.args = args
        self.name = name

    def lt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def gt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def gte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def lte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def __repr__(self):
        return f'<Function {self.name.value}>'

class Boolean(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)
        self.value = self.bool

    def lt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def gt(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def gte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def lte(self, node, other):
        return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def __repr__(self):
        return "True" if self.value else "False"
    
class List(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)
        self.bool = True

    def eq(self, node, other):
        if other.__class__.__name__ == "List":
            if len(self.value) == len(self.value):
                for i in range(len(self.value)):
                    eq, error = self.value[i].eq(node, other.value[i])
                    if not(eq.bool):
                        return Boolean(0, self.lexer), None
                return Boolean(1, self.lexer), None
        return Boolean(0, self.lexer), None

    def lt(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(len(self.value) < len(other.value), self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def gt(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(len(self.value) > len(other.value), self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def gte(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(len(self.value) >= len(other.value), self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def lte(self, node, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return Boolean(len(self.value) <= len(other.value), self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def neq(self, node, other):
        eq, error = self.eq(node, other)
        if error:
            return None, error
        return Boolean(int(not(eq.value)), self.lexer), None

    def add(self, node, other):
        if isinstance(other, List):
            return List(self.value + other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def mul(self, node, other):
        if isinstance(other, Number):
            try:
                return List(self.value * other.value, self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of List and non-integer', self.lexer.text.split("\n"))
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def sub(self, node, other):
        if isinstance(other, Number):
            if other.value > len(self.value):
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of List and number longer than length', self.lexer.text.split("\n"))
            try:
                if other.value > 0:
                    return List(self.value[:-other.value], self.lexer), None
                if other.value == 0:
                    return self, None
                return List(self.value[-other.value:], self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of List and non-integer', self.lexer.text.split("\n"))
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def __repr__(self):
        return f"{self.value}"

class String(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)
        self.bool = True
        
    def add(self, node, other):
        if isinstance(other, Number) or isinstance(other, String):
            return String(self.value + str(other.value), self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def mul(self, node, other):
        if isinstance(other, Number):
            try:
                return String(self.value * other.value, self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of String and non-integer', self.lexer.text.split("\n"))
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def sub(self, node, other):
        if isinstance(other, Number):
            if other.value > len(self.value):
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of String and number longer than length', self.lexer.text.split("\n"))
            try:
                return String(self.value[:-other.value], self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of String and non-integer', self.lexer.text.split("\n"))
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
    
    def __repr__(self):
        return f"{self.value}"

class Number(Value):
    def __init__(self, value, lexer):
        super().__init__(value, lexer)
        if self.value % 1 == 0:
            self.value = int(self.value)
        self.bool = True

    def _in(self, node, other):
        if isinstance(other, List):
            for i in other.value:
                res, error = self.eq(node, i)
                if error:
                    return None, error
                if res.bool:
                    return Boolean(1, self.lexer), None
            return Boolean(0, self.lexer), None
        if isinstance(other, String) or isinstance(other, Number):
            if str(self.value) in str(other.value):
                return Boolean(1, self.lexer), None
            return Boolean(0, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def add(self, node, other):
        if isinstance(other, Number):
            return Number(self.value + other.value, self.lexer), None
        elif isinstance(other, String):
            return String(str(self.value) + other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def sub(self, node, other):
        if isinstance(other, Number):
            return Number(self.value - other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def mul(self, node, other):
        if isinstance(other, Number):
            return Number(self.value * other.value, self.lexer), None
        elif isinstance(other, String):
            try:
                return String(str(other.value) * self.value, self.lexer), None
            except:
                return None, Error(303, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, f'Invalid operation of String and non-integer', self.lexer.text.split("\n"))
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def div(self, node, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Error(302, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, 'Division by zero', self.lexer.text.split("\n"))
            return Number(self.value / other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def exp(self, node, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))
        
    def mod(self, node, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Error(302, Position(self.lexer.index, node.op.line, node.op.pos_start, node.node2.pos_end.source), node.node2.pos_end, 'Division by zero', self.lexer.text.split("\n"))
            return Number(self.value % other.value, self.lexer), None
        else:
            return None, Error(301, node.pos_start, node.pos_end, f'Unsupported operation between {self.__class__.__name__} and {other.__class__.__name__}', self.lexer.text.split("\n"))

    def __repr__(self):
        return f"{self.value}"
    
###############
# SYMBOLTABLE #
###############

class SymbolTable():
    def __init__(self, parent=None):
        self.symbols = {}
        self.constants = {"None": NoneType(None), "True": Boolean(1, None), "False": Boolean(0, None), "print": Function(Token(TT_STR, "print", None, None), ["value"], None, None), "until": Function(Token(TT_STR, "until", None, None), ["value1", "value2"], None, None)}
        self.parent = parent
        
    def get(self, name):
        value = self.symbols.get(name.value, None)
        if value is None and self.parent:
            return self.parent.get(name)
        if value == None:
            value = self.constants.get(name.value, None)
            if value is None and self.parent:
                return self.parent.get(name)
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
    def __init__(self, text, index, source ="<file>"):
        self.text = text
        self.index = index
        self.source = source
        
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
                        return None, Error(101, Position(self.index, linepos, pos_start, self.source), Position(self.index, linepos, pos_start, self.source), f'Illegal character "!"', self.text.split("\n"))
                elif j == ":":
                    line.append(Token(TT_COLON, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == "]":
                    line.append(Token(TT_RSQUARE, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == "[":
                    line.append(Token(TT_LSQUARE, None, linepos, pos))
                    pos += 1
                    j = i[pos]
                elif j == ",":
                    line.append(Token(TT_COMMA, None, linepos, pos))
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
                            return None, Error(103, Position(self.index, linepos, pos_start, self.source), Position(self.index, linepos, pos_start, self.source), f'Unresolved string literal', self.text.split("\n"))
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
                                return None, Error(102, Position(self.index, linepos, pos, self.source), Position(self.index, linepos, pos, self.source), "Too many dots in number", self.text.split("\n"))
                        num += j
                        pos += 1
                        j = i[pos]
                    # Check for errors
                    if num[-1] == ".":
                        return None, Error(102, Position(self.index, linepos, pos-1, self.source), Position(self.index, linepos, pos-1, self.source), "Number cannot end with a dot", self.text.split("\n"))
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
                    return None, Error(101, Position(self.index, linepos, pos, self.source), Position(self.index, linepos, pos, self.source), f'Illegal character "{j}"', self.text.split("\n"))
            # Add EOF Token
            line.append(Token(TT_EOF, None, linepos, pos, pos))
            # Reattach line to output
            out.append(line)
        return out, None
    
##########
# PARSER #
##########

class Parser():
    def __init__(self, tokens, index, lexer, source="<file>"):
        self.tokens = tokens
        self.index = index
        self.lexer = lexer
        self.source = source
        
    def advance(self):
        if self.current_tok.type != "EOF":
            self.current_tok = self.tokens[self.tokens.index(self.current_tok) + 1]
            return self.current_tok
        return None
        
    def parse(self):
        self.current_tok = self.tokens[0]
        if self.current_tok.type == "EOF":
            return None, None
        node, error = self.expr()
        if error:
            return None, error
        if self.current_tok.type != "EOF":
            return None, Error(203, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Conjoined expression', self.lexer.text.split("\n"))
        return node, None
    
    def expr(self):
        if self.current_tok.type == "KEY" and self.current_tok.value in ["var", "const", 'if', 'func', 'cfunc', 'return', "unpack"]:
            if self.current_tok.value in ["var", "const"]:
                node, error = self.var(self.current_tok)
            if self.current_tok.value == "unpack":
                node, error = self.unpack(self.current_tok)
            elif self.current_tok.value == "if":
                node, error = self.ifexpr(self.current_tok.line)
            elif self.current_tok.value in ["func", "cfunc"]:
                node, error = self.funcexpr(self.current_tok)
            elif self.current_tok.value == "return":
                node, error = self.returnexpr(self.current_tok)
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
    
    def unpack(self, key):
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: ":"', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
        pos_start = self.current_tok.pos_start
        self.advance()
        names = []
        if self.current_tok.type == "IDENT":
            names.append(self.current_tok)
            self.advance()
            while self.current_tok.type == "COMMA":
                self.advance()
                if self.current_tok.type != "IDENT":
                    return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: IDENT', self.lexer.text.split("\n"))
                names.append(self.current_tok)
                self.advance()
            if self.current_tok.type != "COMMA" and self.current_tok.type != "EQ":
                if self.current_tok.type == "EOF":
                    return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
                return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: ","', self.lexer.text.split("\n"))
        else:
            if self.current_tok.type != "RBRACE":
                return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: IDENT', self.lexer.text.split("\n"))
        if self.current_tok.type != "EQ":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: "="', self.lexer.text.split("\n"))
        eqtype = self.current_tok
        self.advance()
        node, error = self.andor()
        if error:
            return None, error
        if self.current_tok.type != "RBRACE":
            return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
        pos_end = Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source)
        self.advance()
        return UnpackNode(key, names, eqtype, node, pos_end, self.index, self.source), None
    
    def var(self, key):
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: ":"', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
        pos_start = self.current_tok.pos_start
        self.advance()
        if self.current_tok.type != "IDENT":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: "IDENT"', self.lexer.text.split("\n"))
        name = self.current_tok
        self.advance()
        if self.current_tok.type not in ["EQ", "PLUEQ", "MINEQ", "MULEQ", "DIVEQ", "EXPEQ", "MODEQ"]:
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: "="', self.lexer.text.split("\n"))
        eqtype = self.current_tok
        self.advance()
        node, error = self.andor()
        if error:
            return None, error
        if self.current_tok.type != "RBRACE":
            return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
        pos_end = Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source)
        self.advance()
        return VarDefNode(key, name, eqtype, node, pos_end, self.index, self.source), None
        
    def ifexpr(self, line):
        elifs = None
        _else = None
        tokens, error = Lexer(self.lexer.text, self.index).lex()
        if error:
            return None, error
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: ":"', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
        pos_start = self.current_tok.pos_start
        self.advance()
        cond, error = self.andor()
        if error:
            return None, error
        if self.current_tok.type != "RBRACE":
            return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
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
                return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
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
        return IfNode(cond, then, line, elifs, _else, self.source), None
    
    def returnexpr(self, tok):
        self.advance()
        if self.current_tok.type != "COLON":
            return ReturnNode(tok, [], tok.pos_end, self.index, self.source), None
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
        pos_start = self.current_tok.pos_start
        self.advance()
        nodes = []
        while self.current_tok.type != "RBRACE":
            node, error = self.andor()
            if error:
                return None, error
            if self.current_tok.type != "COMMA" and self.current_tok.type != "RBRACE":
                if self.current_tok.type == "EOF":
                    return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
                return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: ","', self.lexer.text.split("\n"))
            nodes.append(node)
            if self.current_tok.type == "RBRACE":
                rsquare = self.current_tok
                self.advance()
                break
            self.advance()
        return ReturnNode(tok, nodes, rsquare.pos_end, self.index, self.source), None
    
    def funcexpr(self, tok):
        tokens, error = Lexer(self.lexer.text, self.index).lex()
        if error:
            return None, error
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: ":"', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
        pos_start = self.current_tok.pos_start
        self.advance()
        if self.current_tok.type != "IDENT":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: IDENT', self.lexer.text.split("\n"))
        ident = self.current_tok
        self.advance()
        if self.current_tok.type != "LPAREN":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "("', self.lexer.text.split("\n"))
        pos_start_2 = self.current_tok.pos_start
        self.advance()
        args = []
        if self.current_tok.type == "IDENT":
            args.append(self.current_tok)
            self.advance()
            while self.current_tok.type == "COMMA":
                self.advance()
                if self.current_tok.type != "IDENT":
                    return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: IDENT', self.lexer.text.split("\n"))
                args.append(self.current_tok)
                self.advance()
            if self.current_tok.type != "COMMA" and self.current_tok.type != "RPAREN":
                if self.current_tok.type == "RBRACE":
                    return None, Error(201, Position(self.index, self.current_tok.line, pos_start_2, self.source), Position(self.index, self.current_tok.line, pos_start_2, self.source), 'Unresolved grouping: "("', self.lexer.text.split("\n"))
                return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: ","', self.lexer.text.split("\n"))
        else:
            if self.current_tok.type != "RPAREN":
                return None, Error(201, Position(self.index, self.current_tok.line, pos_start_2, self.source), Position(self.index, self.current_tok.line, pos_start_2, self.source), 'Unresolved grouping: "("', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "RBRACE":
            return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n"))
        pos_start = self.current_tok.pos_start
        linepos = self.current_tok.line
        self.advance()
        then = []
        finished = False
        toks = self.tokens
        if self.current_tok.type != "EOF":
            node, error = self.expr()
            if error:
                return None, error
            then.append(node)
            self.tokens = toks
            if self.current_tok.type == "RBRACE":
                finished = True
                self.advance()
        line = self.current_tok.line - 1
        if finished == False:
            line += 1
        tokens, line, then, finished = self.multiline(tokens, line, then, linepos, pos_start, finished)
        if not tokens:
            return None, line
        if finished == False:
                return None, Error(201, Position(self.index, self.current_tok.line, pos_start, self.source), Position(self.index, self.current_tok.line, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n"))
        return FuncDefNode(tok, ident, args, then, line, self.source), None
    
    def elseexpr(self, tokens, line):
        self.advance()
        if self.current_tok.type != "COLON":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Expected token: ":"', self.lexer.text.split("\n")), None
        self.advance()
        if self.current_tok.type != "LBRACE":
            return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: "{"', self.lexer.text.split("\n")), None
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
                return None, Error(201, Position(self.index, linepos, pos_start, self.source), Position(self.index, linepos, pos_start, self.source), 'Unresolved grouping: "{"', self.lexer.text.split("\n")), None, None
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
            return NumberNode(num, self.index, self.source), None
        elif self.current_tok.type == "IDENT":
            # Variables
            var = self.current_tok
            self.advance()
            if self.current_tok.type == "LPAREN":
                lsquare = self.current_tok
                self.advance()
                args = []
                if self.current_tok.type == "RPAREN":
                    pos_end = self.current_tok.pos_end
                    self.advance()
                    return CallNode(var, args, pos_end, self.index, self.source), None
                while self.current_tok.type != "RPAREN":
                    node, error = self.andor()
                    if error:
                        return None, error
                    args.append(node)
                    if self.current_tok.type != "COMMA" and self.current_tok.type != "RPAREN":
                        if self.current_tok.type == "EOF":
                            return None, Error(201, Position(self.index, lsquare.line, lsquare.pos_start, self.source), Position(self.index, lsquare.line, lsquare.pos_end, self.source), 'Unresolved grouping: "("', self.lexer.text.split("\n"))
                        return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: ","', self.lexer.text.split("\n"))
                    if self.current_tok.type == "RPAREN":
                        pos_end = self.current_tok.pos_end
                        self.advance()
                        break
                    self.advance()
                return CallNode(var, args, pos_end, self.index, self.source), None
            return VarGetNode(var, self.index, self.source), None
        elif self.current_tok.type == "STR":
            # Strings
            string = self.current_tok
            self.advance()
            return StringNode(string, self.index, self.source), None
        elif self.current_tok.type == "LSQUARE":
            # Lists
            lsquare = self.current_tok
            self.advance()
            contents = []
            if self.current_tok.type == "RSQUARE":
                rsquare = self.current_tok
                self.advance()
            else:
                while self.current_tok.type != "RSQUARE":
                    node, error = self.andor()
                    if error:
                        return None, error
                    if self.current_tok.type != "COMMA" and self.current_tok.type != "RSQUARE":
                        if self.current_tok.type == "EOF":
                            return None, Error(201, Position(self.index, lsquare.line, lsquare.pos_start, self.source), Position(self.index, lsquare.line, lsquare.pos_end, self.source), 'Unresolved grouping: "["', self.lexer.text.split("\n"))
                        return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected token: ","', self.lexer.text.split("\n"))
                    contents.append(node)
                    if self.current_tok.type == "RSQUARE":
                        rsquare = self.current_tok
                        self.advance()
                        break
                    self.advance()
            return ListNode(lsquare, contents, rsquare, self.index, self.source), None
        elif self.current_tok.type == "LPAREN":
            # Parentheses
            lparen = self.current_tok
            self.advance()
            if self.current_tok.type == "RPAREN":
                # Empty Group
                return None, Error(204, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), 'Expected expression', self.lexer.text.split("\n"))
            node, error = self.andor()
            if error:
                return None, error
            if self.current_tok.type != "RPAREN":
                # Unclosed Group
                return None, Error(201, Position(self.index, lparen.line, lparen.pos_start, self.source), Position(self.index, lparen.line, lparen.pos_end, self.source), 'Unresolved grouping: "("', self.lexer.text.split("\n"))
            node.pos_start = Position(self.index, lparen.line, lparen.pos_start, self.source)
            node.pos_end = Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source)
            self.advance() 
            return node, None
        elif (self.current_tok.type in ["PLUS", "MINUS"]) or (self.current_tok.type == "KEY" and self.current_tok.value == "not"):
            # Unary Operations
            op = self.current_tok
            self.advance()
            node, error = self.list_call()
            if error:
                return None, error
            return UnaryOpNode(op, node, self.index, self.source), None
        else:
            return None, Error(202, Position(self.index, self.current_tok.line, self.current_tok.pos_start, self.source), Position(self.index, self.current_tok.line, self.current_tok.pos_end, self.source), f'Unexpected token: "{self.current_tok}"', self.lexer.text.split("\n"))

    def list_call(self):
        _object, error = self.num()
        if error:
            return None, error
        while self.current_tok.type == "LSQUARE":
            lsquare = self.current_tok
            self.advance()
            call, error = self.andor()
            if error: return None, error
            if self.current_tok.type != "RSQUARE":
                return None, Error(201, Position(self.index, lsquare.line, lsquare.pos_start, self.source), Position(self.index, lsquare.line, lsquare.pos_end, self.source), 'Unresolved grouping: "["', self.lexer.text.split("\n"))
            rsquare = self.current_tok
            self.advance()
            _object = ListCallNode(_object, call, rsquare, self.index, self.source)
        return _object, None

    def exp(self):
        node1, error = self.list_call()
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
        while (self.current_tok.type == "KEY" and self.current_tok.value == 'in') or self.current_tok.type in ["GT", "LT", "GTE", "LTE", "EQEQ", "NEQ"]:
            op = self.current_tok
    
            self.advance()
            
            node2, error = self.plusminus()
            if error:
                return None, error
            
            node1 = BinaryOpNode(node1, op, node2)
        return node1, None
    
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
    def __init__(self, node, lexer, index, symboltable, source="<file>"):
        self.node = node
        self.lexer = lexer
        self.index = index
        self.symboltable = symboltable
        self.source = source
        
    def visit(self, node):
        try:
            node.pos_start.source = self.source
        except:
            pass
        node.pos_end.source = self.source
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)
    
    def visit_NumberNode(self, node):
        return Number(node.tok.value, self.lexer), None

    def visit_ListNode(self, node):
        contents = []
        for i in node.contents:
            res, error = self.visit(i)
            if error:
                return None, error
            contents.append(res)
        return List(contents, self.lexer), None
    
    def visit_StringNode(self, node):
        return String(node.tok.value, self.lexer), None
    
    def visit_VarDefNode(self, node):
        value, error = self.visit(node.value)
        if error:
            return None, error
        if node.key.value == "var":
            if node.name.value in self.symboltable.constants:
                return None, Error(305, Position(self.index, node.name.line, node.name.pos_start, self.lexer.source), Position(self.index, node.name.line, node.name.pos_end, self.lexer.source), f'Constant "{node.name.value}" already defined', self.lexer.text.split("\n"))
            if node.eqtype.type == "EQ":
                self.symboltable.set(node.name.value, value)
            else:
                existing = self.symboltable.get(node.name)
                if existing is None:
                    return None, Error(304, Position(self.index, node.name.line, node.name.pos_start, self.lexer.source), Position(self.index, node.name.line, node.name.pos_end, self.lexer.source), f'Variable "{node.name.value}" not defined', self.lexer.text.split("\n"))
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
                value = new_value
        else:
            existing = self.symboltable.get(node.name)
            if existing != None or node.eqtype.type != "EQ":
                return None, Error(305, Position(self.index, node.name.line, node.name.pos_start, self.lexer.source), Position(self.index, node.name.line, node.name.pos_end, self.lexer.source), f'Constant "{node.name.value}" already defined', self.lexer.text.split("\n"))
            self.symboltable.set_constant(node.name.value, value)
            return value, None
        return value, None
    
    def visit_VarGetNode(self, node):
        value = self.symboltable.get(node.name)
        if value is None:
            return None, Error(304, node.pos_start, node.pos_end, f'Variable "{node.name.value}" not defined', self.lexer.text.split("\n"))
        value.lexer = self.lexer
        return value, None
    
    def visit_FuncDefNode(self, node):
        value = Function(node.ident, node.args, node.then, self.lexer)
        if node.key.value == "func":
            if node.ident.value in self.symboltable.constants:
                return None, Error(305, Position(self.index, node.ident.line, node.ident.pos_start, self.lexer.source), Position(self.index, node.ident.line, node.ident.pos_end, self.lexer.source), f'Constant "{node.ident.value}" already defined', self.lexer.text.split("\n"))
            self.symboltable.set(node.ident.value, value)
        else:
            existing = self.symboltable.get(node.ident)
            if existing != None:
                return None, Error(305, Position(self.index, node.ident.line, node.ident.pos_start, self.lexer.source), Position(self.index, node.ident.line, node.ident.pos_end, self.lexer.source), f'Constant "{node.ident.value}" already defined', self.lexer.text.split("\n"))
            self.symboltable.set_constant(node.ident.value, value)
        return value, None

    def visit_CallNode(self, node):
        func = self.symboltable.get(node.var)
        if func is None:
            return None, Error(304, node.pos_start, node.pos_end, f'Function "{node.var.value}" not defined', self.lexer.text.split("\n"))
        if func.name.value == "until":
            args = []
            for i in node.args:
                res, error = self.visit(i)
                if error:
                    return None, error
                args.append(res)
            if len(args) not in [1, 2]:
                waswere = "were"
                if len(args) == 1:
                    waswere = "was"
                s = "s"
                if len(func.args) == 1:
                    s = ""
                return None, Error(306, node.pos_start, node.pos_end, f'Function {func.name.value} takes {len(func.args)} argument{s}; {len(node.args)} {waswere} given instead', self.lexer.text.split("\n"))
            value = []
            try:
                if len(args) > 1:
                    for i in range(args[0].value, args[1].value):
                        value.append(Number(i, self.lexer))
                else:
                    for i in range(args[0].value):
                        value.append(Number(i, self.lexer))
            except:
                return None, Error(306, node.pos_start, node.pos_end, f'Function {func.name.value} takes whole integer arguments', self.lexer.text.split("\n"))
            return List(value, self.lexer), None
        if not isinstance(func, Function):
            return None, Error(306, node.pos_start, node.pos_end, f'Type {func.__class__.__name__} is not callable', self.lexer.text.split("\n"))
        lexer = Lexer(self.lexer.text, self.index, node)
        tokens, error = lexer.lex()
        symboltable = SymbolTable(self.symboltable)
        if len(node.args) != (len(func.args)):
            waswere = "were"
            if len(node.args) == 1:
                waswere = "was"
            s = "s"
            if len(func.args) == 1:
                s = ""
            return None, Error(306, node.pos_start, node.pos_end, f'Function {func.name.value} takes {len(func.args)} argument{s}; {len(node.args)} {waswere} given instead', self.lexer.text.split("\n"))
        if func.name.value == "print":
            res, error = self.visit(node.args[0])
            if error:
                return None, error
            print(res)
            return NoneType(self.lexer), None
        for i in node.args:
            arg, error = self.visit(i)
            if error:
                return None, error
            symboltable.set(func.args[node.args.index(i)].value, arg)
        interpreter = Interpreter(None, lexer, self.index, symboltable, node)
        for i in func.value:
            if not i:
                continue
            if isinstance(i, ReturnNode):
                if i.nodes == []:
                    return NoneType(self.lexer), None
                elif len(i.nodes) == 1:
                    res, error = interpreter.visit(i.nodes[0])
                    if error:
                        return None, error
                    return res, None
                else:
                    result = []
                    for j in i.nodes:
                        res, error = interpreter.visit(j)
                        if error:
                            return None, error
                        result.append(res)
                    return List(result, self.lexer), None
            res, error = interpreter.visit(i)
            if error:
                if error.error_code == 307:
                    i = res
                    if i.nodes == []:
                        return NoneType(self.lexer), None
                    elif len(i.nodes) == 1:
                        res, error = interpreter.visit(i.nodes[0])
                        if error:
                            return None, error
                        return res, None
                    else:
                        result = []
                        for j in i.nodes:
                            res, error = interpreter.visit(j)
                            if error:
                                return None, error
                            result.append(res)
                        return List(result, self.lexer), None
                else:
                    return None, error
        return None, None
    
    def visit_UnpackNode(self, node):
        value, error = self.visit(node.value)
        if error:
            return None, error

        if len(node.name) < 2:
            return None, Error(308, Position(self.index, node.name[0].line, node.name[0].pos_start, self.lexer.source), Position(self.index, node.name[0].line, node.name[0].pos_end, self.lexer.source), f'Cannot unpack 1 item', self.lexer.text.split("\n"))
        
        if not isinstance(value, List):
            return None, Error(308, node.value.pos_start, node.value.pos_end, f'Cannot unpack non-iterable {value.__class__.__name__}', self.lexer.text.split("\n"))
        
        if len(node.name) != len(value.value):
            return None, Error(308, Position(self.index, node.name[0].line, node.name[0].pos_start, self.lexer.source), node.value.pos_end, f'Cannot unpack {len(value.value)} values into {len(node.name)} objects', self.lexer.text.split("\n"))
        
        for i in node.name:
            if i.value in self.symboltable.constants:
                return None, Error(305, Position(self.index, i.line, i.pos_start, self.lexer.source), Position(self.index, i.line, i.pos_end, self.lexer.source), f'Constant "{i.value}" already defined', self.lexer.text.split("\n"))
            self.symboltable.set(i.value, value.value[node.name.index(i)])
        return None, None
    
    def visit_ReturnNode(self, node):
        return node, Error(307, node.pos_start, node.pos_end, f'Return must be used in a function', self.lexer.text.split("\n"))
    
    def visit_ListCallNode(self, node):
        tocall, error = self.visit(node.node)
        if error: return None, error
        if not (isinstance(tocall, List) or isinstance(tocall, String)):
            return None, Error(309, node.pos_start, node.node.pos_end, f"Cannot index type {tocall.__class__.__name__}", self.lexer.text.split("\n"))
        index, error = self.visit(node.call)
        if error:
            return None ,error
        if not isinstance(index, Number):
            return None, Error(309, node.call.pos_start, node.call.pos_end, f"Cannot index with type {index.__class__.__name__}", self.lexer.text.split("\n"))
        if index.value % 1 != 0:
            return None, Error(309, node.call.pos_start, node.call.pos_end, f"Cannot index with non-integer", self.lexer.text.split("\n"))
        if (index.value > -1 and len(tocall.value)-1 < index.value) or (index.value < 0 and len(tocall.value) < -1 * index.value):
            return None, Error(309, node.call.pos_start, node.call.pos_end, f"Out of index range", self.lexer.text.split("\n"))
        return tocall.value[index.value], None
    
    def visit_IfNode(self, node):
        cond, error = self.visit(node.cond)
        if error:
            return res, error
        
        if cond.bool:
            for i in node.then:
                if not i:
                    continue
                res, error = self.visit(i)
                if error:
                    return res, error
        else:
            if node.elifs:
                res, error = self.visit(node.elifs)
                if error: return res, error
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
            elif node.op.value == "in":
                return node1._in(node, node2)

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