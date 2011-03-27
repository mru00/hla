from ruledb import *
from entities import *
from namespace import *

from modProc import *

class Always(ProcDecl): pass

add_rule(Always, [ "always", "do", StatementList, "done"])

