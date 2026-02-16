MNT = {}
MDT = []
INTERMEDIATE_CODE = []
PARAMETER_TBL = {}

MAX_RECURSION_DEPTH = 50  # Safety guard


def extract_lines(file: str) -> list:
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def extract_instructions(lines: list) -> list:
    return [line.split() for line in lines]


# ---------------- PASS 1 ----------------
def analyze(extracted_lines: list) -> None:
    macro_name = None
    macro_flag = False

    for ins in extracted_lines:
        opcode = ins[0]

        if opcode == 'MACRO':
            macro_flag = True
            macro_name = ins[1]

            formal_params = [p.replace(',', '') for p in ins[2:]]

            MNT[macro_name] = {
                'params': len(formal_params),
                'mdt_index': len(MDT)
            }

            PARAMETER_TBL[macro_name] = {
                'formal_params': formal_params
            }

        elif opcode == 'MEND':
            MDT.append(ins)
            macro_flag = False
            macro_name = None

        elif macro_flag:
            params = PARAMETER_TBL[macro_name]['formal_params']
            updated = ins.copy()

            if len(ins) > 1 and ins[1].replace(',', '') in params:
                index = params.index(ins[1].replace(',', ''))
                updated[1] = f"#{index + 1}"

            MDT.append(updated)

        else:
            INTERMEDIATE_CODE.append(ins)

    print_tables()


def print_tables():
    print("\nMNT:")
    print(f"{'Macro':<15}|{'Params':<10}|{'MDT Index':<10}")
    print("-" * 40)
    for name, data in MNT.items():
        print(f"{name:<15}|{data['params']:<10}|{data['mdt_index']:<10}")

    print("\nMDT:")
    for i, ins in enumerate(MDT):
        print(f"{i:<3} | {' '.join(ins)}")

    print("\nIntermediate Code:")
    for i, ins in enumerate(INTERMEDIATE_CODE):
        print(f"{i:<3} | {' '.join(ins)}")


# ---------------- PASS 2 (Recursive Expansion) ----------------
def expand():
    expanded_code = []

    for code in INTERMEDIATE_CODE:
        expanded_code.extend(expand_instruction(code, depth=0))

    print("\nExpanded Code:")
    print("\n".join(" ".join(line) for line in expanded_code))


def expand_instruction(instruction: list, depth: int):
    """
    Recursively expands macros.
    """
    if depth > MAX_RECURSION_DEPTH:
        raise RecursionError("Maximum macro recursion depth exceeded")

    macro_name = instruction[0]

    # Not a macro call → return as-is
    if macro_name not in MNT:
        return [instruction]

    actual_params = [p.replace(',', '') for p in instruction[1:]]
    formal_params = PARAMETER_TBL[macro_name]['formal_params']

    # Create local parameter mapping (Scoped)
    param_map = {
        f"#{i+1}": actual_params[i] if i < len(actual_params) else ""
        for i in range(len(formal_params))
    }

    result = []

    mdt_index = MNT[macro_name]['mdt_index']

    while mdt_index < len(MDT):
        line = MDT[mdt_index]
        if line[0] == 'MEND':
            break

        resolved_line = resolve_line(line, param_map)

        # Recursive call if nested macro
        result.extend(expand_instruction(resolved_line, depth + 1))

        mdt_index += 1

    return result


def resolve_line(line: list, param_map: dict) -> list:
    """
    Replace #n parameters using current scope mapping.
    """
    resolved = []

    for token in line:
        if token in param_map:
            resolved.append(param_map[token])
        else:
            resolved.append(token)

    return resolved


# ---------------- MAIN ----------------
if __name__ == "__main__":
    file = './samplepgm.asm'
    lines = extract_lines(file)
    instructions = extract_instructions(lines)

    analyze(instructions)
    expand()
