code = []
with open("ASG2.asm", "r") as f:
    code = f.readlines()

def clean(line):
    return line.split(";")[0].strip()

ic = []
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
        ic.append(line)


# OUTPUT
print("Intermediate Code:\n")
for line in ic:
    print(line)