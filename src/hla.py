#! /usr/bin/env python2.6

from parse import parse
from ruledb import dump_ruledb
from namespace import dump_namespace

from modBase import Program
import logging

logging.basicConfig(level=logging.DEBUG)


parse_tree = parse(open("test.hla", "rt").read(), Program)
logging.info("parsed: " + parse_tree.dump())

assert type(parse_tree) == Program

open("output/main.c", "wt").write(parse_tree.render())


dump_namespace()
dump_ruledb()

