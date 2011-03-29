.PHONY: update_dynparser test doc update_unclean-dynparser

doc:
	$(MAKE) -C doc doc

update_dynparser:
	$(MAKE) -C ../dynparser dist
	cp -a ../dynparser/dist/dynparser src

update_unclean-dynparser:
	$(MAKE) -C ../dynparser unclean-dist
	cp -a ../dynparser/dist/dynparser src

test:
	$(MAKE) -C test test