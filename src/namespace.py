


stores = {}

def add_symbol(store, symbol, value):
    assert type(store) == str
    assert type(symbol) == str
    assert value

    if store not in stores.keys():
        stores[store] = {}
    assert symbol not in stores[store].keys()
    stores[store][symbol] = value

def get_symbol(store, symbol):
    return stores[store][symbol]

def dump_namespace():
    print "===dump namespace"
    print "available stores: "
    for (key,store) in stores.items():
        print "  [" +key+ "]"
        for (symbol, value) in store.items():
            print "    " + symbol + " => " + str(value)
    print "===end dump namespace"
