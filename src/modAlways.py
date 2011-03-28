from modProc import *

class Always(ProcDecl): pass

add_rule(Always, [ "always", "do", StatementList, "done"])
