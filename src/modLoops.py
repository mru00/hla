from ruledb import *
from entities import *
from namespace import *


class While(Statement): pass


add_rule(Statement, While)
add_rule(While, ["while", Condition, "do", [Statement], "done" ])
