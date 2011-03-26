from entities import *
from namespace import *
import re

import logging
logging.basicConfig(level=logging.DEBUG)

rules = {}


def add_rule(clazz, arg):
    global rules
    if clazz not in rules.keys():
        rules[clazz] = [ arg ]
    else:
        rules[clazz].append(arg)


token_pat = re.compile(r"[a-zA-Z0-9_.=]+")

def tokenize(program):
    for token in token_pat.findall(program):
        yield token

tokenizer = tokenize(open("test.hla", "rt").read()).next

get_productions = lambda clazz: rules[clazz]

token = tokenizer()


def is_te(clazz):
    try:
        return issubclass(clazz, TE)
    except TypeError:
        return False

def next_token(level):
    global token
    global tokenizer
    logging.info("tokenizer: current token: " + token)
    try:
        token = tokenizer()
        logging.info("tokenizer: next token: " + token)
    except StopIteration:
        logging.info("tokenizer: consumed all stream: ")
        token = None

def parse(clazz, level=0):
    global token


    dbg = lambda m:logging.debug(str(level)+" "*level + m);

    if not token:
        return None

    dbg("curren token= " + str(token))

    parsed_object = None

    if is_te(clazz):
        dbg("must parse TE "+clazz.__name__)
        parsed_object = clazz()
        parsed_object.value = token
        next_token(level)

    else:

        prod_items = get_productions(clazz)

        dbg("trying to parse NTE: "+clazz.__name__ +
                      " with " + str(prod_items))


        for r in prod_items:
            dbg("testing production: " + str(r))


            if type(r) == str:
                assert False, "only TE's can have single-strings"

            elif type(r) == list:
                dbg("found list: " + str(r))
                possible_object = clazz()
                for p in r:
                    dbg("  the current production has next: " + str(p))
                    if type(p) == str:

                        dbg(" must parse string: " + p +
                            " with current token: " + token)

                        if p != token:
                            return None
                        dbg(">>parsed TE: " + p)
                        o = TE()
                        o.value = token
                        possible_object.add(o)
                        next_token(level)
                    elif type(p) == list:
                        dbg(" must parse repetition")
                        assert len(p) == 1
                        clazz3 = p[0]
                        while True:
                            x = parse(clazz3, level+1)
                            if not x:
                                dbg("could not parse "+clazz3.__name__)
                                break
                            else:
                                possible_object.add(x)
                    else:
                        subs = parse(p,level+1)
                        dbg(">>parsed NTE[1]: " + str(subs))
                        possible_object.add(subs)
                parsed_object = possible_object

            elif issubclass(r,NTE):
                possible_object = clazz()
                o = parse(r,level+1)

                if o:
                    dbg(">>parsed NTE[2]: " + str(o))
                    possible_object.add(o)
                    parsed_object = possible_object
                    break
                else:
                    dbg(">>parsing NTE "+r.__name__+" failed, retreat")

            else:
                assert False, "unexpected production item: " + str(r)

    if parsed_object:

        dbg("finishing parse of " + clazz.__name__ +
            " with parse_tree: " + parsed_object.dump())
    else:
        dbg(">>parsing NTE "+r.__name__+" failed, retreat")

    if parsed_object:
        parsed_object.onparse()
    return parsed_object

add_rule(IoDir, "INPUT")
add_rule(IoDir, "OUTPUT")
add_rule(Op, "=")
add_rule(Op, "+")
add_rule(Op, "-")
add_rule(Type, "u8")
add_rule(NamedCondition, [Name])
add_rule(IoDecl, [ "io", Name, "is", IoDir, "on", Port ])
add_rule(Target, [ "targets", Name ])
add_rule(UseDecl, [ "uses", Name ])
add_rule(VarDecl, [ "var", Name, "is", Type ])
add_rule(BinCondition, [Name, Op, Value])
add_rule(ConditionDecl, ["condition", Name, "is", BinCondition])
add_rule(Condition, NamedCondition)
add_rule(Condition, BinCondition)

add_rule(Program, [ Target , [UseDecl], [IoDecl], [VarDecl], 
                    [ConditionDecl], [ProcDecl] ])
add_rule(Set, [ "set", Name, Value ] )
add_rule(Increment, [ "increment", Name ])
add_rule(Invert, [ "invert", Name ])

add_rule(Statement, Set)
add_rule(Statement, Increment)
add_rule(Statement, Invert)

add_rule(ProcDecl, When)
add_rule(ProcDecl, On)
add_rule(ProcDecl, Always)
add_rule(ProcDecl, Initially)


add_rule(When, [ "when", BinCondition, "do", [Statement], "done" ])
add_rule(Initially, [ "initially", "do", [Statement], "done" ])
add_rule(On, [ "on", Name, "do", [Statement], "done" ])
add_rule(Always, [ "always", "do", [Statement], "done"])


parse_tree = parse(Program)
logging.info("parsed: " + parse_tree.dump())
assert token == None, "parse error: not all stream consumed"


dump_namespace()
