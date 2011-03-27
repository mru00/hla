from ruledb import *
from entities import *
from namespace import *

from modStatements import *

class While(Statement): pass


add_rule(While, ["while", Condition, "do", StatementList, "done" ])
