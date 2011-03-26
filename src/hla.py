#! /usr/bin/env python2.6

from parse import *
from namespace import *

parse_tree = parse(open("test.hla", "rt").read())
logging.info("parsed: " + parse_tree.dump())


dump_namespace()
