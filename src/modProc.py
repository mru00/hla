from modStatements import *


class ProcDecl(Decl): pass

class On(ProcDecl):
    genpos = GEN_STATIC_GLOBAL
    template = Template(r"""\
${"  "*level}ISR(${nte.items[1].value}) {
${nte.items[3].render(level+1)}\
${"  "*level}}
""")


class When(ProcDecl):
    genpos = GEN_MAIN_LOOP
    template = Template(r"""\
${"  "*level}if ( ${nte.items[1].render()} ) {
${nte.items[3].render(level+1)}\
${"  "*level}}
""")

class Initially(ProcDecl):
    genpos = GEN_INITIALLY_MAIN
    template = Template(r"""\
${"  "*level}${nte.items[2].render(level+1)}\
""")


add_rule(When, [ "when", Condition, "do", StatementList, "done" ])
add_rule(Initially, [ "initially", "do", StatementList, "done" ])
add_rule(On, [ "on", Name, "do", StatementList, "done" ])

