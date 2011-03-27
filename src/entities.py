import re
import logging
from namespace import *
from mako.template import Template


class TE(object):
    expression = re.compile(r"\w+")
    def __init__(self):
        self.value = None
        self.isparsed = False
    def dump(self, level=0):
        return "\n" + " "*level + self.__class__.__name__ + " value: " + str(self.value)
    def onparse(self):
        pass
    def postparse(self):
        if not self.isparsed:
            self.onparse()
            self.isparsed = True
    def canparse(self):
        return True

class NTE(object):
    template = Template("")
    def __init__(self):
        self.items = []
        self.isparsed = False
    def add(self, item):
        self.items.append(item)
    def get_first(self, clazz):
        return filter(lambda a: type(a) == clazz,  self.items)[0]
    def get_items(self, clazz):
        return filter(lambda a: type(a) == clazz,  self.items)
    def postparse(self):
        if not self.isparsed:
            self.onparse()
            self.isparsed = True
    def dump(self, level=0):
        d =  "\n"+ " "*level + self.__class__.__name__
        for i in self.items:
            d += i.dump(level+1)
        return d
    def onparse(self):
        pass
    def gencode(self):
        pass
    def render(self):
        return self.template.render(nte=self)
    def canparse(self):
        return True

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



class Target(NTE): pass


class Program(NTE):
        template = Template("""
#include <avr.h>
##${nte.get_first(Target).render()}

% for vardecl in nte.get_items(VarDecl):
${vardecl.render()}
% endfor

void main() {

% for intially in nte.get_items(Initially):
${intially.render()}
% endfor

for(;;) {

% for proc in nte.get_items(ProcDecl):
${proc.render()}
% endfor

}

}

""")



class Decl(NTE): pass
class Statement(NTE): pass
class Condition(NTE): pass


class UseDecl(Decl):
    def onparse(self):
        load_mod(self.items[1].value)

class VarDecl(Decl):
    def onparse(self):
        add_symbol('var', self.items[1].value, self)


