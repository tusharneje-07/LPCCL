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
            INTERMEDIATE_CODE.append(ins)

    # collect macro calls from both top-level and MDT before printing
    collect_macro_calls()
    print_tables()


def collect_macro_calls():
    """Scan INTERMEDIATE_CODE and MDT for lines that are macro calls and
    populate POSITIONAL_ACTUAL_TBL. This ensures calls inside macro bodies
    (MDT) are also recorded."""
    POSITIONAL_ACTUAL_TBL.clear()
    # Use per-macro call numbering
    counters = {}

    # scan intermediate code (top-level calls)
    for ins in INTERMEDIATE_CODE:
        if not ins:
            continue
        op = ins[0]
        if op in MNT:
            counters.setdefault(op, 0)
            counters[op] += 1
            params = MNT[op]['params']
            actual_params = [p.replace(',', '') for p in ins[1:]]
            pos_map = {i + 1: (actual_params[i] if i < len(actual_params) else '')
                       for i in range(params)}
            POSITIONAL_ACTUAL_TBL.append({'macro': op, 'call_no': counters[op], 'mapping': pos_map})

    # scan MDT for macro calls inside macro bodies
    for line in MDT:
        if not line or line[0] == 'MEND':
            continue
        op = line[0]
        if op in MNT:
            counters.setdefault(op, 0)
            counters[op] += 1
            params = MNT[op]['params']
            actual_params = [p.replace(',', '') for p in line[1:]]
            pos_map = {i + 1: (actual_params[i] if i < len(actual_params) else '')
                       for i in range(params)}
            POSITIONAL_ACTUAL_TBL.append({'macro': op, 'call_no': counters[op], 'mapping': pos_map})


def print_tables():
    # --- MNT ---
    print("\nMNT:")
    mnt_rows = [(name, str(data['params']), str(data['mdt_index'])) for name, data in MNT.items()]
    mnt_h = ("Macro", "Params", "MDT Index")
    w0 = max([len(mnt_h[0])] + [len(r[0]) for r in mnt_rows] or [0])
    w1 = max([len(mnt_h[1])] + [len(r[1]) for r in mnt_rows] or [0])
    w2 = max([len(mnt_h[2])] + [len(r[2]) for r in mnt_rows] or [0])
    sep = f"+-{'-'*w0}-+-{'-'*w1}-+-{'-'*w2}-+"
    header = f"| {mnt_h[0]:<{w0}} | {mnt_h[1]:^{w1}} | {mnt_h[2]:^{w2}} |"
    print(sep)
    print(header)
    print(sep)
    for r in mnt_rows:
        print(f"| {r[0]:<{w0}} | {r[1]:^{w1}} | {r[2]:^{w2}} |")
    print(sep)

    # --- MDT ---
    print("\nMDT:")
    mdt_rows = [(str(i), ' '.join(ins)) for i, ins in enumerate(MDT)]
    mdt_h = ("Idx", "Instruction")
    w0 = max([len(mdt_h[0])] + [len(r[0]) for r in mdt_rows] or [0])
    w1 = max([len(mdt_h[1])] + [len(r[1]) for r in mdt_rows] or [0])
    sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
    print(sep)
    print(f"| {mdt_h[0]:<{w0}} | {mdt_h[1]:<{w1}} |")
    print(sep)
    for r in mdt_rows:
        print(f"| {r[0]:<{w0}} | {r[1]:<{w1}} |")
    print(sep)

    # --- Intermediate Code ---
    print("\nIntermediate Code:")
    ic_rows = [(str(i), ' '.join(ins)) for i, ins in enumerate(INTERMEDIATE_CODE)]
    ic_h = ("Idx", "Instruction")
    w0 = max([len(ic_h[0])] + [len(r[0]) for r in ic_rows] or [0])
    w1 = max([len(ic_h[1])] + [len(r[1]) for r in ic_rows] or [0])
    sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
    print(sep)
    print(f"| {ic_h[0]:<{w0}} | {ic_h[1]:<{w1}} |")
    print(sep)
    for r in ic_rows:
        print(f"| {r[0]:<{w0}} | {r[1]:<{w1}} |")
    print(sep)

    # --- Formal -> Positional ---
    print("\nFormal -> Positional Table:")
    for macro, mapping in FORMAL_POSITIONAL_TBL.items():
        rows = [(formal, str(pos)) for formal, pos in mapping.items()]
        if not rows:
            print(f"{macro}: (no formal parameters)")
            continue
        h = ("Formal", "Position")
        w0 = max([len(h[0])] + [len(r[0]) for r in rows])
        w1 = max([len(h[1])] + [len(r[1]) for r in rows])
        sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
        print(f"\n{macro}:")
        print(sep)
        print(f"| {h[0]:<{w0}} | {h[1]:^{w1}} |")
        print(sep)
        for r in rows:
            print(f"| {r[0]:<{w0}} | {r[1]:^{w1}} |")
        print(sep)

    # --- Positional -> Actual (grouped by macro) ---
    print("\nPositional -> Actual Table:")
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

        # compute widths per column
        calls = entries
        # header columns
        cols = ["#"] + [f"Pos{p}" for p in range(1, params+1)]
        # compute widths based on header and content
        widths = []
        # # width
        w_call = max(len(cols[0]), max((len(str(e['call_no'])) for e in calls), default=1))
        widths.append(w_call)
        for p in range(1, params+1):
            maxcell = max((len(e['mapping'].get(p, '')) for e in calls), default=0)
            widths.append(max(len(f"Pos{p}"), maxcell))

        # build separator
        sep = "+-" + "-+-".join('-'*w for w in widths) + "-+"
        header = "| " + " | ".join(f"{c:^{w}}" for c, w in zip(cols, widths)) + " |"
        print(sep)
        print(header)
        print(sep)

        for e in calls:
            row = [str(e['call_no'])] + [e['mapping'].get(p, '') for p in range(1, params+1)]
            line = "| " + " | ".join(f"{c:<{w}}" for c, w in zip(row, widths)) + " |"
            print(line)

        print(sep)

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
