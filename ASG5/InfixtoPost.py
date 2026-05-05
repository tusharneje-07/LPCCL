import re

temp_count = 1

def new_temp():
    global temp_count
    temp = f"t{temp_count}"
    temp_count += 1
    return temp

def precedence(op):
    if op in ('+','-'): return 1
    if op in ('*', '/'): return 2
    else: return 0
    
def infix_to_postfix(expr):
    stack = []
    output = []
    i = 0 
    tokens = re.findall(r'[a-zA-Z]+|\d+|[-+*/()]',expr)
    
    while i < len(tokens):
        token = tokens[i]
        
        if token == '-' and (i==0 or tokens[i-1] in '+-*/('):
            output.append('u-')
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
        i+=1
        

    while stack:
            output.append(stack.pop())
    
    return output

def generate_TAC(lhs,postfix):
    stack = []
    code = []
    
    for token in postfix:
        if token=='u-':
            op = stack.pop()
            temp = new_temp()
            code.append(f"{temp} := -{op}")
            stack.append(temp)
        elif token in '+-*/':
            op2 = stack.pop()
            op1 = stack.pop()
            temp = new_temp()
            code.append(f"{temp} := {op1} {token} {op2}")
            stack.append(temp)
        else:
            stack.append(token)
        
    res = stack.pop()
    code.append(f"{lhs} := {res}")
    return code

def process_lines(expr):
    lhs,rhs = expr.split("=")
    postfix = infix_to_postfix(rhs)
    print(lhs,rhs,postfix)

    tac = generate_TAC(lhs,postfix)
    return tac

def main():
    expr = "x=a+b*c/d-f"
    res = process_lines(expr)
    
    for line in res:
        print(line)
        
            
main()