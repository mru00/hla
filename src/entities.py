import re
from namespace import *

class TE(object): 
    def __init__(self):
        self.value = None
    def dump(self, level=0):
        return "\n" + " "*level + self.__class__.__name__ + " value: " + str(self.value)
    def onparse(self):
        pass


class NTE(object):
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)
    def dump(self, level=0):
        d =  "\n"+ " "*level + self.__class__.__name__
        for i in self.items:
            d += i.dump(level+1)
        return d
    def onparse(self):
        pass


class Name(TE):
    expression = re.compile(r"\s+")
class Port(TE):
    expression = re.compile(r"[ABCD]\.\d")
class Value(TE):
    expression = re.compile(r"\d+")
class Nl(TE):
    expression = re.compile(r"\n")

class IoDir(TE):
    expression = re.compile(r"INPUT|OUTPUT")

class Op(TE):
    expression = re.compile(r"INPUT|OUTPUT")

class Type(TE): pass


class Program(NTE): pass

class Target(NTE): pass

class UseDecl(NTE): pass

class VarDecl(NTE):
    def onparse(self):
        add_symbol('var', self.items[1].value, self)

class IoDecl(NTE):
    def onparse(self):
        add_symbol('io', self.items[1].value, self)

class ConditionDecl(NTE):
    def onparse(self):
        add_symbol('cond', self.items[1].value, self)


class Condition(NTE): pass
class BinCondition(NTE): pass
class NamedCondition(NTE): pass


class Statement(NTE): pass
class Set(NTE): pass
class Increment(NTE): pass
class Initially(NTE): pass


class ProcDecl(NTE): pass
class When(NTE): pass
class On(NTE): pass
class Invert(NTE): pass
class Always(NTE): pass

