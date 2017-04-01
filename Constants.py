# Probobly Token.type.
ADD, SUB, MUL, DIV, MOD, POW = 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW'
LT, GT, LE, GE, EQ, NE = 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'
AND, OR, NOT = 'AND', 'OR', 'NOT'
LPAREN, RPAREN, ASSIGN, COMMA, SEMI = 'LPAREN', 'RPAREN', 'ASSIGN', 'COMMA', 'SEMI'
LBRACK, RBRACK, INDEX = 'LBRACK', 'RBRACK', 'INDEX'
LBRACE, RBRACE, NUM, NAME, EOF = 'LBRACE', 'RBRACE', 'NUM', 'NAME', 'EOF'
PRINT, FUNC, IF, ELSE, RETURN = 'PRINT', 'FUNC', 'IF', 'ELSE', 'RETURN'
WHILE, FOR, INPUT = 'WHILE', 'FOR', 'INPUT'
# Reseverd words.
RESERVED = {
    'print': PRINT,
    'func': FUNC,
    'if': IF,
    'else': ELSE,
    'return': RETURN,
    'while': WHILE,
    'for': FOR,
    'input': INPUT
}
# Symbols that has two characters.
TwoCharSymbols = {
    '>=': GE, '<=': LE, '==': EQ, '!=': NE, '&&': AND, '||': OR
}
# Symbols that has only one character.
OneCharSymbols = {
    '+': ADD, '-': SUB, '*': MUL, '/': DIV, '%': MOD, '^': POW,
    '>': GT, '<': LT,
    '(': LPAREN, ')': RPAREN, '=': ASSIGN, ',': COMMA,
    ';': SEMI, '{': LBRACE, '}': RBRACE,
    '[': LBRACK, ']': RBRACK,
    '!': NOT
}
# Binary Operators to Functions.
BinOp = {
    ADD: lambda a, b: a + b, SUB: lambda a, b: a - b,
    MUL: lambda a, b: a * b, DIV: lambda a, b: a / b,
    MOD: lambda a, b: a % b, POW: lambda a, b: a ** b,
    GT: lambda a, b: a > b, LT: lambda a, b: a < b,
    GE: lambda a, b: a >= b, LE: lambda a, b: a <= b,
    EQ: lambda a, b: a == b, NE: lambda a, b: a != b,
    AND: lambda a, b: a and b, OR: lambda a, b: a or b,
    INDEX: lambda a, b: a[int(b)]
}
# Unit Operators to Functions.
UnaryOp = {
    ADD: lambda a: +a,
    SUB: lambda a: -a,
    NOT: lambda a: not a
}
# Priorities of operators.
Prio = {
    ASSIGN: 8,
    OR: 7,
    AND: 6,
    EQ: 5, NE: 5,
    LT: 4, GT: 4, LE: 4, GE: 4,
    ADD: 3, SUB: 3,
    MUL: 2, DIV: 2, MOD: 2,
    POW: 1
}
Max_Priority = 8
RightAssoc = 'RightAssoc'
LeftAssoc = 'LeftAssoc'
Associativity = [
    None,
    RightAssoc,  # '^'
    LeftAssoc,   # '*' '/' '%'
    LeftAssoc,   # '+' '-'
    LeftAssoc,   # '>' '<' '>=' '<='
    LeftAssoc,   # '==' '!='
    LeftAssoc,   # '&&'
    LeftAssoc,   # '||'
    RightAssoc   # '='
]
BeginBlockSymbols = [LBRACE, LPAREN, LBRACK]
EndBlockSymbols = [RBRACE, RPAREN, RBRACK]
VERSION = '3.2'
