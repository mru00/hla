from ruledb import *
from entities import *
from namespace import *

class ProcDecl(Decl): pass

class On(ProcDecl): pass
class When(ProcDecl): pass
class Initially(ProcDecl): pass

add_rule(When, [ "when", Condition, "do", [Statement], "done" ])
add_rule(Initially, [ "initially", "do", [Statement], "done" ])
add_rule(On, [ "on", Name, "do", [Statement], "done" ])

