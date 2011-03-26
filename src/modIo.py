from ruledb import *
from entities import *
from namespace import *


class IoRef(TE):
    def canparse(self):
        s = get_symbol('io', self.value)
        if not s:
            logging.info("name " + self.value + "was not found")
        return s

class IoDir(TE):
    expression = re.compile(r"INPUT|OUTPUT")
    def canparse(self):
        return re.match(self.expression, self.value)

class IoDecl(NTE):
    def onparse(self):
        add_symbol('io', self.items[1].value, self)

class Port(TE):
    expression = re.compile(r"[ABCD]\.\d")
    def canparse(self):
        return re.match(self.expression, self.value)

add_rule(IoDecl, [ "io", Name, "is", IoDir, "on", Port ])
add_rule(Decl, IoDecl)
