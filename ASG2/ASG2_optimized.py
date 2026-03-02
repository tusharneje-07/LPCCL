import os

MNT = {}
MDT = []
INTERMEDIATE_CODE = []
PARAMETER_TBL = {}

MDT_COMMENTS = []
INTERMEDIATE_COMMENTS = []

FORMAL_POSITIONAL_TBL = {}
POSITIONAL_ACTUAL_TBL = []

MAX_RECURSION_DEPTH = 50


def extract_lines(file: str):
    code_lines = []
    comments = []

    with open(file, 'r') as f:
        for raw in f:
            raw = raw.rstrip('\n')

            if ';' in raw:
                parts = raw.split(';', 1)
                code = parts[0].strip()
                comment = parts[1].strip()
            else:
                code = raw.strip()
                comment = ''

            if code:
                code_lines.append(code)
                comments.append(comment)
            else:
                if comment:
                    code_lines.append('')
                    comments.append(comment)

    return code_lines, comments


def extract_instructions(lines):
    return [line.split() if line else [] for line in lines]


def analyze(extracted_lines, comments):
    macro_name = None
    macro_flag = False

    for idx, ins in enumerate(extracted_lines):
        comment = comments[idx] if idx < len(comments) else ''

        if not ins:
            INTERMEDIATE_CODE.append([])
            INTERMEDIATE_COMMENTS.append(comment)
            continue

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

            FORMAL_POSITIONAL_TBL[macro_name] = {
                formal_params[i]: i + 1
                for i in range(len(formal_params))
            }

        elif opcode == 'MEND':
            MDT.append(ins)
            MDT_COMMENTS.append(comment)
            macro_flag = False
            macro_name = None

        elif macro_flag:
            params = PARAMETER_TBL[macro_name]['formal_params']
            updated = ins.copy()

            for j, tok in enumerate(updated):
                tok_clean = tok.replace(',', '')
                if tok_clean in params:
                    idxp = params.index(tok_clean)
                    updated[j] = f"#{idxp+1}"

            MDT.append(updated)
            MDT_COMMENTS.append(comment)

        else:
            INTERMEDIATE_CODE.append(ins)
            INTERMEDIATE_COMMENTS.append(comment)

    collect_macro_calls()
    print_tables()


def collect_macro_calls():
    POSITIONAL_ACTUAL_TBL.clear()
    counters = {}

    for ins in INTERMEDIATE_CODE:
        if not ins:
            continue

        op = ins[0]
        if op in MNT:
            counters.setdefault(op, 0)
            counters[op] += 1

            params = MNT[op]['params']
            actual_params = [p.replace(',', '') for p in ins[1:]]

            pos_map = {
                i + 1: (actual_params[i] if i < len(actual_params) else '')
                for i in range(params)
            }

            POSITIONAL_ACTUAL_TBL.append({
                'macro': op,
                'call_no': counters[op],
                'mapping': pos_map
            })

    for line in MDT:
        if not line or line[0] == 'MEND':
            continue

        op = line[0]
        if op in MNT:
            counters.setdefault(op, 0)
            counters[op] += 1

            params = MNT[op]['params']
            actual_params = [p.replace(',', '') for p in line[1:]]

            pos_map = {
                i + 1: (actual_params[i] if i < len(actual_params) else '')
                for i in range(params)
            }

            POSITIONAL_ACTUAL_TBL.append({
                'macro': op,
                'call_no': counters[op],
                'mapping': pos_map
            })


def print_tables():

    print("\nMNT:")
    mnt_rows = [(n, str(v['params']), str(v['mdt_index']))
                for n, v in MNT.items()]

    h = ("Macro", "Params", "MDT Index")
    w0 = max([len(h[0])] + [len(r[0]) for r in mnt_rows] or [0])
    w1 = max([len(h[1])] + [len(r[1]) for r in mnt_rows] or [0])
    w2 = max([len(h[2])] + [len(r[2]) for r in mnt_rows] or [0])

    sep = f"+-{'-'*w0}-+-{'-'*w1}-+-{'-'*w2}-+"
    print(sep)
    print(f"| {h[0]:<{w0}} | {h[1]:^{w1}} | {h[2]:^{w2}} |")
    print(sep)
    for r in mnt_rows:
        print(f"| {r[0]:<{w0}} | {r[1]:^{w1}} | {r[2]:^{w2}} |")
    print(sep)

    print("\nMDT:")
    mdt_rows = [(str(i), ' '.join(ins)) for i, ins in enumerate(MDT)]
    h = ("Idx", "Instruction")
    w0 = max([len(h[0])] + [len(r[0]) for r in mdt_rows] or [0])
    w1 = max([len(h[1])] + [len(r[1]) for r in mdt_rows] or [0])

    sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
    print(sep)
    print(f"| {h[0]:<{w0}} | {h[1]:<{w1}} |")
    print(sep)
    for r in mdt_rows:
        print(f"| {r[0]:<{w0}} | {r[1]:<{w1}} |")
    print(sep)

    print("\nIntermediate Code:")
    ic_rows = [(str(i), ' '.join(ins))
               for i, ins in enumerate(INTERMEDIATE_CODE)]
    h = ("Idx", "Instruction")
    w0 = max([len(h[0])] + [len(r[0]) for r in ic_rows] or [0])
    w1 = max([len(h[1])] + [len(r[1]) for r in ic_rows] or [0])

    sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
    print(sep)
    print(f"| {h[0]:<{w0}} | {h[1]:<{w1}} |")
    print(sep)
    for r in ic_rows:
        print(f"| {r[0]:<{w0}} | {r[1]:<{w1}} |")
    print(sep)

    print("\nFormal vs Positional Table:")
    for macro, mapping in FORMAL_POSITIONAL_TBL.items():

        rows = [(k, str(v)) for k, v in mapping.items()]
        print(f"\n{macro}:")

        h = ("Formal", "Position")
        w0 = max([len(h[0])] + [len(r[0]) for r in rows])
        w1 = max([len(h[1])] + [len(r[1]) for r in rows])

        sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
        print(sep)
        print(f"| {h[0]:<{w0}} | {h[1]:^{w1}} |")
        print(sep)
        for r in rows:
            print(f"| {r[0]:<{w0}} | #{r[1]:^{w1}} |")
        print(sep)

    print("\nPositional vs. Actual Table:")

    grouped = {}
    for entry in POSITIONAL_ACTUAL_TBL:
        grouped.setdefault(entry['macro'], []).append(entry)

    for macro in MNT.keys():
        entries = grouped.get(macro, [])
        params = MNT[macro]['params']

        print(f"\n{macro}: {params} param(s), {len(entries)} call(s)")

        if params == 0:
            print("  (no positional parameters)")
            continue

        for entry in entries:
            print(f"\nCall #{entry['call_no']}")

            rows = []
            for pos in range(1, params + 1):
                rows.append((f"#{pos}", entry['mapping'].get(pos, '')))

            h = ("#", "Param")
            w0 = max(len(h[0]), max(len(r[0]) for r in rows))
            w1 = max(len(h[1]), max(len(r[1]) for r in rows))

            sep = f"+-{'-'*w0}-+-{'-'*w1}-+"
            print(sep)
            print(f"| {h[0]:<{w0}} | {h[1]:<{w1}} |")
            print(sep)

            for r in rows:
                print(f"| {r[0]:<{w0}} | {r[1]:<{w1}} |")

            print(sep)


def expand():
    expanded_code = []

    for i, code in enumerate(INTERMEDIATE_CODE):
        comment = INTERMEDIATE_COMMENTS[i]
        expanded_code.extend(expand_instruction(code, comment, 0))

    print("\nExpanded Code:")
    for tokens, comm in expanded_code:
        line = " ".join(tokens) if tokens else ''
        if comm:
            print(f"{line} ;{comm}" if line else f";{comm}")
        else:
            print(line)


def expand_instruction(instruction, comment, depth):
    if depth > MAX_RECURSION_DEPTH:
        raise RecursionError()

    if not instruction:
        return [(instruction, comment)]

    macro_name = instruction[0]

    if macro_name not in MNT:
        return [(instruction, comment)]

    actual = [p.replace(',', '') for p in instruction[1:]]
    formal = PARAMETER_TBL[macro_name]['formal_params']

    param_map = {
        f"#{i+1}": actual[i] if i < len(actual) else ""
        for i in range(len(formal))
    }

    result = []
    idx = MNT[macro_name]['mdt_index']

    while idx < len(MDT):
        line = MDT[idx]
        if line[0] == 'MEND':
            break

        resolved = resolve_line(line, param_map)
        comm = MDT_COMMENTS[idx]

        result.extend(expand_instruction(resolved, comm, depth + 1))
        idx += 1

    return result


def resolve_line(line, param_map):
    return [param_map.get(tok, tok) for tok in line]


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    file = os.path.join(base, 'samplepgm.asm')

    lines, comments = extract_lines(file)
    instructions = extract_instructions(lines)

    analyze(instructions, comments)
    expand()