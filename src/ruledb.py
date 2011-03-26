rules = {}

def add_rule(clazz, arg):
    global rules
    if clazz not in rules.keys():
        rules[clazz] = [ arg ]
    else:
        rules[clazz].append(arg)

