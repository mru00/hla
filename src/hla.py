#! /usr/bin/env python2.6

from parse import *
from namespace import *

import logging

logging.basicConfig(level=logging.DEBUG)


parse_tree = parse(open("test.hla", "rt").read())
logging.info("parsed: " + parse_tree.dump())


dump_namespace()
dump_ruledb()

