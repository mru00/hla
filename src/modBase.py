from dynparser import parse, add_rule, reset_rules, NTE, TE
from dynparser.gendb import *
from dynparser.namespace import get_symbol, add_symbol

import re

from mako.template import Template


def load_mod(name):
    use = __import__('mod'+name, globals(), locals(), [], 0)
    if not get_symbol('mod', name):
        add_symbol('mod', name, use)



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

add_rule(Target, [ "targets", Name ])
add_rule(UseDecl, [ "uses", Name ])
add_rule(VarDecl, [ "var", Name, "is", Type ])

add_rule(Program, [ Target , [Decl]])

