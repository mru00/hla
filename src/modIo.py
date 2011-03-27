from ruledb import *
from entities import *
from namespace import *

from modBase import *


class IoRef(TE):
    def canparse(self):
        return get_symbol('io', self.value) != None

class IoDir(TE):
    expression = re.compile(r"INPUT|OUTPUT")

class Port(TE):
    expression = re.compile(r"[ABCD]\.\d")

class IoDecl(Decl):
    def onparse(self):
        add_symbol('io', self.items[1].value, self)

add_rule(IoDecl, [ "io", Name, "is", IoDir, "on", Port ])
