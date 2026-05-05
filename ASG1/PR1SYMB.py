LC = 0
LITTAB = []

def is_lit(x): return x.startswith("=")

def read(file):
    return [l.split() for l in open(file) if l.strip()]

def add_literal(x):
    if x not in [l["name"] for l in LITTAB]:
        LITTAB.append({"name": x, "addr": None})

def assign_literals(start):
    global LC
    for i in range(start, len(LITTAB)):
        if LITTAB[i]["addr"] is None:
            LITTAB[i]["addr"] = LC
            LC += 1

def make_literal_table(code):
    global LC
    pool_start = 0

    for line in code:
        for token in line:
            if is_lit(token):
                add_literal(token)

        if "START" in line:
            LC = int(line[1])

        elif "LTORG" in line:
            assign_literals(pool_start)
            pool_start = len(LITTAB)

        elif "END" in line:
            assign_literals(pool_start)

        else:
            LC += 1

    print("\nLITERAL TABLE")
    for i,l in enumerate(LITTAB,1):
        print(i, l["name"], l["addr"])

code = read("sample_ic.asm")
make_literal_table(code)