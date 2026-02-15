import os

KEYWORD_INSTRUCTIONS = ["LOAD", "ADD", "MULT"]
KEYWORD_COMP_DIRECTIVES = ["START", "ORIGIN", "LTORG", "END"]
KEYWORD_DATA_DEFINATION = ["DC", "DS"]
LC = 0

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

literal_table = {}

pool_table = []

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

def analyze(extracted_lines: list)->dict:
    global LC
    print('-'*3 + '+' + '-'*31 + '+' + '-'*8 + '+')
    print(f"{'No.':<3}|", f"{'Instruction':<30}|", f"{'LC':<6} |")
    print('-'*3 + '+' + '-'*31 + '+' + '-'*8 + '+')
    LTORG_FLAG = False
    pool_table.append(1)  # First pool starts at literal index 1
    for ins in extracted_lines:
        
        if LTORG_FLAG:        
            if ins[0] in literal_table.keys():
                literal_table[ins[0]] = LC
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{LC:<6} |")
                LC += 1
            else:
                for lit in literal_table.keys():
                    if literal_table[lit] is None:
                        literal_table[lit] = LC
                        print(f"{extracted_lines.index(ins)+1:<3}|", f"{lit:<30}|", f"{LC:<6} |")
                        LC += 1
                LTORG_FLAG = False
        else:
            if is_symobol(ins[0]):
                symbol_table[ins[0]] = LC
            
            if is_literal(ins[-1]):
                literal_table[ins[-1]] = None
            
            if 'START' in ins:
                LC = int(ins[ins.index('START') + 1])
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{0:<6} |")
            elif 'ORIGIN' in ins:
                instruction = ins[ins.index('ORIGIN') + 1]
                if instruction.isdigit():
                    LC = int(instruction)
                else:
                    LC = int(symbol_table[instruction.split('+')[0]]) + int(instruction.split('+')[1])
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{'':<6} |")
            elif 'LTORG' in ins:
                LTORG_FLAG = True
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{'':<6} |")
                # Add next pool starting index to pool table
                pool_table.append(len(literal_table) + 1)
            elif 'DS' in ins:
                size = int(ins[ins.index('DS') + 1])
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{LC:<6} |")
                LC += size
            elif 'END' in ins:
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{'':<6} |")
                for lit in literal_table.keys():
                    if literal_table[lit] is None:
                        literal_table[lit] = LC
                        print(f"{extracted_lines.index(ins)+1:<3}|", f"{lit:<30}|", f"{LC:<6} |")
                        LC += 1
                
            elif 'EQU' in ins:
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{'':<6} |")
            else:
                print(f"{extracted_lines.index(ins)+1:<3}|", f"{' '.join(ins):<30}|", f"{LC:<6} |")
                LC += 1
            
        # print('-'*3 + '+' + '-'*31 + '+' + '-'*8 + '+')

    count_comments = 0
    count_instructions = 0
    count_compiler_directives = 0
    
    comments = []
    instructions = []
    compiler_directives = []
    
    for line in extracted_lines:
        for instruction in line:
            if instruction.startswith(';'):
                count_comments += 1
                comments.append(f"{extracted_lines.index(line)+1}     " + ' '.join(line[line.index(instruction):]) + f"    {line[line.index(';'):]}") 
            elif instruction in KEYWORD_INSTRUCTIONS:
                count_instructions += 1
                instructions.append(f"{extracted_lines.index(line)+1}     " + ' '.join(line) + f"    {line}")
            
            elif instruction in KEYWORD_COMP_DIRECTIVES:
                count_compiler_directives += 1
                compiler_directives.append(f"{extracted_lines.index(line)+1}     " + ' '.join(line) + f"    {line}")

    
    print("\n\nSymbol Table:")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    print(f"{"#R":<5}|",f"{"SYMBOL":<10}|", f"{"ADDRESS":<7} |")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    for sym in symbol_table.keys():
        print(f"{list(symbol_table.keys()).index(sym)+1:<5}|",f"{sym:<10}|", f"{symbol_table[sym]:<7} |")
    
    print("\n\nLiteral Table:")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    print(f"{"#R":<5}|",f"{"LITERAL":<10}|", f"{"ADDRESS":<7} |")
    print('-'*5 + '+' + '-'*11 + '+' + '-'*9 + '+')
    for lit in literal_table.keys():
        print(f"{list(literal_table.keys()).index(lit)+1:<5}|",f"{lit:<10}|", f"{literal_table[lit]:<7} |")
    
    print("\n\nPool Table:")
    print('-'*5 + '+' + '-'*18 + '+')
    print(f"{"#P":<5}|", f"{"LITERAL INDEX":<16} |")
    print('-'*5 + '+' + '-'*18 + '+')
    for i, pool in enumerate(pool_table):
        print(f"{i+1:<5}|", f"{pool:<16} |")
    
if __name__ == "__main__":
    file = './sample.asm'
    lines = extract_lines(file)
    instructions = extract_instructions(lines)
    analyze(instructions)