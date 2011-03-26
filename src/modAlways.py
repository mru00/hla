from ruledb import *
from entities import *
from namespace import *

from modProc import *


class Always(NTE): pass

add_rule(ProcDecl, Always)
add_rule(Always, [ "always", "do", [Statement], "done"])

