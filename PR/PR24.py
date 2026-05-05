code = []
with open("ASG2.asm", "r") as f:
    code = f.readlines()

# Remove comments
def clean(line):
    return line.split(";")[0].strip()


# ---------------- STEP 1: STORE MACROS ----------------
macros = {}
i = 0

while i < len(code):
    line = clean(code[i])

    if line == "":
        i += 1
        continue

    if line.startswith("MACRO"):
        parts = line.split()

        # Handle cases like: MACRO ABC or MACRO ADD1 ARG
        name = parts[1]
        params = parts[2:] if len(parts) > 2 else []

        if params:
            params = [p.strip() for p in " ".join(params).split(",")]

        body = []
        i += 1

        while i < len(code) and clean(code[i]) != "MEND":
            line_body = clean(code[i])
            if line_body != "":
                body.append(line_body)
            i += 1

        macros[name] = (params, body)

    i += 1


# ---------------- STEP 2: EXPAND FUNCTION ----------------
def expand(line):
    if not line.strip():
        return []

    parts = line.split()
    if len(parts) == 0:
        return []

    name = parts[0]

    # Not a macro → return as it is
    if name not in macros:
        return [line]

    params, body = macros[name]

    args = parts[1:] if len(parts) > 1 else []
    if args:
        args = [a.strip() for a in " ".join(args).split(",")]

    result = []

    for bline in body:
        words = bline.split()
        new_line = []

        for w in words:
            if w in params:
                idx = params.index(w)
                new_line.append(args[idx])
            else:
                new_line.append(w)

        expanded_line = " ".join(new_line)

        # recursive expansion (nested macros)
        result.extend(expand(expanded_line))

    return result


# ---------------- STEP 3: GENERATE OUTPUT ----------------
expanded = []
inside_macro = False

for line in code:
    line = clean(line)

    if line == "":
        continue

    if line.startswith("MACRO"):
        inside_macro = True
        continue

    if line == "MEND":
        inside_macro = False
        continue

    if not inside_macro:
        expanded.extend(expand(line))


# ---------------- OUTPUT ----------------
print("Expanded Code:\n")
for line in expanded:
    print(line)