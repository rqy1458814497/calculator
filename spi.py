##############################################################
# Constants                                                  #
##############################################################

# Probobly Token.type.
ADD, SUB, MUL, DIV, MOD, POW = 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW'
LT, GT, LE, GE, EQ, NE = 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'
AND, OR, NOT = 'AND', 'OR', 'NOT'
LPAREN, RPAREN, ASSIGN, COMMA, SEMI = 'LPAREN', 'RPAREN', 'ASSIGN', 'COMMA', 'SEMI'
LBRACK, RBRACK, INDEX = 'LBRACK', 'RBRACK', 'INDEX'
LBRACE, RBRACE, NUM, NAME, STRING = 'LBRACE', 'RBRACE', 'NUM', 'NAME', 'STRING'
PRINT, FUNC, IF, ELSE, RETURN = 'PRINT', 'FUNC', 'IF', 'ELSE', 'RETURN'
WHILE, FOR, INPUT = 'WHILE', 'FOR', 'INPUT'
EOF = 'EOF'
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
EscapeCharacters = {
    'n': '\n', 't': '\t', 'r': '\r',
    '\'': '\'', '\"': '\"', '\\': '\\',
    'a': '\a', 'b': '\b',
    'v': '\v', 'f': '\f'
}
BeginBlockSymbols = [LBRACE, LPAREN, LBRACK]
EndBlockSymbols = [RBRACE, RPAREN, RBRACK]
VERSION = '3.3'


##############################################################
# Lexer                                                      #
##############################################################

class Token(object):
    """Token type."""

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token(%s, %r)" % (self.type, self.value)

    __repr__ = __str__


class Lexer(object):
    """
        Lexer. Lexical analyzer.
        Interface: get_next_token(): Lexical analyze the next token;
                   get_local_text(): Get the lexical-analyzing local texts.
    """

    def __init__(self, text):
        self.text = text
        self.pos = 1
        self.current_char = text[0]

    def Error(self, errstr):
        raise SyntaxError(errstr)

    def advance(self):
        if self.pos == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.pos += 1

    def peek(self):
        if self.pos >= len(self.text) - 1:
            return None
        else:
            return self.text[self.pos]

    def get_local_text(self, length=5):
        ans = ''
        if self.pos - 1 - length > 0:
            ans += '...'
        ans += self.text[max(self.pos - 1 - length, 0): min(self.pos - 1 + length, len(self.text))]
        if self.pos - 1 + length < len(self.text):
            ans += '...'
        return ans

    def skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_NAME(self):
        ans = ''
        while self.current_char is not None and (self.current_char.isalpha() or
                                                 self.current_char == '_' or
                                                 self.current_char.isdigit()):
            ans += self.current_char
            self.advance()
        if ans in RESERVED:
            return Token(RESERVED[ans], ans)
        else:
            return Token(NAME, ans)

    def get_number(self):
        ans = ''
        while self.current_char is not None and self.current_char.isdigit():
            ans += self.current_char
            self.advance()
        if self.current_char == '.':
            ok = False
            ans += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                ans += self.current_char
                self.advance()
                ok = True
            if not ok:
                self.Error('Lexical analyze error at "%s"' % self.get_local_text())
        if self.current_char == 'e':
            ans += 'e'
            self.advance()
            if self.current_char == '-':
                ans += '-'
                self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                ans += self.current_char
                self.advance()
        return Token(NUM, float(ans))

    def get_string(self):
        endchar = self.current_char
        self.advance()
        ans = ''
        while self.current_char is not None and self.current_char != endchar:
            if self.current_char == '\\':
                self.advance()
                ch = self.current_char
                self.advance()
                if ch in EscapeCharacters:
                    ans += EscapeCharacters[ch]
                elif ch == 'o':
                    ch = self.current_char
                    self.advance()
                    ch += self.current_char
                    self.advance()
                    ans += chr(int(ch, 16))
                elif ch == 'x':
                    ch = self.current_char
                    self.advance()
                    ch += self.current_char
                    self.advance()
                    ans += chr(int(ch, 8))
                else:
                    self.Error('invaild escape characters at "%s"' % self.get_local_text())
            else:
                ans += self.current_char
                self.advance()
        if self.current_char != endchar:
            self.Error('EOL while scanning string literal')
        self.advance()
        return ans

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
                continue
            elif self.current_char.isdigit() or self.current_char == '.':
                return self.get_number()
            elif self.peek() is not None and self.current_char + self.peek() in TwoCharSymbols:
                c = self.current_char + self.peek()
                self.advance()
                self.advance()
                return Token(TwoCharSymbols[c], c)
            elif self.current_char in OneCharSymbols:
                c = self.current_char
                self.advance()
                return Token(OneCharSymbols[c], c)
            elif self.current_char.isalpha() or self.current_char == '_':
                return self.get_NAME()
            elif self.current_char in ['\'', '\"']:
                return Token(STRING, self.get_string())
            else:
                self.Error('parse error at "%s"' % self.get_local_text())
        return Token(EOF, None)


##############################################################
# AST                                                        #
##############################################################

class AST(object):
    """AST class. Only used as base class."""
    pass


class AST_BinOp(AST):
    def __init__(self, token, lson, rson):
        self.token = token
        self.lson = lson
        self.rson = rson

    def __str__(self):
        return "AST_BinOp(%r, %r, %r)" % (self.token, self.lson, self.rson)

    __repr__ = __str__


class AST_UnaryOp(AST):
    def __init__(self, token, son):
        self.token = token
        self.son = son

    def __str__(self):
        return "AST_UnaryOp(%r, %r)" % (self.token, self.son)

    __repr__ = __str__


class AST_Num(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "AST_Num(%r)" % (self.value)

    __repr__ = __str__


class AST_String(AST):
    """AST: string"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "AST_String(%r)" % (self.value)

    __repr__ = __str__


class AST_Array(AST):
    """AST: array"""

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        return "AST_Array(%r)" % (self.lst)

    __repr__ = __str__


class AST_ID(AST):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "AST_ID(%r)" % (self.name)

    __repr__ = __str__


class AST_Print(AST):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "AST_Print(%r)" % (self.expr)

    __repr__ = __str__


class AST_Input(AST):
    """AST: input statement"""

    def __init__(self, var):
        self.var = var

    def __str__(self):
        return "AST_Input(%r)" % (self.var)

    __repr__ = __str__


class AST_EmptyStat(AST):
    def __str__(self):
        return "AST_EmptyStat()"

    __repr__ = __str__


class AST_Block(AST):
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return "AST_Block(%r)" % (self.statements)

    __repr__ = __str__


class AST_FuncDef(AST):
    def __init__(self, name, arglist, block):
        self.name = name
        self.arglist = arglist
        self.block = block

    def __str__(self):
        return "AST_FuncDef(%r, %r, %r)" % (self.name, self.arglist, self.block)

    __repr__ = __str__


class AST_FuncCall(AST):
    def __init__(self, funcname, arglist):
        self.arglist = arglist
        self.funcname = funcname

    def __str__(self):
        return "AST_FuncCall(%r, %r)" % (self.funcname, self.arglist)

    __repr__ = __str__


class AST_If(AST):
    def __init__(self, condition, ifstat, elsestat):
        self.condition = condition
        self.ifstat = ifstat
        self.elsestat = elsestat

    def __str__(self):
        return "AST_If(%r, %r, %r)" % (self.condition, self.ifstat, self.elsestat)

    __repr__ = __str__


class AST_While(AST):
    def __init__(self, condition, stat):
        self.condition = condition
        self.stat = stat

    def __str__(self):
        return "AST_If(%r, %r)" % (self.condition, self.stat)

    __repr__ = __str__


class AST_For(AST):
    """AST: for-loop statement"""

    def __init__(self, name, begin, end, step, stat):
        self.name = name
        self.begin = begin
        self.end = end
        self.step = step
        self.stat = stat

    def __str__(self):
        return "AST_For(%r, %s, %s, %s, %s)" % (
            self.name, self.begin, self.end, self.step, self.stat)

    __repr__ = __str__


class AST_Return(AST):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "AST_Return(%r)" % (self.expr)

    __repr__ = __str__


##############################################################
# Parser                                                     #
##############################################################

class Parser(object):

    def __init__(self, text):
        self.level = 0
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def Error(self, errstr):
        raise SyntaxError(errstr)

    def eat(self, type):
        if self.current_token.type != type:
            self.Error('invalid syntax at "%s" at pos %d' %
                       (self.lexer.get_local_text(), self.lexer.pos - 1l))
        else:
            self.current_token = self.lexer.get_next_token()
            if type in BeginBlockSymbols:
                self.level += 1
            elif type in EndBlockSymbols:
                self.level -= 1
            if self.current_token.type == EOF and self.level > 0:
                text = ''
                while not text and not text.isspace():
                    try:
                        text = raw_input('... ')
                    except NameError:
                        text = input('... ')
                self.lexer = Lexer(text)
                self.current_token = self.lexer.get_next_token()

    def Unit(self, priority):
        if priority == 0:
            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                ans = self.Unit(Max_Priority)
                self.eat(RPAREN)
            elif self.current_token.type == NUM:
                ans = AST_Num(self.current_token.value)
                self.eat(NUM)
            elif self.current_token.type == STRING:
                ans = AST_String(self.current_token.value)
                self.eat(STRING)
            elif self.current_token.type in UnaryOp:
                token = self.current_token
                self.eat(token.type)
                ans = AST_UnaryOp(token, self.Unit(0))
            elif self.current_token.type == NAME:
                name = self.current_token.value
                self.eat(NAME)
                if self.current_token.type == LPAREN:
                    self.eat(LPAREN)
                    arglist = []
                    if self.current_token.type != RPAREN:
                        arglist.append(self.Unit(Max_Priority))
                        while self.current_token.type != RPAREN:
                            self.eat(COMMA)
                            arglist.append(self.Unit(Max_Priority))
                    self.eat(RPAREN)
                    ans = AST_FuncCall(name, arglist)
                else:
                    ans = AST_ID(name)
            elif self.current_token.type == LBRACK:
                self.eat(LBRACK)
                lst = []
                if self.current_token.type != RBRACK:
                    lst.append(self.Unit(Max_Priority))
                    while self.current_token.type == COMMA:
                        self.eat(COMMA)
                        lst.append(self.Unit(Max_Priority))
                self.eat(RBRACK)
                ans = AST_Array(lst)
            else:
                self.Error('invalid syntax at "%r" at pos %d' %
                           (self.lexer.get_local_text(), self.lexer.pos - 1l))
            while self.current_token.type == LBRACK:
                self.eat(LBRACK)
                ind = self.Unit(Max_Priority)
                self.eat(RBRACK)
                ans = AST_BinOp(Token(INDEX, '[]'), ans, ind)
        elif Associativity[priority] == LeftAssoc:
            ans = self.Unit(priority - 1)
            while self.current_token.type in Prio and Prio[self.current_token.type] == priority:
                token = self.current_token
                self.eat(token.type)
                ans = AST_BinOp(token, ans, self.Unit(priority - 1))
        else:
            ans = self.Unit(priority - 1)
            rightest_node = ans
            first = True
            while self.current_token.type in Prio and Prio[self.current_token.type] == priority:
                token = self.current_token
                self.eat(token.type)
                if first:
                    ans = AST_BinOp(token, ans, self.Unit(priority - 1))
                    rightest_node = ans
                    first = False
                else:
                    rightest_node.rson = AST_BinOp(
                        token, rightest_node.rson, self.Unit(priority - 1))
                    rightest_node = rightest_node.rson
        return ans

    def ifstat(self):
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.Unit(Max_Priority)
        self.eat(RPAREN)
        ifstat = self.stat()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            elsestat = self.stat()
        else:
            elsestat = AST_EmptyStat()
        return AST_If(condition, ifstat, elsestat)

    def whilestat(self):
        self.eat(WHILE)
        self.eat(LPAREN)
        condition = self.Unit(Max_Priority)
        self.eat(RPAREN)
        stat = self.stat()
        return AST_While(condition, stat)

    def forstat(self):
        self.eat(FOR)
        self.eat(LPAREN)
        name = self.current_token.value
        self.eat(NAME)
        self.eat(ASSIGN)
        begin = self.Unit(Max_Priority)
        self.eat(COMMA)
        end = self.Unit(Max_Priority)
        if self.current_token.type == COMMA:
            self.eat(COMMA)
            step = self.Unit(Max_Priority)
        else:
            step = None
        self.eat(RPAREN)
        stat = self.stat()
        return AST_For(name, begin, end, step, stat)

    def stat(self):
        if self.current_token.type == LBRACE:
            ans = self.block()
        elif self.current_token.type == PRINT:
            self.eat(PRINT)
            ans = AST_Print(self.Unit(Max_Priority))
            self.eat(SEMI)
        elif self.current_token.type == IF:
            ans = self.ifstat()
        elif self.current_token.type == WHILE:
            ans = self.whilestat()
        elif self.current_token.type == FOR:
            ans = self.forstat()
        elif self.current_token.type == RETURN:
            self.eat(RETURN)
            if self.current_token.type != SEMI:
                ans = AST_Return(self.Unit(Max_Priority))
            else:
                ans = AST_Return(None)
            self.eat(SEMI)
        elif self.current_token.type == INPUT:
            self.eat(INPUT)
            ans = AST_Input(self.Unit(Max_Priority))
            self.eat(SEMI)
        else:
            ans = self.Unit(Max_Priority)
            self.eat(SEMI)
        return ans

    def block(self):
        self.eat(LBRACE)
        block = []
        while self.current_token.type != RBRACE:
            block.append(self.stat())
        self.eat(RBRACE)
        return AST_Block(block)

    def parse(self):
        if self.current_token.type == FUNC:
            self.eat(FUNC)
            token = self.current_token
            self.eat(NAME)
            name = token.value
            self.eat(LPAREN)
            arglist = []
            if self.current_token.type == NAME:
                arglist.append(self.current_token.value)
                self.eat(NAME)
                while self.current_token.type != RPAREN:
                    self.eat(COMMA)
                    token = self.current_token
                    self.eat(NAME)
                    arglist.append(token.value)
            self.eat(RPAREN)
            return AST_FuncDef(name, arglist, self.block())
        else:
            return self.stat()


##############################################################
# NodeVisitor                                                #
##############################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__[4:]
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_%s method' % type(node).__name__)


class Inputer(object):
    def __init__(self):
        self.lst = []

    def getNumber(self):
        if not self.lst:
            try:
                self.lst = raw_input().split()
            except NameError:
                self.lst = input().split()
        ans = float(self.lst[0])
        self.lst = self.lst[1:]
        return ans


inputer = Inputer()


class Interpreter(NodeVisitor):
    def __init__(self, parser, global_var, functions):
        self.parser = parser
        self.global_var = global_var
        self.local_var = [global_var]
        self.call_stack = []
        self.functions = functions
        self.returned = False
        self.return_value = None

    def Error(self, errstr):
        raise SyntaxError(errstr)

    def visit_BinOp(self, node):
        tp = node.token.type
        if tp != ASSIGN:
            lans = self.visit(node.lson)
            if (tp == AND and not lans) or (tp == OR and lans):
                return lans
            return BinOp[tp](lans, self.visit(node.rson))
        elif not isinstance(node.lson, AST_ID):
            if isinstance(node.lson, AST_BinOp) and node.lson.token.type == INDEX:
                self.visit(node.lson.lson)[int(self.visit(node.lson.rson))] = self.visit(node.rson)
            else:
                self.Error("Can't assign to a non-variable")
        else:
            name = node.lson.name
            for vars in list(reversed(self.local_var)):
                if name in vars:
                    vars[name] = self.visit(node.rson)
                    return vars[name]
            self.local_var[-1][name] = self.visit(node.rson)
            return self.local_var[-1][name]

    def visit_Print(self, node):
        ans = self.visit(node.expr)
        if isinstance(ans, float):
            print('%g' % ans)
        else:
            print(ans)

    def visit_Input(self, node):
        ans = inputer.getNumber()
        self.visit(AST_BinOp(Token(ASSIGN, '='), node.var, AST_Num(float(ans))))

    def visit_UnaryOp(self, node):
        return UnaryOp[node.token.type](self.visit(node.son))

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Array(self, node):
        ans = []
        for subnode in node.lst:
            ans.append(self.visit(subnode))
        return ans

    def visit_ID(self, node):
        for vars in list(reversed(self.local_var)):
            if node.name in vars:
                return vars[node.name]
        if node.name in self.global_var:
            return self.global_var[node.name]
        else:
            self.Error('Undefined variable: %s' % node.name)

    def visit_FuncDef(self, node):
        self.functions[node.name] = node

    def visit_FuncCall(self, node):
        if not node.funcname in self.functions:
            self.Error('Undefined function: %s' % node.funcname)
        func = self.functions[node.funcname]
        length = len(func.arglist)
        if length != len(node.arglist):
            self.Error('%s takes %d argument(s) (%d given)' %
                       (node.name, length, len(node.arglist)))
        newlocal = {}
        for i in range(length):
            newlocal[func.arglist[i]] = self.visit(node.arglist[i])
        self.call_stack.append(self.local_var)
        self.local_var = [self.global_var, newlocal]
        for stat in func.block.statements:
            self.visit(stat)
            if self.returned:
                break
        self.returned = False
        self.local_var = self.call_stack.pop()
        return self.return_value

    def visit_EmptyStat(self, node):
        pass

    def visit_Block(self, node):
        self.local_var.append({})
        for stat in node.statements:
            self.visit(stat)
            if self.returned:
                break
        self.local_var.pop()

    def visit_If(self, node):
        if self.visit(node.condition):
            self.visit(node.ifstat)
        else:
            self.visit(node.elsestat)

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.stat)

    def visit_For(self, node):
        begin = self.visit(node.begin)
        self.local_var.append({node.name: begin})
        end = self.visit(node.end)
        if node.step is not None:
            step = self.visit(node.step)
        elif begin <= end:
            step = 1
        else:
            step = -1
        while (end - self.local_var[-1][node.name]) * step >= 0:
            self.visit(node.stat)
            self.local_var[-1][node.name] += step
        self.local_var.pop()

    def visit_Return(self, node):
        if node.expr == None:
            self.return_value = None
        else:
            self.return_value = self.visit(node.expr)
        self.returned = True

    def interpret(self):
        tree_root = self.parser.parse()
        ans = self.visit(tree_root)
        if self.returned:
            self.Error('Return outside functions!')
        return ans


##############################################################
# Main                                                       #
##############################################################

cmd_list = ['help', 'version', 'showall', 'init', 'showfunc']

variable_table = {}
functions = {}
last = None


def CMD_help(args):
    print('Test help')


def CMD_version(args):
    print('version ' + VERSION)


def CMD_print(args):
    print(args[0])


def CMD_showfunc(args):
    if functions:
        length = 0
        ans = []
        for k in functions:
            s = k + '('
            if functions[k].arglist:
                s += functions[k].arglist[0]
                for t in functions[k].arglist[1:]:
                    s += ', ' + t
            s += ')'
            length = max(length, len(s))
            ans.append(s)
        for s in ans:
            print(s)
    else:
        print('No functions.')


def CMD_showall(args):
    if variable_table:
        length = 0
        for k in variable_table:
            length = max(length, len(k))
        for (k, v) in variable_table.items():
            print('%s : %s' % ((length - len(k) + 1) * ' ' + k, v))
    else:
        print('No variables.')


def CMD_showfunc(args):
    if functions:
        length = 0
        ans = []
        for k in functions:
            s = k + '(' + str(functions[k].args)[1:-1] + ')'
            length = max(length, len(s))
            ans.append(s)
        for s in ans:
            print(s)
    else:
        print('No variables.')


def CMD_init(args):
    variable_table.clear()
    print('Ok. All variables are deleted.')


def runcmd(text):
    if len(text) == 1:
        text = last
    args = text.split()
    text = args[0]
    args = args[1:]
    if text == None:
        print('There is no last command to perfrom.')
        print('Enter ":help" for help.')
        return
    lst = reduce(lambda l, s: s.find(text[1:]) and l or l + [s],
                 cmd_list, [None])[1:]
    if not lst:
        last = None
        print('Unknown command"' + text + '".')
        print('Enter ":help" for help.')
        return
    last = text
    if len(lst) > 1:
        print('Ambiguous command. You may want:')
        ans = ''
        for i in range(0, len(lst)):
            ans += ' ' + lst[i]
            if len(ans) >= 50:
                print(ans)
                ans = ''
        print(ans)
    else:
        globals()['CMD_' + lst[0]](args)


def main():
    print('A calculator written by RQY at Mar 31, 2017.')
    print('version ' + VERSION)
    try:
        while True:
            try:
                text = raw_input('>>> ')
            except NameError:
                text = input('>>> ')
            if text and not text.isspace():
                text.strip()
                if text[0] == ':':
                    runcmd(text)
                else:
                    try:
                        p = Parser(text)
                        i = Interpreter(p, variable_table, functions)
                        ans = i.interpret()
                        # if ans is not None:
                        # print(ans)
                        # print(p.parse())
                    except Exception, e:
                        print(e.message)
    except EOFError:
        print('')


if __name__ == '__main__':
    main()
