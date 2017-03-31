from Constants import *
import Lexer


class AST(object):
    """AST class. Only used as base class."""
    pass


class AST_BinOp(AST):
    """AST: binary operator"""

    def __init__(self, token, lson, rson):
        self.token = token
        self.lson = lson
        self.rson = rson

    def __str__(self):
        return "AST_BinOp(%r, %r, %r)" % (self.token, self.lson, self.rson)

    __repr__ = __str__


class AST_UnaryOp(AST):
    """AST: unary operator"""

    def __init__(self, token, son):
        self.token = token
        self.son = son

    def __str__(self):
        return "AST_UnaryOp(%r, %r)" % (self.token, self.son)

    __repr__ = __str__


class AST_Num(AST):
    """AST: number"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "AST_Num(%g)" % (self.value)

    __repr__ = __str__


class AST_Array(AST):
    """AST: array"""

    def __init__(self, lst):
        self.lst = lst

    def __str__(self):
        return "AST_Num(%r)" % (self.lst)

    __repr__ = __str__


class AST_ID(AST):
    """AST: name (for variable)"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "AST_ID(%r)" % (self.name)

    __repr__ = __str__


class AST_Print(AST):
    """AST: print statement"""

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "AST_Print(%r)" % (self.expr)

    __repr__ = __str__


class AST_EmptyStat(AST):
    """AST: empty statement"""

    def __str__(self):
        return "AST_EmptyStat()"

    __repr__ = __str__


class AST_Block(AST):
    """AST: code block"""

    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return "AST_Block(%r)" % (self.statements)

    __repr__ = __str__


class AST_FuncDef(AST):
    """AST: function definition"""

    def __init__(self, name, arglist, block):
        self.name = name
        self.arglist = arglist
        self.block = block

    def __str__(self):
        return "AST_FuncDef(%r, %r, %r)" % (self.name, self.arglist, self.block)

    __repr__ = __str__


class AST_FuncCall(AST):
    """AST: function call"""

    def __init__(self, funcname, arglist):
        self.arglist = arglist
        self.funcname = funcname

    def __str__(self):
        return "AST_FuncCall(%r, %r)" % (self.funcname, self.arglist)

    __repr__ = __str__


class AST_If(AST):
    """AST: if-else statement"""

    def __init__(self, condition, ifstat, elsestat):
        self.condition = condition
        self.ifstat = ifstat
        self.elsestat = elsestat

    def __str__(self):
        return "AST_If(%r, %r, %r)" % (self.condition, self.ifstat, self.elsestat)

    __repr__ = __str__


class AST_Return(AST):
    """AST: return statement"""

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "AST_Return(%r)" % (self.expr)

    __repr__ = __str__


class AST_While(AST):
    """AST: while-loop statement"""

    def __init__(self, condition, stat):
        self.condition = condition
        self.stat = stat

    def __str__(self):
        return "AST_While(%r, %r)" % (self.condition, self.stat)

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


class Parser(object):

    def __init__(self, text):
        self.level = 0
        self.lexer = Lexer.Lexer(text)
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
                self.lexer = Lexer.Lexer(text)
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
                ans = AST_BinOp(Lexer.Token(INDEX, '[]'), ans, ind)
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

    def stat(self):
        if self.current_token.type == LBRACE:
            ans = self.block()
        elif self.current_token.type == PRINT:
            self.eat(PRINT)
            ans = AST_Print(self.Unit(Max_Priority))
            self.eat(SEMI)
        elif self.current_token.type == IF:
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
            ans = AST_If(condition, ifstat, elsestat)
        elif self.current_token.type == WHILE:
            self.eat(WHILE)
            self.eat(LPAREN)
            condition = self.Unit(Max_Priority)
            self.eat(RPAREN)
            stat = self.stat()
            ans = AST_While(condition, stat)
        elif self.current_token.type == FOR:
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
            ans = AST_For(name, begin, end, step, stat)
        elif self.current_token.type == RETURN:
            self.eat(RETURN)
            if self.current_token.type != SEMI:
                ans = AST_Return(self.Unit(Max_Priority))
            else:
                ans = AST_Return(None)
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
