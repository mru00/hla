import re
import logging
from namespace import *



class TE(object):
    expression = re.compile(r"\w+")
    def __init__(self):
        self.value = None
    def dump(self, level=0):
        return "\n" + " "*level + self.__class__.__name__ + " value: " + str(self.value)
    def onparse(self):
        pass
    def canparse(self):
        return True

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


class Name(TE): pass

class VarRef(TE):
    def canparse(self):
        return get_symbol('var', self.value) != None

class Value(TE):
    expression = re.compile(r"\d+|low|high")

class Op(TE):
    expression = re.compile(r"[+-=]")

class Type(TE):
    expression = re.compile(r"u8")





class Program(NTE): pass

class Target(NTE): pass

class Decl(NTE): pass
class Statement(NTE): pass
class Condition(NTE): pass


class UseDecl(Decl):
    def onparse(self):
        load_mod(self.items[1].value)

class VarDecl(Decl):
    def onparse(self):
        add_symbol('var', self.items[1].value, self)


