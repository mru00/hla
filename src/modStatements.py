from ruledb import *
from entities import *
from namespace import *
from mako.template import Template


class Set(Statement):
    template = Template(r"""\
${"  "*level}${nte.items[1].value} = ${nte.items[2].value};
""")

class Increment(Statement):
    template = Template(r"""\
${"  "*level}${nte.items[1].value}++;
""")


class Invert(Statement):
    template = Template(r"""\
${"  "*level}${nte.items[1].value} = ! ${nte.items[1].value};
""")

class StatementList(NTE):
    template = Template(r"""\
% for o in nte.items:
${o.render(level+1)}\
% endfor
""")

add_rule(Set, [ "set", Name, Value ] )
add_rule(Increment, [ "increment", Name ])
add_rule(Invert, [ "invert", Name ])

add_rule(StatementList, [ [Statement] ])
