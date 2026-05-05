import re
temp_count=1
label_count=1
 
def new_temp():
    global temp_count
    t=f"t{temp_count}"
    temp_count+=1
    return t
 
def new_label():
    global label_count
    l=f"L{label_count}"
    label_count+=1
    return l
 
def Arth_tac(expr):
    expr=expr.replace(" ","")
    if "=" in expr:
        lhs,rhs=expr.split("=")
    else:
        lhs=None
        rhs=expr
    tokens=re.findall(r"[A-Za-z0-9]+|[\+\-\*\/\(\)]",rhs)
    op_stack=[]
    val_stack=[]
    tac=[]
    precedence={'+':1,'-':1,'*':2,'/':2}
 
    def apply_op():
        op=op_stack.pop()
        b=val_stack.pop()
        a=val_stack.pop()
        t=new_temp()
        tac.append(f"{t} = {a} {op} {b}")
        val_stack.append(t)
 
    for line in tokens:
        if line.isalnum():
            val_stack.append(line)
        elif line == "(":
            op_stack.append(line)
        elif line == ")":
            while op_stack and op_stack[-1]!="(":
                apply_op()
            op_stack.pop()
        else:
            while (op_stack and op_stack[-1]!="(" and precedence.get(op_stack[-1],0) >= precedence[line]):
                apply_op()
            op_stack.append(line)
 
    while op_stack:
        apply_op()
 
    result=val_stack.pop()
    if lhs:
        tac.append(f"{lhs} = {result}")
    else:
        tac.append(result)
    return tac
 
def if_else():
    print("Enter condition:")
    condition=input()
    print("If statement:")
    if_stmt=input()
    print("Else statement:")
    else_stmt=input()
    tac=[]
    L1=new_label()
    L2=new_label()
    L3=new_label()
    tac.append(f"if {condition} goto {L1}")
    tac.append(f"goto{L2}")
    tac.append(f"{L1}:")
    tac.extend(Arth_tac(if_stmt))
    tac.append(f"goto {L3}")
    tac.append(f"{L2}:")
    tac.extend(Arth_tac(else_stmt))
    tac.append(f"{L3} :")
    return tac
 
print("1. Arithmetic Expression to TAC \n2. IF-ELSE to TAC")
choice=int(input())
if choice==1:
    print("Enter expression:")
    expr=input()
    result=Arth_tac(expr)
    for r in result:
        print(r)
elif choice==2:
    result=if_else()
    for r in result:
        print(r)