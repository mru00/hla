from ruledb import *
from entities import *
from namespace import *
from mako.template import Template

from modStatements import *

class While(Statement):
    template = Template(r"""\
${"  "*level}while ( ${nte.items[1].render()} ) {
${nte.items[3].render(level+1)}\
${"  "*level}}
""")

add_rule(While, ["while", Condition, "do", StatementList, "done" ])
