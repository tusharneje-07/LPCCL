code = []
with open("ASG2.asm", "r") as f:
    code = f.readlines()

def clean(line):
    return line.split(";")[0].strip()

# Step 1: Store macros
macros = {}
i = 0

while i < len(code):
    line = clean(code[i])

    if line.startswith("MACRO"):
        parts = line.split()
        name = parts[1]

        params = []
        if len(parts) > 2:
            params = [p.strip() for p in " ".join(parts[2:]).split(",")]

        macros[name] = params

        # skip body
        i += 1
        while clean(code[i]) != "MEND":
            i += 1

    i += 1


# FORMAL vs POSITIONAL
print("Formal vs Positional:\n")

for name in macros:
    params = macros[name]

    print(name)
    if len(params) == 0:
        print("No Parameters")
    else:
        for i in range(len(params)):
            print(params[i], "→", f"#{i+1}")
    print()


# ACTUAL vs POSITIONAL
print("Actual vs Positional:\n")

inside_macro = False

for line in code:
    line = clean(line)

    if line.startswith("MACRO"):
        inside_macro = True
        continue

    if line == "MEND":
        inside_macro = False
        continue

    if inside_macro:
        continue

    if line == "":
        continue   # ✅ skip empty line

    parts = line.split()
    if len(parts) == 0:
        continue   # extra safety

    name = parts[0]

    if name in macros:
        params = macros[name]

        # get actual args
        args = parts[1:] if len(parts) > 1 else []
        if args:
            args = [a.strip() for a in " ".join(args).split(",")]

        print(name)

        if len(params) == 0:
            print("No Parameters")
        else:
            for i in range(len(args)):
                print(args[i], "→", f"#{i+1}")

        print()