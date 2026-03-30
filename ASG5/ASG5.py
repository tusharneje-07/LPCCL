import sys
import re

temp_count = 1

def new_temp():
    global temp_count
    temp = f"t{temp_count}"
    temp_count += 1
    return temp

# Operator precedence
def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

# Convert infix to postfix
def infix_to_postfix(expr):
    stack = []
    output = []
    tokens = re.findall(r'[a-zA-Z]+|\d+|[-+*/()]', expr)

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle unary minus
        if token == '-' and (i == 0 or tokens[i-1] in '+-*/('):
            output.append('u-')  # unary minus
        elif token.isalnum():
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

# Generate TAC from postfix
def generate_TAC(lhs, postfix):
    stack = []
    code = []

    for token in postfix:
        if token == 'u-':
            operand = stack.pop()
            temp = new_temp()
            code.append(f"{temp} := - {operand}")
            stack.append(temp)

        elif token in '+-*/':
            op2 = stack.pop()
            op1 = stack.pop()
            temp = new_temp()
            code.append(f"{temp} := {op1} {token} {op2}")
            stack.append(temp)

        else:
            stack.append(token)

    result = stack.pop()
    code.append(f"{lhs} := {result}")

    return code

def process_line(line):
    if '=' not in line:
        print("Invalid expression")
        return

    lhs, rhs = line.split('=')
    lhs = lhs.strip()
    rhs = rhs.strip()

    postfix = infix_to_postfix(rhs)
    tac = generate_TAC(lhs, postfix)

    for line in tac:
        print(line)

# -------- MAIN --------
def main():
    if len(sys.argv) > 1:
        # Read from file
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        process_line(line)
        except FileNotFoundError:
            print("File not found!")
    else:
        # Manual input
        expr = input("Write Expression: ")
        process_line(expr)

if __name__ == "__main__":
    main()