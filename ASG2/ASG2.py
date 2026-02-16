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
PARAMETER_TBL = {}
def analyze(extracted_lines: list)->dict:
    macro_name = None
    macro_flag = False
    
    for ins in extracted_lines:
        if 'MACRO' == ins[0]:
            macro_flag = True
            macro_name = ins[1]
            MNT[macro_name] = {}
            MNT[macro_name]['params'] = len(ins[2:])
            parameters = []
            for param in ins[2:]:
                parameters.append(str(param).replace(',',''))
            PARAMETER_TBL[macro_name] = {'formal_params': parameters}
            MNT[macro_name]['mdt_index'] = len(MDT) + 1
        elif 'MEND' == ins[0]:
            MDT.append(ins)
            macro_flag = False
            macro_name = None
        else:
            if macro_flag:
                params = PARAMETER_TBL[macro_name]
                if len(ins) == 2:
                    if ins[1] in params['formal_params']:
                        ins[1] = f"#{params['formal_params'].index(ins[1]) + 1}"
                        MDT.append(ins)
                    else:
                        MDT.append(ins)
                else:
                    MDT.append(ins)
            else:
                INTERMEDIATE_CODE.append(ins)
    
    print("\nMNT:")
    print(f"{'Name of Macro':<15}|", f"{'No. of Params':<15}|", f"{'Starting Index':<15} |")
    print('-'*15 + '+' + '-'*16 + '+' + '-'*17 + '+')
    for macro in MNT.keys():
        print(f"{macro:<15}|", f"{MNT[macro]['params']:<15}|", f"{MNT[macro]['mdt_index']:<15} |")
    print('-'*15 + '+' + '-'*16 + '+' + '-'*17 + '+')
    
    print("\nMDT:")
    print(f"{'#':<15}|", f"{'MDT':<15}|")
    print('-'*15 + '+' + '-'*16 + '+')
    for code in MDT:
        print(f"{MDT.index(code)+1:<15}|", f"{' '.join(code):<15}|")
    
    print("\nIntermediate Code:")
    print(f"{'#':<15}|", f"{'Instrctions':<15}|")
    print('-'*15 + '+' + '-'*16 + '+')
    for code in INTERMEDIATE_CODE:
        print(f"{INTERMEDIATE_CODE.index(code)+1:<15}|", f"{' '.join(code):<15}|")

def expand():
    expanded_code = []
    for code in INTERMEDIATE_CODE:
        if code[0] in MNT.keys():
            macro_name = code[0]
            actual_params = code[1:]
            PARAMETER_TBL[macro_name]['actual_params'] = actual_params
            mdt_index = MNT[macro_name]['mdt_index']
            macro_ins = None
            while mdt_index <= len(MDT):
                macro_ins = MDT[mdt_index - 1]
                if 'MEND' in macro_ins:
                    break
                elif macro_ins[0] in MNT.keys():
                    nested_macro_name = macro_ins[0]
                    nested_macro_actual_params = macro_ins[1:]
                    nested_mdt_index = MNT[nested_macro_name]['mdt_index']
                    while nested_mdt_index <= len(MDT):
                        nested_macro_ins = MDT[nested_mdt_index - 1]
                        if 'MEND' in nested_macro_ins:
                            break
                        if not nested_macro_ins[0] in MNT.keys():
                            if nested_macro_ins[1].startswith('#'):
                                parameter_number = int(nested_macro_ins[1][1:])
                                if len(PARAMETER_TBL[nested_macro_name]) <= 1:
                                    actual_params_nf = ""
                                    for i, param in enumerate(nested_macro_actual_params):
                                        actual_params_nf += f"{param} "
                                    nested_macro_ins[1] = actual_params_nf
                                else:
                                    nested_macro_ins[1] = PARAMETER_TBL[nested_macro_name]['actual_params'][parameter_number - 1].replace(',','')
                                
                            expanded_code.append(nested_macro_ins)
                        nested_mdt_index += 1
                if not macro_ins[0] in MNT.keys():
                            if macro_ins[1].startswith('#'):
                                parameter_number = int(macro_ins[1][1:])
                                if len(PARAMETER_TBL[macro_name]) <= 1:
                                    actual_params_nf = ""
                                    for i, param in enumerate(PARAMETER_TBL[macro_name]['actual_params']):
                                        actual_params_nf += f"{param} "
                                    macro_ins[1] = actual_params_nf
                                else:
                                    macro_ins[1] = PARAMETER_TBL[macro_name]['actual_params'][parameter_number - 1].replace(',','')
                                
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