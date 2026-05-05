code = []
with open("ASG1.asm") as f:
    code = f.readlines()

lc = 0
symtab = {}

def evaluate(expr):
    if "+" in expr:
        s, n = expr.split("+")
        return symtab[s] + int(n)
    return symtab.get(expr, 0)

for line in code:
    parts = line.split()

    if parts[0] == "START":
        lc = int(parts[1])

    elif parts[0] == "ORIGIN":
        lc = evaluate(parts[1])

    elif len(parts) == 3:
        label, opcode, operand = parts

        if opcode == "DC":
            symtab[label] = lc
            lc += 1

        elif opcode == "DS":
            symtab[label] = lc
            lc += int(operand)

        elif opcode == "EQU":
            symtab[label] = symtab.get(operand, 0)

        else:
            symtab[label] = lc
            lc += 1

    else:
        lc += 1

print("Symbol Table:")
for k, v in symtab.items():
    print(k, ":", v)