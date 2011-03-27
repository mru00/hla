from ruledb import *
from entities import *
from namespace import *

class CallC(Statement): pass

add_rule(Statement, CallC)
add_rule(CallC, [ "callc", Name ])
