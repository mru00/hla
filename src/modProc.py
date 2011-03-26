from ruledb import *
from entities import *
from namespace import *

class On(NTE): pass
class When(NTE): pass
class Initially(NTE): pass
class ProcDecl(NTE): pass


add_rule(Decl, ProcDecl)


add_rule(When, [ "when", Condition, "do", [Statement], "done" ])
add_rule(Initially, [ "initially", "do", [Statement], "done" ])
add_rule(On, [ "on", Name, "do", [Statement], "done" ])



add_rule(ProcDecl, When)
add_rule(ProcDecl, Initially)
add_rule(ProcDecl, On)
