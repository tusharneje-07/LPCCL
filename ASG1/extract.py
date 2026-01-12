import os
KEYWORD_INSTRUCTIONS = ["LOAD", "ADD", "MULT"]
KEYWORD_COMP_DIRECTIVES = ["START", "ORIGIN", "LTORG", "END"]
KEYWORD_DATA_DEFINATION = ["DC", "DS"]

def extract_lines(file: str)->list:
    with open(file, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def extract_instructions(line: list)->list:
    instructions = []
    for l in line:
        instructions.append(l.split())
    return instructions

def analyze(extracted_lines: list)->dict:
    count_comments = 0
    count_instructions = 0
    count_compiler_directives = 0
    count_data_definitions = 0
    
    comments = []
    instructions = []
    compiler_directives = []
    data_definitions = []
    
    
    
    for line in extracted_lines:
        for instruction in line:
            if instruction.startswith(';'):
                count_comments += 1
                comments.append(f"{extracted_lines.index(line)+1}     " + ' '.join(line[line.index(instruction):]))
                # break
            elif instruction in KEYWORD_INSTRUCTIONS:
                count_instructions += 1
                instructions.append(f"{extracted_lines.index(line)+1}     " + ' '.join(line))
            
            elif instruction in KEYWORD_COMP_DIRECTIVES:
                count_compiler_directives += 1
                compiler_directives.append(f"{extracted_lines.index(line)+1}     " + ' '.join(line))

    print(f"[COMMENTS] ({count_comments}):\n")
    print('\n'.join(comments))
    print(f"\n[INSTRUCTIONS] ({count_instructions}):")
    print('\n'.join(instructions))
    print(f"\n[COMPILER DIRECTIVES] ({count_compiler_directives}):")
    print('\n'.join(compiler_directives))
    
if __name__ == "__main__":
    file = './testpgm.asm'
    lines = extract_lines(file)
    instructions = extract_instructions(lines)
    analyze(instructions)