import sys
import re

temp_count = 1

def new_temp():
    global temp_count
    temp = f"t{temp_count}"
    temp_count += 1
    return temp

# ---------------- PRECEDENCE ----------------
def precedence(op):
    if op == 'u-': return 3
    if op in ('*', '/'): return 2
    if op in ('+', '-'): return 1
    return 0

# ---------------- INFIX → POSTFIX ----------------
def infix_to_postfix(expr):
    stack = []
    output = []

    tokens = re.findall(r'[a-zA-Z]+|\d+|<=|>=|==|!=|[-+*/()<>]', expr)

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # unary minus
        if token == '-' and (i == 0 or tokens[i-1] in '+-*/(<>='):
            token = 'u-'

        if token.isalnum():
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

        else:
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)

        i += 1

    while stack:
        output.append(stack.pop())

    return output

# ---------------- TAC EXPRESSION ----------------
def generate_TAC_expr(lhs, postfix):
    stack = []
    code = []

    for token in postfix:
        if token == 'u-':
            op = stack.pop()
            t = new_temp()
            code.append(f"{t} := - {op}")
            stack.append(t)

        elif token in '+-*/':
            b = stack.pop()
            a = stack.pop()
            t = new_temp()
            code.append(f"{t} := {a} {token} {b}")
            stack.append(t)

        else:
            stack.append(token)

    res = stack.pop()
    code.append(f"{lhs} := {res}")

    return code

# ---------------- CONDITION ----------------
def generate_condition_TAC(cond):
    m = re.match(r'(.+?)(<=|>=|==|!=|<|>)(.+)', cond)
    left, op, right = m.groups()

    left, right = left.strip(), right.strip()

    code = []
    postfix = infix_to_postfix(right)

    if len(postfix) > 1:
        t = new_temp()
        code.extend(generate_TAC_expr(t, postfix))
        right = t

    tcond = new_temp()
    code.append(f"{tcond} := {left} {op} {right}")

    return code, tcond

# ---------------- ASSIGNMENT ----------------
def process_assignment(line):
    lhs, rhs = line.split('=')
    return generate_TAC_expr(lhs.strip(), infix_to_postfix(rhs.strip()))

# ---------------- BLOCK PARSER ----------------
def extract_block(lines, start):
    block = []
    i = start
    depth = 0

    while i < len(lines):
        line = lines[i]

        if '{' in line:
            depth += 1
            if depth > 1:
                block.append(line)

        elif '}' in line:
            depth -= 1
            if depth == 0:
                return block, i
            else:
                block.append(line)
        else:
            block.append(line)

        i += 1

    return block, i

# ---------------- LABEL FORMAT ----------------
def format_label(idx):
    return "[i]" if idx == 0 else f"[i+{idx}]"

# ---------------- MAIN PROCESSOR ----------------
def process_lines(lines):
    code = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # -------- IF --------
        if line.startswith("if"):
            cond = re.search(r'\((.*?)\)', line).group(1)

            cond_code, tcond = generate_condition_TAC(cond)
            code.extend(cond_code)

            # placeholders
            if_index = len(code)
            code.append(f"if {tcond} goto ?")
            code.append("goto ?")

            # IF block
            if_block, end_if_idx = extract_block(lines, i)

            # check ELSE
            has_else = False
            else_block = []

            if end_if_idx + 1 < len(lines) and lines[end_if_idx + 1].startswith("else"):
                has_else = True
                else_block, end_else_idx = extract_block(lines, end_if_idx + 1)
                i = end_else_idx
            else:
                i = end_if_idx

            true_start = len(code)

            # generate IF block
            if_code = process_lines(if_block)
            code.extend(if_code)

            if has_else:
                jump_after_if = len(code)
                code.append("goto ?")

                false_start = len(code)

                else_code = process_lines(else_block)
                code.extend(else_code)

                end_all = len(code)

                # fix jumps
                code[if_index] = f"if {tcond} goto {format_label(true_start)}"
                code[if_index+1] = f"goto {format_label(false_start)}"
                code[jump_after_if] = f"goto {format_label(end_all)}"

            else:
                end_if = len(code)

                code[if_index] = f"if {tcond} goto {format_label(true_start)}"
                code[if_index+1] = f"goto {format_label(end_if)}"

        # -------- ASSIGNMENT --------
        else:
            code.extend(process_assignment(line.replace(';', '')))

        i += 1

    return code

# ---------------- MAIN ----------------
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            lines = [l.strip() for l in f if l.strip()]
    else:
        lines = []
        while True:
            l = input()
            if not l: break
            lines.append(l.strip())

    raw_code = process_lines(lines)

    final = []
    for idx, line in enumerate(raw_code):
        final.append(f"{format_label(idx)}: {line}")

    # blank last line
    final.append(f"{format_label(len(raw_code))}:")

    for l in final:
        print(l)

    with open("tac.txt", "w") as f:
        for l in final:
            f.write(l + "\n")

if __name__ == "__main__":
    main()