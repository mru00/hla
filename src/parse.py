from entities import *
from namespace import *
from ruledb import *
import re

import logging

token = None
tokenizer = None

token_pat = re.compile(r"[^ \t\n]+")

def tokenize(program):
    for token_ in token_pat.findall(program):
        yield token_


def next_token(level):
    global token
    global tokenizer
    logging.debug("tokenizer: current token: " + token)
    try:
        token = tokenizer()
        logging.debug("tokenizer: next token: " + token)
    except StopIteration:
        logging.debug("tokenizer: consumed all stream")
        token = None

def parse_aux(clazz, level):
    global token


    dbg = lambda m:logging.debug(str(level)+" "*level + m);

    if not token:
        return None

    dbg("curren token= " + str(token))

    parsed_object = None

    if issubclass(clazz, TE):
        dbg("must parse TE "+clazz.__name__)
        possible_object = clazz()
        possible_object.value = token
        does_match = re.match(possible_object.expression, token)
        if not does_match:
            dbg("RE does not match for token %s" % token)
        if does_match and possible_object.canparse():
            parsed_object = possible_object
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
                            x = parse_aux(clazz3, level+1)
                            if not x:
                                dbg("could not parse: %s" % clazz3.__name__)
                                break
                            elif x.canparse():
                                possible_object.add(x)
                            else:
                                break
                    else:
                        subs = parse_aux(p,level+1)
                        if subs and subs.canparse():
                            dbg(">>parsed NTE [%s/%s]: %s" %(clazz.__name__,p.__name__, subs))
                            if isinstance(subs,clazz):
                                possible_object = subs
                            else:
                                possible_object.add(subs)
                        else:
                            possible_object = None
                            break
                parsed_object = possible_object

            else:
                assert False, "unexpected production item: " + str(r)

            if parsed_object:
                break

    if parsed_object and parsed_object.canparse():

        dbg("finishing parse of " + clazz.__name__ +
            " with parse_tree: " + parsed_object.dump())
    else:
        dbg(">>parsing NTE "+clazz.__name__+" failed, retreat")
        return None


    if parsed_object:
        parsed_object.postparse()
    return parsed_object


def parse(f, toplevel):

    global token
    global tokenizer
    tokenizer = tokenize(f).next
    token = tokenizer()
    parse_data = parse_aux(toplevel, 0)

    assert token == None, "parse error: not all stream consumed"

    return parse_data

