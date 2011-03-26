.PHONY: profile

profile:
	python -m cProfile parse.py -o parse.prof
	python -c 'import pstats; p = pstats.Stats("parse.prof"); p.print_stats();'


.PHONY: coverage
coverage:
	python-coverage -e
	python-coverage -x parse.py
	python-coverage -a parse.py