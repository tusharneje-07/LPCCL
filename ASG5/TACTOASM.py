import re
import sys

def generate_assembly(tac_lines):
    assembly = []

    for line in tac_lines:
        line = line.strip()

        # Remove numbering (1), 2), etc.)
        line = re.sub(r'^\d+\)\s*', '', line)

        # LABEL like #1
        if line.startswith("#"):
            label = line[1:]
            assembly.append(f"LABEL L{label}")
            continue

        # IF statement
        if line.startswith("if"):
            parts = re.findall(r'\w+|#\d+', line)
            temp = parts[1]
            label = parts[-1].replace("#", "")
            assembly.append(f"CMP {temp}, 0")
            assembly.append(f"JNE L{label}")
            continue

        # GOTO
        if line.startswith("goto"):
            label = re.search(r'#(\d+)', line).group(1)
            assembly.append(f"JMP L{label}")
            continue

        # Assignment
        if ":=" in line:
            lhs, rhs = line.split(":=")
            lhs = lhs.strip()
            rhs = rhs.strip()

            tokens = rhs.split()

            # Relational <
            if '<' in tokens:
                op1, _, op2 = tokens
                assembly.append(f"MOV R1, {op1}")
                assembly.append(f"CMP R1, {op2}")
                assembly.append(f"SETL {lhs}")

            # Binary operations
            elif len(tokens) == 3:
                op1, operator, op2 = tokens
                assembly.append(f"MOV R1, {op1}")

                if operator == '+':
                    assembly.append(f"ADD R1, {op2}")
                elif operator == '-':
                    assembly.append(f"SUB R1, {op2}")
                elif operator == '*':
                    assembly.append(f"MUL R1, {op2}")
                elif operator == '/':
                    assembly.append(f"DIV R1, {op2}")

                assembly.append(f"MOV {lhs}, R1")

            # Simple assignment
            else:
                assembly.append(f"MOV {lhs}, {rhs}")

    return assembly


# -------- MAIN --------
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            tac_lines = f.readlines()
    else:
        print("Enter TAC (end with empty line):")
        tac_lines = []
        while True:
            line = input()
            if not line:
                break
            tac_lines.append(line)

    asm = generate_assembly(tac_lines)

    print("\nGenerated Assembly Code:\n")
    for line in asm:
        print(line)


if __name__ == "__main__":
    main()