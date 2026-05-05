import re

def is_constant(expr):
    return re.fullmatch(r"\d+(\.\d+)?", expr)

def is_variable(expr):
    return re.fullmatch(r"[a-zA-Z]\w*", expr)

def evaluate(expr):
    try:
        return str(eval(expr))
    except:
        return expr

def simplify(expr):
    if "*" in expr:
        a, b = expr.split("*", 1)
        if a == "1":
            return b
        if b == "1":
            return a
        if a == "0" or b == "0":
            return "0"

    if "+" in expr:
        a, b = expr.split("+", 1)
        if a == "0":
            return b
        if b == "0":
            return a

    return expr


def optimize_tac(tac):
    values = {}
    optimized = []

    for line in tac:
        if "=" not in line:
            optimized.append(line)
            continue

        left, right = line.split("=")
        left = left.strip()
        right = right.strip().replace(" ", "")

        # Safe propagation (ONLY constants or variables)
        for var in values:
            if is_constant(values[var]) or is_variable(values[var]):
                right = re.sub(rf"\b{var}\b", values[var], right)

        # Simplify algebra
        right = simplify(right)

        # Constant folding
        if re.fullmatch(r"\d+([+\-*/]\d+)", right):
            right = evaluate(right)

        # Store only safe mappings
        if is_constant(right) or is_variable(right):
            values[left] = right
        else:
            values[left] = left  # block further expansion

        optimized.append(f"{left} = {right}")

    return optimized


def dead_code_elimination(tac):
    used = set()
    result = []

    if tac:
        last_line = tac[-1]
        if "=" in last_line:
            left, _ = last_line.split("=")
            used.add(left.strip())

    for line in reversed(tac):
        if "=" not in line:
            result.append(line)
            continue

        left, right = line.split("=")
        left = left.strip()
        right = right.strip()

        if left in used:
            result.append(line)

            tokens = re.findall(r"[a-zA-Z]\w*", right)
            for t in tokens:
                used.add(t)

    return list(reversed(result))


if __name__ == "__main__":
    print("Enter TAC (empty line to stop):")

    tac = []
    while True:
        line = input()
        if line == "":
            break
        tac.append(line)

    opt = optimize_tac(tac)
    final = dead_code_elimination(opt)

    print("\nOptimized TAC:")
    for line in final:
        print(line)
        
# Input:

"""
t1 = a + b
t2 = t1 * 2
t3 = t2 + c
t4 = t3 * 1
t5 = t4 + 0
t6 = t5 + d
result = t6
"""
