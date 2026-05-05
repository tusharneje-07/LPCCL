code = []
with open("ASG1.asm") as f:
    code = f.readlines()

lc = 0
littab = []
pooltab = [0]

def is_literal(op):
    return op.startswith("=")

for line in code:
    parts = line.split()

    if parts[0] == "START":
        lc = int(parts[1])

    elif parts[0] == "ORIGIN":
        # skipping expression eval for simplicity
        lc = lc  # assume already handled elsewhere

    elif parts[0] == "LTORG" or parts[0] == "END":
        # Assign addresses to unassigned literals
        for i in range(pooltab[-1], len(littab)):
            lit, addr = littab[i]
            if addr is None:
                littab[i] = (lit, lc)
                lc += 1
        if parts[0] == "LTORG":
            pooltab.append(len(littab))

    else:
        # check operand
        if len(parts) > 1:
            operand = parts[-1]
            if is_literal(operand):
                # avoid duplicate entries
                exists = False
                for lit, _ in littab:
                    if lit == operand:
                        exists = True
                        break
                if not exists:
                    littab.append((operand, None))

        lc += 1


# OUTPUT
print("Literal Table:")
for i, (lit, addr) in enumerate(littab):
    print(i, lit, ":", addr)

print("\nPool Table:")
for i, p in enumerate(pooltab):
    print(i, ":", p)