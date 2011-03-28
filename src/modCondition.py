from modIo import *

class NamedCondition(Condition):
    template = Template(r"""\
${nte.getcond().render()}\
""")
    def canparse(self):
        print "HAS %s" % get_symbol('cond', self.items[0].value)
        return get_symbol('cond', self.items[0].value) != None
    def getcond(self):
        c = get_symbol('cond', self.items[0].value)
        assert c
        return c.items[3]

class BinCondition(Condition): pass

class BinConditionVar(BinCondition):
    template = Template(r"""\
${nte.items[0].value} == ${nte.items[2].value}\
""")

class BinConditionIo(BinCondition):
    template = Template(r"""\
${nte.items[0].value} == ${nte.items[2].value}\
""")

class ConditionDecl(Decl):
    def onparse(self):
        add_symbol('cond', self.items[1].value, self)

add_rule(NamedCondition, [Name])
add_rule(BinConditionIo, [IoRef, Op, Value])
add_rule(BinConditionVar, [VarRef, Op, Value])
add_rule(ConditionDecl, ["condition", Name, "is", BinCondition])

