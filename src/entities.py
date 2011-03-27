import re
import logging
from namespace import *
from gendb import *
import gendb
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
    genpos = GEN_HERE
    template = Template(r"""/*not implemented : ${nte.__class__}*/
""")
    def __init__(self):
        self.items = []
        self.isparsed = False
    def add(self, item):
        self.items.append(item)
    def get_first(self, clazz):
        return self.get_items(clazz)[0]
    def get_items(self, clazz):
        logging.debug("+searching for %s" % str(clazz))
        for i in self.items:
            logging.debug("  could be %s" % i)
        l = filter(lambda a: isinstance(a,eval(clazz)),  self.items)
        for i in l:
            logging.debug("  is %s" % i)

        return l
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
    def render(self, level=0):
        logging.debug("rendering: %s" % self.__class__.__name__)
        return self.template.render(nte=self, gendb=gendb, level=level)
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



class Target(NTE):
    genpos = GEN_INCLUDE
    


class Program(NTE):

    template = Template(r"""
#include <avr.h>

% for o in nte.getpositems(gendb.GEN_INCLUDE):
<% assert o != Undefined %>
${o.render(0)}\
% endfor

% for o in nte.getpositems(gendb.GEN_STATIC_GLOBAL):
<% assert o != Undefined %>
${o.render(0)}\
% endfor

void main() {

% for o in nte.getpositems(gendb.GEN_INITIALLY_MAIN):
<% assert o != Undefined %>
${o.render(1)}
% endfor

  for(;;) {
% for o in nte.getpositems(gendb.GEN_MAIN_LOOP):
<% assert o != Undefined %>
${o.render(3)}
% endfor
  }

}

""")

    def getpositems(self, pos):
        return filter (lambda a: a.genpos == pos, self.items)


class Decl(NTE): pass
class Statement(NTE): pass
class Condition(NTE): pass


class UseDecl(Decl):
    def onparse(self):
        load_mod(self.items[1].value)

class VarDecl(Decl):
    template = Template("""
static ${nte.items[3].value} ${nte.items[1].value};
""")

    genpos = GEN_STATIC_GLOBAL
    def onparse(self):
        add_symbol('var', self.items[1].value, self)

