from ruledb import *
from entities import *
from namespace import *

from modBase import *

class CallC(Statement): pass

add_rule(CallC, [ "callc", Name ])
