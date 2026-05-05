code = []
with open("ASG2.asm", "r") as f:
    code = f.readlines()

mnt = []
mdt_index = 1

i = 0
while i < len(code):
    line = code[i].split(";")[0].strip()

    if line.startswith("MACRO"):
        parts = line.split()

        # Get macro name and parameters
        if len(parts) > 1:
            name = parts[1]
            params = parts[2:] if len(parts) > 2 else []
        else:
            i += 1
            continue

        # Count parameters
        param_count = 0
        if params:
            param_count = len(" ".join(params).split(","))

        # Add to MNT
        mnt.append((name, param_count, mdt_index))

        # Move inside macro body
        i += 1
        while i < len(code):
            body_line = code[i].split(";")[0].strip()
            mdt_index += 1

            if body_line == "MEND":
                break
            i += 1

    i += 1


# OUTPUT
print("MNT (Macro Name Table):")
print("Name\tParams\tMDT Index")
for name, p, idx in mnt:
    print(f"{name}\t{p}\t{idx}")