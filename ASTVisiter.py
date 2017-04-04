from Constants import *
from Lexer import Token
import Parser


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
        self.inputer = Inputer()

    def Error(self, errstr):
        raise SyntaxError(errstr)

    def visit_BinOp(self, node):
        tp = node.token.type
        if tp != ASSIGN:
            lans = self.visit(node.lson)
            if (tp == AND and not lans) or (tp == OR and lans):
                return lans
            return BinOp[tp](lans, self.visit(node.rson))
        elif not isinstance(node.lson, Parser.AST_ID):
            if isinstance(node.lson, Parser.AST_BinOp) and node.lson.token.type == INDEX:
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
        self.visit(Parser.AST_BinOp(Token(ASSIGN, '='), node.var, Parser.AST_Num(float(ans))))

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
                       (node.funcname, length, len(node.arglist)))
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
