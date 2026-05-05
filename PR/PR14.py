code = []
with open("ASG1.asm") as f:
    code = f.readlines()

symtab = {"A": 1, "B": 2, "C": 3, "L": 4}
littab = ["='5'", "='10'", "='5'"]

IS = {"LOAD": 1, "ADD": 2, "MULT": 3}
DL = {"DC": 1, "DS": 2}
AD = {"START": 1, "END": 2, "ORIGIN": 3, "EQU": 4, "LTORG": 5}

def get_sym_index(sym):
    return symtab.get(sym, 0)

def get_lit_index(lit):
    for i in range(len(littab)):
        if littab[i] == lit:
            return i + 1
    return 0

print("Intermediate Code:\n")

for line in code:
    parts = line.split()

    if parts[0] in AD:
        if len(parts) > 1:
            print(f"(AD,{AD[parts[0]]:02}) (C,{parts[1]})")
        else:
            print(f"(AD,{AD[parts[0]]:02})")

    elif len(parts) == 3 and parts[1] in DL:
        opcode = parts[1]
        operand = parts[2]
        print(f"(DL,{DL[opcode]:02}) (C,{operand})")

    else:
        if len(parts) == 3:
            opcode = parts[1]
            operand = parts[2]
        else:
            opcode = parts[0]
            operand = parts[1] if len(parts) > 1 else ""

        if opcode in IS:
            if operand.startswith("="):
                idx = get_lit_index(operand)
                print(f"(IS,{IS[opcode]:02}) (L,{idx})")
            else:
                idx = get_sym_index(operand)
                print(f"(IS,{IS[opcode]:02}) (S,{idx})")