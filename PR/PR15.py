# ---------------- INTERMEDIATE CODE ----------------
IC = [
    "(AD,01) (C,100)",
    "(IS,01) (S,1)",
    "(IS,01) (S,2)",
    "(IS,02) (L,1)",
    "(IS,03) (S,3)",
    "(DL,01) (C,5)",
    "(AD,02)"
]

# ---------------- SYMBOL TABLE ----------------
symtab = {
    1: 200,   # S,1 → address 200
    2: 201,
    3: 205
}

# ---------------- LITERAL TABLE ----------------
littab = {
    1: 300    # L,1 → address 300
}

# ---------------- MACHINE CODE GENERATION ----------------
print("Machine Code:\n")

for line in IC:
    parts = line.split()

    # Skip AD (assembler directives)
    if "(AD," in parts[0]:
        continue

    # DL (Declarative)
    if "(DL," in parts[0]:
        value = parts[1].replace("(C,", "").replace(")", "")
        print(f"00 0 {value}")
        continue

    # IS (Imperative)
    if "(IS," in parts[0]:
        opcode = parts[0].replace("(IS,", "").replace(")", "")

        operand = parts[1]

        # Symbol
        if "(S," in operand:
            idx = int(operand.replace("(S,", "").replace(")", ""))
            addr = symtab[idx]

        # Literal
        elif "(L," in operand:
            idx = int(operand.replace("(L,", "").replace(")", ""))
            addr = littab[idx]

        # Constant
        elif "(C," in operand:
            addr = operand.replace("(C,", "").replace(")", "")

        else:
            addr = 0

        print(f"{opcode} 0 {addr}")