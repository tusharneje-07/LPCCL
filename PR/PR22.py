code = []
with open("ASG2.asm", "r") as f:
    code = f.readlines()

# Function to remove comments
def clean(line):
    return line.split(";")[0].strip()


mdt = []
macro_defs = {}

i = 0
while i < len(code):
    line = clean(code[i])

    if line.startswith("MACRO"):
        parts = line.split()
        name = parts[1]

        params = []
        if len(parts) > 2:
            params = [p.strip() for p in " ".join(parts[2:]).split(",")]

        macro_defs[name] = {"params": params, "body": []}

        i += 1
        while clean(code[i]) != "MEND":
            macro_defs[name]["body"].append(clean(code[i]))
            i += 1

    i += 1


# Replace parameters → #1, #2...
def replace_params(line, params):
    words = line.split()
    new_line = []

    for w in words:
        if w in params:
            idx = params.index(w) + 1
            new_line.append(f"#{idx}")
        else:
            new_line.append(w)

    return " ".join(new_line)


# MDT with early expansion
for name in macro_defs:
    params = macro_defs[name]["params"]
    body = macro_defs[name]["body"]

    for line in body:
        parts = line.split()

        # Nested macro
        if parts[0] in macro_defs:
            nested = parts[0]
            actual_args = parts[1:]

            n_params = macro_defs[nested]["params"]
            n_body = macro_defs[nested]["body"]

            for nline in n_body:
                temp = nline
                for j in range(len(n_params)):
                    temp = temp.replace(n_params[j], actual_args[j])
                mdt.append(temp)

        else:
            mdt.append(replace_params(line, params))

    mdt.append("MEND")


# OUTPUT
print("MDT:\n")
for i, line in enumerate(mdt, start=1):
    print(i, line)