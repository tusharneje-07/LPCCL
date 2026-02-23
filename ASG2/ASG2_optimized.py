import os

MNT = {}
MDT = []
INTERMEDIATE_CODE = []
PARAMETER_TBL = {}

# Maps macro -> { formal_param: positional_index }
FORMAL_POSITIONAL_TBL = {}

# List of macro calls: each item is {macro, call_no, mapping: {pos: actual}}
POSITIONAL_ACTUAL_TBL = []

MAX_RECURSION_DEPTH = 50


def extract_lines(file: str) -> list:
    cleaned = []
    with open(file, 'r') as f:
        for raw in f:
            # remove inline comments starting with ';'
            line = raw.split(';', 1)[0].strip()
            if line:
                cleaned.append(line)
    return cleaned


def extract_instructions(lines: list) -> list:
    return [line.split() for line in lines]

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

            # build formal->positional table for this macro
            FORMAL_POSITIONAL_TBL[macro_name] = {
                formal_params[i]: i + 1 for i in range(len(formal_params))
            }

        elif opcode == 'MEND':
            MDT.append(ins)
            macro_flag = False
            macro_name = None

        elif macro_flag:
            params = PARAMETER_TBL[macro_name]['formal_params']
            updated = ins.copy()

            # replace any token that matches a formal parameter with positional #n
            for j, tok in enumerate(updated):
                tok_clean = tok.replace(',', '')
                if tok_clean in params:
                    idx = params.index(tok_clean)
                    updated[j] = f"#{idx+1}"

            MDT.append(updated)

        else:
            # Non-macro line. If this is a macro call record positional->actual mapping
            if opcode in MNT:
                actual_params = [p.replace(',', '') for p in ins[1:]]
                pos_map = {i + 1: (actual_params[i] if i < len(actual_params) else '')
                           for i in range(MNT[opcode]['params'])}
                POSITIONAL_ACTUAL_TBL.append({
                    'macro': opcode,
                    'call_no': len(POSITIONAL_ACTUAL_TBL) + 1,
                    'mapping': pos_map,
                    'actuals': actual_params
                })

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

    print("\nFormal -> Positional Table:")
    for macro, mapping in FORMAL_POSITIONAL_TBL.items():
        print(f"{macro}:")
        for formal, pos in mapping.items():
            print(f"  {formal} -> position {pos}")

    print("\nPositional -> Actual Table (grouped by macro):")
    # group entries by macro name
    grouped = {}
    for entry in POSITIONAL_ACTUAL_TBL:
        grouped.setdefault(entry['macro'], []).append(entry)

    for macro in MNT.keys():
        entries = grouped.get(macro, [])
        params = MNT[macro]['params']
        print(f"\n{macro}: {params} param(s), {len(entries)} call(s)")

        if params == 0:
            if entries:
                print("  (no positional parameters) — calls recorded")
            else:
                print("  (no positional parameters)")
            continue

        # build header
        cols = ['Call#'] + [f"Pos{p}" for p in range(1, params+1)]
        widths = [8] + [15] * params
        header = "".join(f"{c:<{w}}" for c, w in zip(cols, widths))
        sep = "".join("-" * w for w in widths)
        print(header)
        print(sep)

        for e in entries:
            row = [str(e['call_no'])]
            for p in range(1, params+1):
                val = e['mapping'].get(p, '')
                row.append(val)
            print("".join(f"{c:<{w}}" for c, w in zip(row, widths)))

def expand():
    expanded_code = []

    for code in INTERMEDIATE_CODE:
        expanded_code.extend(expand_instruction(code, depth=0))

    print("\nExpanded Code:")
    print("\n".join(" ".join(line) for line in expanded_code))


def expand_instruction(instruction: list, depth: int):
    if depth > MAX_RECURSION_DEPTH:
        raise RecursionError("Maximum macro recursion depth exceeded")

    macro_name = instruction[0]

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

        result.extend(expand_instruction(resolved_line, depth + 1))

        mdt_index += 1

    return result


def resolve_line(line: list, param_map: dict) -> list:
    resolved = []

    for token in line:
        if token in param_map:
            resolved.append(param_map[token])
        else:
            resolved.append(token)

    return resolved

if __name__ == "__main__":
    # locate sample file relative to this script
    base = os.path.dirname(__file__)
    file = os.path.join(base, 'samplepgm.asm')
    lines = extract_lines(file)
    instructions = extract_instructions(lines)

    analyze(instructions)
    expand()
