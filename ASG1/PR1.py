LC = 0

OPTAB = {
    "STOP":("IS",0),"ADD":("IS",1),"SUB":("IS",2),"MULT":("IS",3),
    "MOVER":("IS",4),"MOVEM":("IS",5),"COMP":("IS",6),
    "BC":("IS",7),"DIV":("IS",8),"READ":("IS",9),"PRINT":("IS",10),

    "START":("AD",1),"END":("AD",2),"ORIGIN":("AD",3),
    "EQU":("AD",4),"LTORG":("AD",5),

    "DS":("DL",1),"DC":("DL",2),

    "AREG":("RG",1),"BREG":("RG",2),
    "CREG":("RG",3),"DREG":("RG",4)
}

SYMTAB, LITTAB, POOLTAB = {}, [], [0]
errors = []

def is_sym(x): return x.isidentifier() and x not in OPTAB
def is_lit(x): return x.startswith("=")

def get_sym(x):
    if x not in SYMTAB:
        SYMTAB[x] = None   # forward reference
    return list(SYMTAB).index(x)+1

def get_lit(x):
    for i,l in enumerate(LITTAB):
        if l["name"]==x: return i+1
    LITTAB.append({"name":x,"addr":None})
    return len(LITTAB)

def eval_expr(expr):
    if expr.isdigit():
        return int(expr)

    parts = expr.replace('-', '+-').split('+')
    base = parts[0]
    offset = int(parts[1]) if len(parts) > 1 else 0

    if base in SYMTAB and SYMTAB[base] is not None:
        return SYMTAB[base] + offset
    else:
        errors.append(f"Undefined symbol in expression: {expr}")
        return 0

def process_literals():
    global LC
    for i in range(POOLTAB[-1], len(LITTAB)):
        if LITTAB[i]["addr"] is None:
            LITTAB[i]["addr"] = LC
            LC += 1
    POOLTAB.append(len(LITTAB))

def read(file):
    return [l.split() for l in open(file) if l.strip()]

def analyze(code):
    global LC

    for line in code:
        label, op, *rest = (line+[None,None])[:3]

        # detect label properly
        if op not in OPTAB:
            op, rest = label, line[1:]
            label = None

        # symbol definition
        if label:
            if label in SYMTAB and SYMTAB[label] is not None:
                errors.append(f"Duplicate symbol: {label}")
            SYMTAB[label] = LC

        # --- directives ---
        if op == "START":
            LC = int(rest[0])
            print(f"(AD,01) (C,{rest[0]})")

        elif op == "END":
            process_literals()
            print("(AD,02)")

        elif op == "ORIGIN":
            LC = eval_expr(rest[0])
            print("(AD,03)")

        elif op == "EQU":
            if label:
                SYMTAB[label] = eval_expr(rest[0])
            print("(AD,04)")

        elif op == "LTORG":
            process_literals()
            print("(AD,05)")

        elif op == "DS":
            print(f"(DL,01) (C,{rest[0]})")
            LC += int(rest[0])

        elif op == "DC":
            print(f"(DL,02) (C,{rest[0]})")
            LC += 1

        # --- imperative ---
        elif op in OPTAB:
            cls, code_val = OPTAB[op]
            out = f"({cls},{code_val:02})"

            ops = []
            for x in rest:
                if is_lit(x):
                    ops.append(f"(L,{get_lit(x)})")
                elif is_sym(x):
                    ops.append(f"(S,{get_sym(x)})")
                elif x.isdigit():
                    ops.append(f"(C,{x})")
                elif x in OPTAB and OPTAB[x][0] == "RG":
                    ops.append(f"(RG,{OPTAB[x][1]})")

            print(out, *ops)
            LC += 1

    # --- final checks ---
    for sym, addr in SYMTAB.items():
        if addr is None:
            errors.append(f"Symbol used but not defined: {sym}")

    # ---- tables ----
    print("\nSYMBOL TABLE")
    for i,(k,v) in enumerate(SYMTAB.items(),1):
        print(i,k,v)

    print("\nLITERAL TABLE")
    for i,l in enumerate(LITTAB,1):
        print(i,l["name"],l["addr"])

    print("\nPOOL TABLE")
    for i,p in enumerate(POOLTAB,1):
        print(i,p+1)

    # ---- errors ----
    print("\nERRORS")
    if errors:
        for e in errors:
            print("-", e)
    else:
        print("No errors")


# run
code = read("sample_ic.asm")
analyze(code)