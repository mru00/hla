from ruledb import *
from entities import *
from namespace import *


class Set(NTE): pass
class Increment(NTE): pass
class Invert(NTE): pass


add_rule(Set, [ "set", Name, Value ] )
add_rule(Increment, [ "increment", Name ])
add_rule(Invert, [ "invert", Name ])


add_rule(Statement, Set)
add_rule(Statement, Increment)
add_rule(Statement, Invert)
