# -----------------------------
# DATA STRUCTURES
# -----------------------------
MNT = {}
MDT = []


# -----------------------------
# PASS 1: BUILD MNT + MDT
# -----------------------------
def pass1(lines):
    intermediate = []
    i = 0

    while i < len(lines):
        line = lines[i].replace(",", " ").strip()

        if line.startswith("MACRO"):
            parts = line.split()

            macro_name = parts[1]
            formal_args = parts[2:]

            MNT[macro_name] = (len(MDT), formal_args)

            i += 1

            while i < len(lines) and lines[i].strip() != "MEND":
                MDT.append(lines[i].strip())
                i += 1

            MDT.append("MEND")

        else:
            if line and line != "MEND":
                intermediate.append(line)

        i += 1

    return intermediate


# -----------------------------
# SAFE SUBSTITUTION (TOKEN LEVEL)
# -----------------------------
def substitute(line, ALA):
    tokens = line.split()
    return " ".join([ALA.get(tok, tok) for tok in tokens])


# -----------------------------
# PASS 2: RECURSIVE EXPANSION
# -----------------------------
def expand_line(line):
    parts = line.split()

    # If macro call
    if parts and parts[0] in MNT:
        macro_name = parts[0]
        mdt_index, formal_args = MNT[macro_name]
        actual_args = parts[1:]

        ALA = dict(zip(formal_args, actual_args))

        expanded = []
        i = mdt_index

        while MDT[i] != "MEND":
            exp_line = MDT[i]

            # STEP 1: substitute arguments
            exp_line = substitute(exp_line, ALA)

            # STEP 2: recursive expansion
            expanded.extend(expand_line(exp_line))

            i += 1

        return expanded

    return [line]


def pass2(intermediate):
    output = []

    for line in intermediate:
        output.extend(expand_line(line))

    return output


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    with open("samplepgm.asm") as f:
        lines = [line.strip() for line in f if line.strip()]

    intermediate = pass1(lines)

    print("\n----- MNT -----")
    for k, v in MNT.items():
        print(k, "->", v)

    print("\n----- MDT -----")
    for i, line in enumerate(MDT):
        print(i, ":", line)

    print("\n----- INTERMEDIATE CODE -----")
    for line in intermediate:
        print(line)

    expanded = pass2(intermediate)

    print("\n----- EXPANDED CODE -----")
    for line in expanded:
        print(line)