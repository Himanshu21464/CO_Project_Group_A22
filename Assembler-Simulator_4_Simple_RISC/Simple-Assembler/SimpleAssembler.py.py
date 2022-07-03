import sys

def Binary_Converter(Num):
    binary = bin(Num)[2::]
    result = '0'*(8-len(binary))+binary
    return result

def Opcode(ins,reg=-1):
    dic= {"add":"10000", "sub":"10001",
        "mov":["10010","10011"],  
        "ld":"10100", "st":"10101", "mul":"10110", "div":"10111", "rs":"11000", "ls":"11001", "xor":"11010", "or":"11011", "and":"11100", "not":"11101", "cmp":"11110", "jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111", "hlt":"01010"}

def ISA_type(ins, reg= -1):
   
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

def reg_addr(reg):
    regs = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}
    if(reg in regs.keys()):
        return regs[reg]
    return -1

ASM_Code = []
for line in sys.stdin:
    ASM_Code.append(line)

Bin_res = [] 
Errors = []  


isHalt = False
tag = dict()
var = dict()
dec_var = True

varl = 0
for line in ASM_Code:
    if (not line):
        continue
    elif(line.split()[0] == "var"):
        varl += 1
    else:
        break


khaali_rekha = 0
for line in ASM_Code:
    if(not line):
        khaali_rekha += 1

temporary = varl
nvar_add = len(ASM_Code) - varl - khaali_rekha
num=1
while(varl):
    if(not ASM_Code[0]):
        num += 1
        continue
    line = ASM_Code[0].split()
    if(line[0] == "var" and len(line) == 2):
        if(line[1] not in var.keys()):
            var[line[1]] = Binary_Converter(nvar_add)
            nvar_add += 1
            varl -= 1
            ASM_Code.pop(0)
            num+= 1
            continue
        else:
            Errors.append("Error found at line " + str(num) + ": Multiple declaration found!!!")
            num+= 1
            continue
    elif(line[0] == "var"):
        Errors.append("Error found at line " + str(num) + ": Invalid variable declaration!!!")
        varl-= 1
        ASM_Code.pop(0)
        num+= 1
        continue
    else:
        dec_var= False
        break
dec_var = False
varl = temporary


for lnum in range(len(ASM_Code)):
    if(not ASM_Code[lnum]):
        continue
    cur_line = ASM_Code[lnum].split()
    if (ASM_Code[lnum].split()[0][-1] == ":"):
        if((ASM_Code[lnum].split()[0][:len(ASM_Code[lnum].split()[0]) - 1:]) not in tag.keys()):
            tag[(ASM_Code[lnum].split()[0][:len(ASM_Code[lnum].split()[0]) - 1:])] = Binary_Converter(lnum)
            temporary = ""
            for i in range(1,len(ASM_Code[lnum].split())):
                temporary += ASM_Code[lnum].split()[i] + " "
            ASM_Code[lnum] = temporary
        else:
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Multiple declaration found!!!")
            continue

for lnum in range(len(ASM_Code)):


    cur_line = ASM_Code[lnum].split()
    if (not cur_line):
        continue
    if (cur_line[0] == "var" and not dec_var):
        Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Variable not declared!!!")
        continue
    if (cur_line[0][-1] == ":"):
        Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Multiple labels used!!!")
        continue


    if (isHalt):
        Errors.append("Error found at Line " + str(lnum + varl + 1) + ": htl is'nt used!!!")
        continue

    if (ISA_type(cur_line[0]) == -1 and cur_line[0] != "mov"):
        Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid instruction!!!")
        continue

    if (cur_line[0] == "mov" and len(cur_line) == 3):
        if (reg_addr(cur_line[2]) != -1):
            # mov reg1 reg2
            if (reg_addr(cur_line[1]) == -1 or reg_addr(cur_line[2]) == -1):
                Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid Register!!!")
                continue
            if(reg_addr(cur_line[1]) == "111"):
                Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid FLAGS!!!")
                continue
            Bin_res.append(Opcode(cur_line[0], 1) + "00000" + reg_addr(cur_line[1]) + reg_addr(cur_line[2]))
            continue
        elif (cur_line[2][1::].isdecimal()):
            # mov reg1 $Imm
            if (cur_line[2][0] != "$"):
                Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid syntax!!!")
                continue
            if (reg_addr(cur_line[1]) == -1):
                Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid Register!!!")
                continue
            if(reg_addr(cur_line[1]) == "111"):
                Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid FLAGS!!!")
                continue
            if (int(cur_line[2][1::]) < 0 or int(cur_line[2][1::]) > 255):
                Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid Immediate Value!!!")
                continue
            Bin_res.append(Opcode(cur_line[0], 0) + reg_addr(cur_line[1]) + Binary_Converter(int(cur_line[2][1::])))
            continue
    elif (cur_line[0] == "mov"):
        Errors.append("Error found at Line " + str(lnum + varl + 1) + ": Invalid syntax of instruction!!!")
        continue


    if (ISA_type(cur_line[0]) == 'a' and len(cur_line) == 4):
            if (reg_addr(cur_line[1]) == -1 or reg_addr(cur_line[2]) == -1 or reg_addr(cur_line[3]) == -1):
                Errors.append("Error found at line " + str(lnum + varl+1) + ": Invalid Register!!!")
                continue
            if (reg_addr(cur_line[1]) == "111" or reg_addr(cur_line[2]) == "111" or reg_addr(cur_line[3]) == "111"):
                Errors.append("Error found at line " + str(lnum + varl+1) + ": Invalid FLAGS!!!")
                continue
            Bin_res.append(Opcode(cur_line[0]) + "00" + reg_addr(cur_line[1]) + reg_addr(cur_line[2]) + reg_addr(cur_line[3]))
            continue
    elif (ISA_type(cur_line[0]) == 'a'):
        Errors.append("Error found at line " + str(lnum+ varl + 1) + ": Invalid syntax of Instruction!!!")
        continue

    if (ISA_type(cur_line[0]) == 'b' and len(cur_line) == 3):
        if (cur_line[2][0] != "$"):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Syntax Error!!!")
            continue
        if(int(cur_line[2][1::]) not in range(0,256)):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid Immediate Value!!!")
            continue
        if(reg_addr(cur_line[1])==-1):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid Register!!!")
            continue
        if(reg_addr(cur_line[1]) == "111"):
            Errors.append("Error found at line "+ str(lnum + varl + 1) + ": Invalid FLAGS!!!")
            continue
        Bin_res.append((Opcode(cur_line[0]) + reg_addr(cur_line[1]) + Binary_Converter(int(cur_line[2][1::]))))
        continue
    elif(ISA_type(cur_line[0]) == 'b'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue

    if (ISA_type(cur_line[0]) == 'c' and len(cur_line) == 3):
        if (reg_addr(cur_line[1]) == -1 or reg_addr(cur_line[2]) == -1):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid Register!!!")
            continue
        if(reg_addr(cur_line[1]) == "111" or reg_addr(cur_line[2]) == "111"):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid FLAGS!!!")
            continue
        Bin_res.append(Opcode(cur_line[0]) + "00000" + reg_addr(cur_line[1]) + reg_addr(cur_line[2]))
        continue
    elif (ISA_type(cur_line[0]) == 'c'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue

    if (ISA_type(cur_line[0]) == 'd' and len(cur_line) == 3):
        if (reg_addr(cur_line[1]) == -1):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid Register!!!")
            continue
        if(reg_addr(cur_line[1]) == "111"):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid FLAGS!!!")
            continue
        if (cur_line[2] not in varl.keys()):
            if(cur_line[2] in tag.keys()):
                Errors.append("Error found at line " + str(lnum + varl + 1) + ": Label used as variable!!!")
                continue
            else:
                Errors.append("Error found at line " + str(lnum + varl + 1) + ": Undefined variable!!!")
                continue
        else:
            Bin_res.append(Opcode(cur_line[0]) + reg_addr(cur_line[1]) + var[cur_line[2]])
            continue
    elif (ISA_type(cur_line[0]) == 'd'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue


    if (ISA_type(cur_line[0]) == 'e' and len(cur_line) == 2):
        inst = cur_line.pop(0)
        if (cur_line[0] not in tag.keys()):
            if (cur_line[0] in var.keys()):
                Errors.append("Error found at line " + str(lnum + varl + 1) + ": variable used as label!!!")
                continue
            else:
                Errors.append("Error found at line " + str(lnum + varl + 1) + ": Undefined label!!!")
                continue
        else:
            Bin_res.append(Opcode(inst) + '0' * 3 + tag[cur_line[0]])
            continue
    elif (ISA_type(cur_line[0]) == 'e'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue

    if (ISA_type(cur_line[0]) == 'f' and len(cur_line) == 1):
        Bin_res.append(Opcode(cur_line[0]) + '0' * 11)
        isHalt = True
        continue
    elif (ISA_type(cur_line[0]) == 'f'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue

if (not isHalt):
    Errors.append("Error : No hlt instruction found!!!")

if(len(Bin_res)>256):
    print("Error : Code length exceeds!!!")
elif (len(Errors)):
    for error in Errors:
        print(error)
else:
    for sahi_uttar in Bin_res:
        print(sahi_uttar)