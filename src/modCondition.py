from ruledb import *
from entities import *
from namespace import *

class BinCondition(NTE): pass
class NamedCondition(NTE): pass

class ConditionDecl(NTE):
    def onparse(self):
        add_symbol('cond', self.items[1].value, self)

add_rule(Decl, ConditionDecl)
add_rule(BinCondition, [Name, Op, Value])
add_rule(ConditionDecl, ["condition", Name, "is", BinCondition])
add_rule(Condition, BinCondition)

#add_rule(NamedCondition, [Name])
#add_rule(Condition, NamedCondition)
