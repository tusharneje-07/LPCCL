import os

KEYWORD_INSTRUCTIONS = ["LOAD", "ADD", "MULT"]
KEYWORD_COMP_DIRECTIVES = ["START", "ORIGIN", "LTORG", "END"]
KEYWORD_DATA_DEFINATION = ["DC", "DS"]
LC = 0

intermediate_code = []  # To store intermediate code

opcode_table = {
    # Imperative Statements (IS)
    "STOP":   {"class": "IS", "opcode": 0, "length": 1},
    "ADD":    {"class": "IS", "opcode": 1, "length": 1},
    "SUB":    {"class": "IS", "opcode": 2, "length": 1},
    "MULT":   {"class": "IS", "opcode": 3, "length": 1},
    "MOVER":  {"class": "IS", "opcode": 4, "length": 1},
    "MOVEM":  {"class": "IS", "opcode": 5, "length": 1},
    "COMP":   {"class": "IS", "opcode": 6, "length": 1},
    "BC":     {"class": "IS", "opcode": 7, "length": 1},
    "DIV":    {"class": "IS", "opcode": 8, "length": 1},
    "READ":   {"class": "IS", "opcode": 9, "length": 1},
    "PRINT":  {"class": "IS", "opcode": 10, "length": 1},
    "LOAD":   {"class": "IS", "opcode": 11, "length": 1},

    # Assembler Directives (AD)
    "START":  {"class": "AD", "opcode": 1, "length": 1},
    "END":    {"class": "AD", "opcode": 2, "length": 1},
    "ORIGIN": {"class": "AD", "opcode": 3, "length": 1},
    "EQU":    {"class": "AD", "opcode": 4, "length": 1},
    "LTORG":  {"class": "AD", "opcode": 5, "length": 1},
    # Declarative Statements (DL)
    "DS":     {"class": "DL", "opcode": 1, "length": 1},
    "DC":     {"class": "DL", "opcode": 2, "length": 1},

    # Registers (RG)
    "AREG":   {"class": "RG", "opcode": 1, "length": 1},
    "BREG":   {"class": "RG", "opcode": 2, "length": 1},
    "CREG":   {"class": "RG", "opcode": 3, "length": 1},
    "DREG":   {"class": "RG", "opcode": 4, "length": 1},

    # Condition Codes (CC)
    "EQ":     {"class": "CC", "opcode": 1, "length": 1},
    "LT":     {"class": "CC", "opcode": 2, "length": 1},
    "GT":     {"class": "CC", "opcode": 3, "length": 1},
    "LE":     {"class": "CC", "opcode": 4, "length": 1},
    "GE":     {"class": "CC", "opcode": 5, "length": 1},
    "ANY":    {"class": "CC", "opcode": 6, "length": 1},
}


symbol_table = {}

literal_table = []  # list of {'name': str, 'address': int|None}

pool_table = []  # list of 1-based start indices into literal_table

error_table = {
    "E01": "Duplicate Definition of Symbol",
    "E02": "Symbol Not Declared",
    "E03": "Invalid Mnemonic",
}

warning_table = {
    "W01": "Symbol Declared But Not Used",
}

errors   = []   
warnings = []   
symbol_usage = set()  

def extract_lines(file: str)->list:
    with open(file, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def extract_instructions(line: list)->list:
    instructions = []
    for l in line:
        instructions.append(l.split())
    return instructions

def is_symobol(token: str)->bool:
    if token.isidentifier() and token not in opcode_table.keys():
        return True
    return False

def is_literal(token: str)->bool:
    if token.startswith('='):
        return True
    return False

def get_symbol_index(symbol: str) -> int:
    symbols = list(symbol_table.keys())
    if symbol in symbols:
        return symbols.index(symbol) + 1
    return 0

def get_literal_index(literal: str, pool_start_0: int = 0) -> int:
    for i in range(pool_start_0, len(literal_table)):
        if literal_table[i]['name'] == literal:
            return i + 1
    return 0

def get_opcode_tuple(mnemonic: str) -> str:
    if mnemonic in opcode_table:
        info = opcode_table[mnemonic]
        return f"({info['class']}, {info['opcode']:02d})"
    return ""

def get_operand_tuple(operand: str, pool_start_0: int = 0) -> str:
    if operand.startswith("='") or operand.startswith("="):
        idx = get_literal_index(operand, pool_start_0)
        return f"(L, {idx:02d})"
    elif operand.isdigit():
        # Constant
        return f"(C, {operand})"
    elif operand in opcode_table and opcode_table[operand]['class'] == 'RG':
        # Register
        return f"({opcode_table[operand]['class']}, {opcode_table[operand]['opcode']:02d})"
    elif is_symobol(operand):
        # Symbol
        idx = get_symbol_index(operand)
        return f"(S, {idx:02d})"
    return ""

def analyze(extracted_lines: list)->dict:
    global LC
    global intermediate_code

    pool_table.append(1)
    current_pool_lit_start = 0     # 0-based index into literal_table where current pool begins
    symbol_order = []
    error_lines = set()  # set of 1-based line numbers with errors

    for line_num_p1, ins in enumerate(extracted_lines, start=1):
        if len(ins) >= 2 and ins[1] in opcode_table:
            lbl   = ins[0]
            mnem  = ins[1]
        else:
            lbl   = None
            mnem  = ins[0]

        if lbl:
            if lbl in symbol_table and symbol_table[lbl] is not None:
                errors.append((
                    line_num_p1, "E01",
                    f"Symbol '{lbl}' already defined at address {symbol_table[lbl]}"
                ))
                error_lines.add(line_num_p1)
            else:
                # Fresh definition OR resolving a forward reference
                symbol_table[lbl] = LC
                if lbl not in symbol_order:
                    symbol_order.append(lbl)

        valid_opcodes = {
            k for k, v in opcode_table.items()
            if v['class'] not in ('RG', 'CC')
        }
        if mnem not in valid_opcodes:
            errors.append((
                line_num_p1, "E03",
                f"Invalid mnemonic '{mnem}'"
            ))
            error_lines.add(line_num_p1)
            
        operand_start = 2 if lbl else 1
        for token in ins[operand_start:]:
            clean_token = token.split('+')[0].split('-')[0]
            if is_symobol(clean_token):
                symbol_usage.add(clean_token)
                if clean_token not in symbol_order:
                    symbol_order.append(clean_token)
                    symbol_table[clean_token] = None   # forward / unknown ref

        if is_literal(ins[-1]):
            already_in_pool = any(
                lit['name'] == ins[-1]
                for lit in literal_table[current_pool_lit_start:]
            )
            if not already_in_pool:
                literal_table.append({'name': ins[-1], 'address': None})

        if 'START' in ins:
            LC = int(ins[ins.index('START') + 1])
        elif 'ORIGIN' in ins:
            instruction = ins[ins.index('ORIGIN') + 1]
            if instruction.isdigit():
                LC = int(instruction)
            else:
                parts = instruction.replace('-', '+-').split('+')
                base   = parts[0]
                offset = int(parts[1]) if len(parts) > 1 else 0
                base_addr = symbol_table.get(base)
                if base_addr is not None:
                    LC = base_addr + offset
        elif 'LTORG' in ins:
            for i in range(current_pool_lit_start, len(literal_table)):
                if literal_table[i]['address'] is None:
                    literal_table[i]['address'] = LC
                    LC += 1
            current_pool_lit_start = len(literal_table)
            pool_table.append(current_pool_lit_start + 1)
        elif 'DS' in ins:
            LC += int(ins[ins.index('DS') + 1])
        elif 'END' in ins:
            for i in range(current_pool_lit_start, len(literal_table)):
                if literal_table[i]['address'] is None:
                    literal_table[i]['address'] = LC
                    LC += 1
        elif 'EQU' in ins:
            if lbl:
                operand = ins[ins.index('EQU') + 1]
                if symbol_table.get(operand) is not None:
                    symbol_table[lbl] = symbol_table[operand]
        else:
            LC += 1

    for sym, addr in symbol_table.items():
        if addr is None:
            # Find first line that uses this symbol as an operand
            ref_line = 0
            for ln, ins in enumerate(extracted_lines, start=1):
                for token in ins[1:]:
                    if token.split('+')[0].split('-')[0] == sym:
                        ref_line = ln
                        break
                if ref_line:
                    break
            errors.append((
                ref_line, "E02",
                f"Symbol '{sym}' used but never declared"
            ))
            error_lines.add(ref_line)

    for sym in symbol_table:
        if sym not in symbol_usage:
            # find declaration line
            decl_line = 0
            for ln, ins in enumerate(extracted_lines, start=1):
                if is_symobol(ins[0]) and ins[0] == sym:
                    decl_line = ln
                    break
            warnings.append((
                decl_line, "W01",
                f"Symbol '{sym}' declared but never used"
            ))
    
    LC = 0
    current_pool_idx = 0        # which pool we're in (0-based index into pool_table)
    processed_lit_0idx = set()  # 0-based indices of literal_table entries already printed
    
    SEP = "-" * 70
    HEADER = f"{'L#':<4}|{'LABEL':<8}|{'OPCODE':<8}|{'OPERAND':<12}|{'LC':<12}|{'OPCODE IC':<12}|{'OPERAND IC':<15}|"
    
    print("\n" + "=" * 70)
    print(" " * 15 + "INTERMEDIATE CODE GENERATION")
    print("=" * 70)
    print(HEADER)
    print(SEP)
    
    for idx, ins in enumerate(extracted_lines):
        line_num = idx + 1
        label = ""
        opcode_mnem = ""
        operand = ""
        lc_str = ""
        opcode_ic = ""
        operand_ic = ""
        
        tokens = ins[:]
        # Same rule as Pass 1: label only if the second token is a known mnemonic
        if len(tokens) >= 2 and tokens[1] in opcode_table:
            label = tokens[0]
            tokens = tokens[1:]
        if len(tokens) >= 1:
            opcode_mnem = tokens[0]
        if len(tokens) >= 2:
            operand = tokens[1]
        
        # 0-based start of CURRENT pool in literal_table
        pool_start_0 = pool_table[current_pool_idx] - 1
        
        if opcode_mnem == 'START':
            LC = int(operand)
            lc_str = "LC = 0"
            opcode_ic = get_opcode_tuple('START')
            operand_ic = f"(C, {operand})"
            
        elif opcode_mnem == 'END':
            opcode_ic = get_opcode_tuple('END')
            lc_str = ""
            
        elif opcode_mnem == 'ORIGIN':
            opcode_ic = get_opcode_tuple('ORIGIN')
            lc_str = ""
            if operand.isdigit():
                LC = int(operand)
                operand_ic = f"(C, {operand})"
            else:
                parts = operand.replace('-', '+-').split('+')
                base = parts[0]
                offset = int(parts[1]) if len(parts) > 1 else 0
                base_idx = get_symbol_index(base)
                operand_ic = f"(S, {base_idx:02d})" if offset >= 0 else f"(S, {base_idx:02d}){offset}"
                base_addr = symbol_table.get(base)
                if base_addr is not None:
                    LC = base_addr + offset
                    
        elif opcode_mnem == 'LTORG':
            opcode_ic = get_opcode_tuple('LTORG')
            lc_str = ""
            err_flag = " [ERR]" if line_num in error_lines else ""
            print(f"{line_num:<4}|{label:<8}|{opcode_mnem:<8}|{operand:<12}|{lc_str:<12}|{opcode_ic:<12}|{operand_ic:<15}|{err_flag}")
            intermediate_code.append({'lc': lc_str, 'opcode_ic': opcode_ic, 'operand_ic': operand_ic})
            # Print ONLY the literals belonging to the current pool (not future pools)
            next_pool_start_0 = pool_table[current_pool_idx + 1] - 1 if current_pool_idx + 1 < len(pool_table) else len(literal_table)
            for i in range(pool_start_0, next_pool_start_0):
                if i not in processed_lit_0idx and literal_table[i]['address'] is not None:
                    lit = literal_table[i]
                    processed_lit_0idx.add(i)
                    lit_lc = f"LC = {lit['address']}"
                    print(f"{'':<4}|{'':<8}|{'':<8}|{lit['name']:<12}|{lit_lc:<12}|{'':<12}|{f'(L, {i+1:02d})':<15}|")
                    intermediate_code.append({'lc': lit_lc, 'opcode_ic': '', 'operand_ic': f'(L, {i+1:02d})'})
                    LC = lit['address'] + 1
            current_pool_idx += 1  # Advance to next pool
            continue
            
        elif opcode_mnem == 'EQU':
            opcode_ic = get_opcode_tuple('EQU')
            if operand in symbol_table:
                operand_ic = f"(S, {get_symbol_index(operand):02d})"
            lc_str = ""
            
        elif opcode_mnem == 'DC':
            lc_str = f"LC = {LC}"
            opcode_ic = get_opcode_tuple('DC')
            operand_ic = f"(C, {operand})"
            LC += 1
            
        elif opcode_mnem == 'DS':
            lc_str = f"LC = {LC}"
            opcode_ic = get_opcode_tuple('DS')
            operand_ic = f"(C, {operand})"
            LC += int(operand)
            
        elif opcode_mnem in opcode_table and opcode_table[opcode_mnem]['class'] == 'IS':
            lc_str = f"LC = {LC}"
            opcode_ic = get_opcode_tuple(opcode_mnem)
            operand_ic = get_operand_tuple(operand, pool_start_0)
            LC += 1
            
        else:
            lc_str = f"LC = {LC}"
            if opcode_mnem in opcode_table:
                opcode_ic = get_opcode_tuple(opcode_mnem)
            operand_ic = get_operand_tuple(operand, pool_start_0) if operand else ""
            LC += 1
        
        intermediate_code.append({'lc': lc_str, 'opcode_ic': opcode_ic, 'operand_ic': operand_ic})
        err_flag = " [ERR]" if line_num in error_lines else ""
        print(f"{line_num:<4}|{label:<8}|{opcode_mnem:<8}|{operand:<12}|{lc_str:<12}|{opcode_ic:<12}|{operand_ic:<15}|{err_flag}")
        
        # After END, print remaining literals from the last pool
        if opcode_mnem == 'END':
            end_pool_start_0 = pool_table[current_pool_idx] - 1 if current_pool_idx < len(pool_table) else len(literal_table)
            for i in range(end_pool_start_0, len(literal_table)):
                if i not in processed_lit_0idx and literal_table[i]['address'] is not None:
                    lit = literal_table[i]
                    processed_lit_0idx.add(i)
                    lit_addr = lit['address']
                    print(f"{'':<4}|{'':<8}|{'':<8}|{lit['name']:<12}|{f'LC = {lit_addr}':<12}|{'':<12}|{f'(L, {i+1:02d})':<15}|")

    print(SEP)
    
    # ---- Symbol Table ----
    print("\n\nSymbol Table:")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    print(f"{'#R':<5}|", f"{'SYMBOL':<10}|", f"{'ADDRESS':<7} |")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    for i, sym in enumerate(symbol_table.keys()):
        addr = symbol_table[sym] if symbol_table[sym] is not None else "------"
        print(f"{i+1:<5}|", f"{sym:<10}|", f"{addr:<7} |")
    
    # ---- Literal Table ----
    print("\n\nLiteral Table:")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    print(f"{'#R':<5}|", f"{'LITERAL':<10}|", f"{'ADDRESS':<7} |")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    for i, lit in enumerate(literal_table):
        addr = lit['address'] if lit['address'] is not None else "UNDEF"
        print(f"{i+1:<5}|", f"{lit['name']:<10}|", f"{addr:<7} |")
    
    # ---- Pool Table ----
    print("\n\nPool Table:")
    print('-'*5 + '+' + '-'*9 + '+' + '-'*9 + '+')
    print(f"{'#R':<5}|", f"{'#P':<7} |", f"{'#L':<7} |")
    print('-'*5 + '+' + '-'*9 + '+' + '-'*9 + '+')
    for i in range(len(pool_table)):
        p_start = pool_table[i]
        p_end = pool_table[i + 1] - 1 if i + 1 < len(pool_table) else len(literal_table)
        p_count = p_end - p_start + 1
        print(f"{i+1:<5}|", f"{p_start:<7} |", f"{p_count:<7} |")

    # ---- Error Table ----
    print("\n\nErrors Detected:")
    W = 5; IW = 7; TW = 40; DW = 50
    SEP_E = '-'*W + '+' + '-'*IW + '+' + '-'*TW + '+' + '-'*DW + '+'
    print(SEP_E)
    print(f"{'LINE':<{W}}| {'ID':<{IW-1}}| {'TYPE':<{TW-1}}| {'DESCRIPTION':<{DW-1}}|")
    print(SEP_E)
    if errors:
        for (ln, eid, detail) in sorted(errors, key=lambda x: x[0]):
            etype = error_table.get(eid, eid)
            print(f"{ln:<{W}}| {eid:<{IW-1}}| {etype:<{TW-1}}| {detail:<{DW-1}}|")
    else:
        print("  No errors found.")
    print(SEP_E)

    # ---- Warning Table ----
    print("\n\nWarnings:")
    print(SEP_E)
    print(f"{'LINE':<{W}}| {'ID':<{IW-1}}| {'TYPE':<{TW-1}}| {'DESCRIPTION':<{DW-1}}|")
    print(SEP_E)
    if warnings:
        for (ln, wid, detail) in sorted(warnings, key=lambda x: x[0]):
            wtype = warning_table.get(wid, wid)
            print(f"{ln:<{W}}| {wid:<{IW-1}}| {wtype:<{TW-1}}| {detail:<{DW-1}}|")
    else:
        print("  No warnings.")
    print(SEP_E)

if __name__ == "__main__":
    file = './sample_ic.asm'
    lines = extract_lines(file)
    instructions = extract_instructions(lines)
    analyze(instructions)