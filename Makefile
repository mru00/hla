.PHONY: update_dynparser test doc

doc:
	$(MAKE) -C doc doc

update_dynparser:
	$(MAKE) -C ../dynparser dist
	cp -a ../dynparser/dist/dynparser src

test:
	$(MAKE) -C test test