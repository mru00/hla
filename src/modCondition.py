from ruledb import *
from entities import *
from namespace import *

from modIo import *

class NamedCondition(Condition):
    def canparse(self):
        print "HAS %s" % get_symbol('cond', self.items[0].value)
        return get_symbol('cond', self.items[0].value) != None

class BinCondition(Condition): pass
class BinConditionVar(BinCondition): pass
class BinConditionIo(BinCondition): pass

class ConditionDecl(Decl):
    def onparse(self):
        add_symbol('cond', self.items[1].value, self)

add_rule(BinConditionIo, [IoRef, Op, Value])
add_rule(BinConditionVar, [VarRef, Op, Value])
add_rule(ConditionDecl, ["condition", Name, "is", BinCondition])
add_rule(NamedCondition, [Name])

