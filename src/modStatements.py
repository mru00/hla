from ruledb import *
from entities import *
from namespace import *


class Set(Statement): pass
class Increment(Statement): pass
class Invert(Statement): pass


add_rule(Set, [ "set", Name, Value ] )
add_rule(Increment, [ "increment", Name ])
add_rule(Invert, [ "invert", Name ])

