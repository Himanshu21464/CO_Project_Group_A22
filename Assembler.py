import sys

def Opcode():
    Dict= {"add"  :"10000", "sub"  :"10001",
        "mov"  :["10010","10011"],   #10010 for move immediate and 10011 for Move register
        "ld"   :"10100", "st"   :"10101", "mul"  :"10110","div"  :"10111","rs"   :"11000","ls"   :"11001", "xor"  :"11010","or"   :"11011", "and"  :"11100","not"  :"11101","cmp"  :"11110","jmp"  :"11111","jlt"  :"01100","jgt"  :"01101","je"   :"01111","hlt"  :"01010"}


def Binary_Converter(Num):
    binary = bin(Num)[2::]
    result = '0'*(8-len(binary))+binary
    return result


def Instruction(ins, reg= -1):
   
    prakaar= {  'a': ["add", "sub", "mul", "xor", "or", "and"],
                'b': ["mov", "rs", "ls"],
                'c': ["mov", "div", "not", "cmp"],
                'd': ["ld", "st"],
                'e': ["jmp", "jlt", "jgt", "je"],
                'f': ["hlt"]
            } 
    if(reg==0):
        return 'b'
    if(reg==1):
        return 'c'
    for i in prakaar.keys():
        if ins in prakaar[i]:
            return i
    return -1

def register_code(reg):
   
    reg = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}
    if(reg in reg.keys()):
        return reg[reg]
    return -1


# /////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////





code = []
for line in sys.stdin:
    code.append(line)  #append ith line of assembly code in list

Bin_res = []  # append the resulted binary in list
Errors_generated = []  # append the encountered errors in the list


isHalt = False
tag = dict()
Var = dict()
dec_var = True

var_lines = 0
for line in code:
    if (not line):
        continue
    elif(line.split()[0] == "var"):
        var_lines += 1
    else:
        break


khali_rekha = 0
for line in code:
    if(not line):
        khali_rekha += 1


temp = var_lines
Nxt_Var_Address = len(code) - var_lines - khali_rekha
N = 1
while(var_lines):
    if(not code[0]):
        N += 1
        continue
    line = code[0].split()
    if(line[0] == "var" and len(line) == 2):
        if(line[1] not in Var.keys()):
            Var[line[1]] = Binary_Converter(Nxt_Var_Address)
            Nxt_Var_Address += 1
            var_lines -= 1
            code.pop(0)
            N += 1
            continue
        else:
            Errors_generated.append("Error found at line " + str(N) + ": Multiple declarations for same variable!!!")
            N += 1
            continue
    elif(line[0] == "var"):
        Errors_generated.append("Error found at line " + str(N) + ": Invalid variable declaration!!!")
        var_lines -= 1
        code.pop(0)
        N += 1
        continue
    else:
        dec_var = False
        break
dec_var = False
var_lines = temp


for line_Num in range(len(code)):
    if(not code[line_Num]):
        continue
    cur_line = code[line_Num].split()
    if (code[line_Num].split()[0][-1] == ":"):
        if((code[line_Num].split()[0][:len(code[line_Num].split()[0]) - 1:]) not in tag.keys()):
            tag[(code[line_Num].split()[0][:len(code[line_Num].split()[0]) - 1:])] = Binary_Converter(line_Num)
            temp = ""
            for i in range(1,len(code[line_Num].split())):
                temp += code[line_Num].split()[i] + " "
            code[line_Num] = temp
        else:
            Errors_generated.append("Error found at line " + str(line_Num + var_lines + 1) + ": Multiple declarations for same label!!!")
            continue

for line_Num in range(len(code)):


    cur_line = code[line_Num].split()
    if (not cur_line):
        continue
    if (cur_line[0] == "var" and not dec_var):
        Errors_generated.append("Error found at line " + str(line_Num + var_lines + 1) + ": Variable not declared!!!")
        continue
    if (cur_line[0][-1] == ":"):
        Errors_generated.append("Error found at line " + str(line_Num + var_lines + 1) + ": Multiple labels used!!!")
        continue


    # -------------------------------------------------------------------------------------------------------
    if (isHalt):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": hlt not used in the end!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == -1 and cur_line[0] != "mov"):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (cur_line[0] == "mov" and len(cur_line) == 3):
        if (register_code(cur_line[2]) != -1):
            # mov reg1 reg2
            if (register_code(cur_line[1]) == -1 or register_code(cur_line[2]) == -1):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Register!!!")
                continue
            if(register_code(cur_line[1]) == "111"):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate use of FLAGS!!!")
                continue
            Bin_res.append(Opcode(cur_line[0], 1) + "00000" + register_code(cur_line[1]) + register_code(cur_line[2]))
            continue
        elif (cur_line[2][1::].isdecimal()):
            # mov reg1 $Imm
            if (cur_line[2][0] != "$"):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid syntax!!!")
                continue
            if (register_code(cur_line[1]) == -1):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Register!!!")
                continue
            if(register_code(cur_line[1]) == "111"):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate use of FLAGS!!!")
                continue
            if (int(cur_line[2][1::]) < 0 or int(cur_line[2][1::]) > 255):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate Immediate Value!!!")
                continue
            Bin_res.append(Opcode(cur_line[0], 0) + register_code(cur_line[1]) + Binary_Converter(int(cur_line[2][1::])))
            continue
    elif (cur_line[0] == "mov"):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == 'a' and len(cur_line) == 4):
        if (register_code(cur_line[1]) == -1 or register_code(cur_line[2]) == -1 or register_code(cur_line[3]) == -1):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Register!!!")
            continue
        if (register_code(cur_line[1]) == "111" or register_code(cur_line[2]) == "111" or register_code(cur_line[3]) == "111"):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate use of FLAGS!!!")
            continue
        Bin_res.append(Opcode(cur_line[0]) + "00" + register_code(cur_line[1]) + register_code(cur_line[2]) + register_code(cur_line[3]))
        continue
    elif (Instruction(cur_line[0]) == 'a'):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == 'b' and len(cur_line) == 3):
        if (cur_line[2][0] != "$"):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid syntax!!!")
            continue
        if(int(cur_line[2][1::]) not in range(0,256)):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate Immediate Value")
            continue
        if(register_code(cur_line[1])==-1):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Register!!!")
            continue
        if(register_code(cur_line[1]) == "111"):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate use of FLAGS!!!")
            continue
        Bin_res.append((Opcode(cur_line[0]) + register_code(cur_line[1]) + Binary_Converter(int(cur_line[2][1::]))))
        continue
    elif(Instruction(cur_line[0]) == 'b'):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == 'c' and len(cur_line) == 3):
        if (register_code(cur_line[1]) == -1 or register_code(cur_line[2]) == -1):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Register!!!")
            continue
        if(register_code(cur_line[1]) == "111" or register_code(cur_line[2]) == "111"):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate use of FLAGS!!!")
            continue
        Bin_res.append(Opcode(cur_line[0]) + "00000" + register_code(cur_line[1]) + register_code(cur_line[2]))
        continue
    elif (Instruction(cur_line[0]) == 'c'):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == 'd' and len(cur_line) == 3):
        if (register_code(cur_line[1]) == -1):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Register!!!")
            continue
        if(register_code(cur_line[1]) == "111"):
            Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Illegitimate use of FLAGS!!!")
            continue
        if (cur_line[2] not in Var.keys()):
            if(cur_line[2] in tag.keys()):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Misuse of label as variable")
                continue
            else:
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Use of undefined variable")
                continue
        else:
            Bin_res.append(Opcode(cur_line[0]) + register_code(cur_line[1]) + Var[cur_line[2]])
            continue
    elif (Instruction(cur_line[0]) == 'd'):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == 'e' and len(cur_line) == 2):
        ins = cur_line.pop(0)
        if (cur_line[0] not in tag.keys()):
            if (cur_line[0] in Var.keys()):
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Misuse of variable as label")
                continue
            else:
                Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Use of undefined tag")
                continue
        else:
            Bin_res.append(Opcode(ins) + '0' * 3 + tag[cur_line[0]])
            continue
    elif (Instruction(cur_line[0]) == 'e'):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

    # -------------------------------------------------------------------------------------------------------
    if (Instruction(cur_line[0]) == 'f' and len(cur_line) == 1):
        Bin_res.append(Opcode(cur_line[0]) + '0' * 11)
        isHalt = True
        continue
    elif (Instruction(cur_line[0]) == 'f'):
        Errors_generated.append("Error found at line" + str(line_Num + var_lines + 1) + ": Invalid Syntax for instruction!!!")
        continue
    # _______________________________________________________________________________________________________

if (not isHalt):
    Errors_generated.append("Error!!! No halt used in the end")

if(len(Bin_res)>256):
    print("Error!!! Code length exceeds")
elif (len(Errors_generated)):
    for error in Errors_generated:
        print(error)
else:
    for sahi_uttar in Bin_res:
        print(sahi_uttar)