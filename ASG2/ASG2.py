import os

def extract_lines(file: str)->list:
    with open(file, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def extract_instructions(line: list)->list:
    instructions = []
    for l in line:
        instructions.append(l.split())
    return instructions

MNT = {}
MDT = []
INTERMEDIATE_CODE = []

def analyze(extracted_lines: list)->dict:
    macro_name = None
    macro_flag = False
    
    for ins in extracted_lines:
        if 'MACRO' == ins[0]:
            macro_flag = True
            macro_name = ins[1]
            MNT[macro_name] = {}
            MNT[macro_name]['params'] = len(ins[2:])
            MNT[macro_name]['mdt_index'] = len(MDT) + 1
        elif 'MEND' == ins[0]:
            MDT.append(ins)
            macro_flag = False
            macro_name = None
        else:
            if macro_flag:
                MDT.append(ins)
            else:
                INTERMEDIATE_CODE.append(ins)
    
    # print("\nMNT:")
    # print(f"{'Name of Macro':<15}|", f"{'No. of Params':<15}|", f"{'Starting Index':<15} |")
    # print('-'*15 + '+' + '-'*16 + '+' + '-'*17 + '+')
    # for macro in MNT.keys():
    #     print(f"{macro:<15}|", f"{MNT[macro]['params']:<15}|", f"{MNT[macro]['mdt_index']:<15} |")
    # print('-'*15 + '+' + '-'*16 + '+' + '-'*17 + '+')
    
    # print("\nMDT:")
    # print(f"{'#':<15}|", f"{'MDT':<15}|")
    # print('-'*15 + '+' + '-'*16 + '+')
    # for code in MDT:
    #     print(f"{MDT.index(code)+1:<15}|", f"{' '.join(code):<15}|")
    
    # print("\nIntermediate Code:")
    # print(f"{'#':<15}|", f"{'Instrctions':<15}|")
    # print('-'*15 + '+' + '-'*16 + '+')
    # for code in INTERMEDIATE_CODE:
    #     print(f"{INTERMEDIATE_CODE.index(code)+1:<15}|", f"{' '.join(code):<15}|")

def expand():
    expanded_code = []
    for code in INTERMEDIATE_CODE:
        if code[0] in MNT.keys():
            macro_name = code[0]
            mdt_index = MNT[macro_name]['mdt_index']
            macro_ins = None
            while mdt_index <= len(MDT):
                macro_ins = MDT[mdt_index - 1]
                if 'MEND' in macro_ins:
                    break
                elif macro_ins[0] in MNT.keys():
                    nested_macro_name = macro_ins[0]
                    nested_mdt_index = MNT[nested_macro_name]['mdt_index']
                    while nested_mdt_index <= len(MDT):
                        nested_macro_ins = MDT[nested_mdt_index - 1]
                        if 'MEND' in nested_macro_ins:
                            break
                        if not nested_macro_ins[0] in MNT.keys():
                            expanded_code.append(nested_macro_ins)
                        nested_mdt_index += 1
                if not macro_ins[0] in MNT.keys():
                    expanded_code.append(macro_ins)
                mdt_index += 1
        else:
            if not code[0] in MNT.keys():
                expanded_code.append(code)
    
    print("\nExpanded Code:")
    print("\n".join([' '.join(code) for code in expanded_code]))

if __name__ == "__main__":
    file = './samplepgm.asm'
    lines = extract_lines(file)
    instructions = extract_instructions(lines)
    analyze(instructions)
    expand()