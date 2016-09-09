#-------------------------------------------------
# IMPORTS
#-------------------------------------------------

from parsing.syntax import *
from semantics.scope import Scope

#-------------------------------------------------
# CONSTANTS
#-------------------------------------------------

PASS_1 = 1
PASS_2 = 2
PASS_3 = 3
PASS_4 = 4

#-------------------------------------------------
# DECORATORS
#-------------------------------------------------

def analyzes(c, p):
    def decorator(func):
        func._na_pass      = p
        func._na_construct = c

        return func

    return decorator

#-------------------------------------------------
# CLASSES
#-------------------------------------------------

class SemanticAnalyzer(object):
    def __init__(self):
        self.analyzer_funcs = {}

        for s in dir(self):
            func = getattr(self, s, None)
            if not hasattr(func, '_na_construct'):
                continue

            p = func._na_pass
            c = func._na_construct

            if p not in self.analyzer_funcs:
                self.analyzer_funcs[p] = {}

            self.analyzer_funcs[p][c] = func

        self.scope = Scope()

        # Built-ins
        self.scope.decl_var('console'  , 'string')
        self.scope.decl_var('file'     , 'string')
        self.scope.decl_var('process'  , 'string')
        self.scope.decl_var('readline' , 'string')

    def verify(self, ast):
        self.enter_scope()

        for p in range(1, 5):
            self.cur_pass = p
            self.verify_single(ast)

        self.leave_scope()

    def verify_children(self, node):
        if not node.children:
            return

        for child in node.children:
            self.verify_single(child)

    def verify_single(self, node):
        p = self.cur_pass

        r = False
        if p in self.analyzer_funcs:
            funcs = self.analyzer_funcs[p]
            if node.construct in funcs:
                funcs[node.construct](node)
                r = True

        if not r:
            self.verify_children(node)

    def enter_scope(self):
        self.scope = Scope(parent_scope=self.scope)

    def leave_scope(self):
        for s in self.scope.variables:
            var = self.scope.var(s)

            # One read means the variable is never used (only assigned once).
            if var.reads == 1:
                smaragd.warning('variable not used: {}'.format(var.name))

        self.scope = self.scope.parent_scope

    @analyzes(ASSIGN, PASS_1)
    def __assign(self, node):
        if node.children[0].construct == IDENTIFIER:
            var_name = node.children[0].data
            var = self.scope.var(var_name)
            if not var:
                # FIXME: Keep type data?
                self.scope.decl_var(var_name, 'string')
            var = self.scope.var(var_name)
            var.writes += 1

        self.verify_children(node)

    @analyzes(FUNC, PASS_1)
    def __func(self, node):
        if node.data:
            self.scope.decl_var(node.data, 'string')

        self.enter_scope()

        decl = node.children[0]
        defi = node.children[1]

        for child in decl.children:
            assert child.construct == IDENTIFIER
            self.scope.decl_var(child.data, 'string')

        self.verify_children(node)

        self.leave_scope()

    @analyzes(IDENTIFIER, PASS_1)
    def __identifier(self, node):
        var = self.scope.var(node.data)
        if not var:
            smaragd.error('identifier not declared: {}'.format(node.data), node.token)
        else:
            var.reads += 1

    @analyzes(ADD, PASS_2)
    def __add(self, node):
        a = node.children[0]
        b = node.children[1]

        if (a.construct in (INTEGER, STRING)
        and b.construct in (INTEGER, STRING)
        and a.construct != b.construct):
            smaragd.warning('adding integer and string', node.token)

        for child in node.children:
            self.verify_single(child)

    @analyzes(DIVIDE, PASS_2)
    def __divide(self, node):
        a = node.children[0]
        b = node.children[1]

        if (a.construct == STRING or b.construct == STRING):
            smaragd.error('division only allowed with integers', node.token)

        elif (a.construct == INTEGER and b.construct == INTEGER):
            if int(b.data) == 0:
                smaragd.warning('division by zero', node.token)
            elif int(a.data) > int(b.data):
                smaragd.warning('division will result in zero', node.token)

        self.verify_children(node)

    @analyzes(MULTIPLY, PASS_2)
    def __multiply(self, node):
        a = node.children[0]
        b = node.children[1]

        if (a.construct == STRING or b.construct == STRING):
            smaragd.error('multiplication only allowed with integers', node.token)

        self.verify_children(node)

    @analyzes(SUBTRACT, PASS_2)
    def __subtract(self, node):
        a = node.children[0]
        b = node.children[1]

        if (a.construct == STRING or b.construct == STRING):
            smaragd.error('subtraction only allowed with integers', node.token)

        self.verify_children(node)
