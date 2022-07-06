import sys


# Function defination for Opcode 
def Opcode(inst,reg=-1):

    #dictionary for Opcode
    dic= {"add":"10000", "sub":"10001",
        "mov":["10010","10011"],      #10010 for move immediate and 10011 for move register 
        "ld":"10100", "st":"10101", "mul":"10110", "div":"10111", "rs":"11000", "ls":"11001", "xor":"11010", "or":"11011", "and":"11100", "not":"11101", "cmp":"11110", "jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111", "hlt":"01010"}



    # checking condition for move immediate and move register 
    if(reg == 1):
        return dic["mov"][1]
    elif(reg == 0):
        return dic["mov"][0]
    return dic[inst]
    

#Function for Registers address
def reg_addr(reg):
    regs = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}
    if(reg in regs.keys()):
        return regs[reg]
    return -1

#Function for returning Instruction ka prakaar   (manjhe.... kis tarah ka instruction hai) 
def ISA_type(inst, reg= -1):
   
    prakaar= {  'A': ["add", "sub", "mul", "xor", "or", "and"],'B': ["mov", "rs", "ls"],'C': ["mov", "div", "not", "cmp"],'D': ["ld", "st"],'E': ["jmp", "jlt", "jgt", "je"],'F': ["hlt"]} 
    if(reg==0):
        return 'B'
    if(reg==1):
        return 'C'
    for i in prakaar.keys():
        if inst in prakaar[i]:
            return i
    return -1


#Function for Binary
def Binary_Converter(Num):
    binary = bin(Num)[2::]
    result = '0'*(8-len(binary))+binary
    return result
    
tag = dict()    

Bin_res = [] 
Errors = []

ASM_Code = []
dec_var = True


for line in sys.stdin:                    # source --https://www.geeksforgeeks.org/python-sys-module/
    ASM_Code.append(line)
  
var = dict()

isHalt = False

varl = 0
for line in ASM_Code:
    if (not line):
        continue
    elif(line.split()[0] == "var"):
        varl += 1
    elif(not line):
        continue

    else:
        break


khaali_rekha = 0
temporary = varl



for line in ASM_Code:
    if(not line):
        khaali_rekha += 1


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

varl = temporary
dec_var = False

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

    #checking whether the ISA type of A and is present at line's second element
    if (ISA_type(cur_line[0]) == 'A' and len(cur_line) == 4):
            if (reg_addr(cur_line[1]) == -1 or reg_addr(cur_line[2]) == -1 or reg_addr(cur_line[3]) == -1):
                Errors.append("Error found at line " + str(lnum + varl+1) + ": Invalid Register!!!")
                continue
            if (reg_addr(cur_line[1]) == "111" or reg_addr(cur_line[2]) == "111" or reg_addr(cur_line[3]) == "111"):
                Errors.append("Error found at line " + str(lnum + varl+1) + ": Invalid FLAGS!!!")
                continue
            Bin_res.append(Opcode(cur_line[0]) + "00" + reg_addr(cur_line[1]) + reg_addr(cur_line[2]) + reg_addr(cur_line[3]))
            continue


    #print error message when ISA is at wrong place
    elif (ISA_type(cur_line[0]) == 'A'):
        Errors.append("Error found at line " + str(lnum+ varl + 1) + ": Invalid syntax of Instruction!!!")
        continue


    #checking whether the ISA type of B and is present at line's second element
    if (ISA_type(cur_line[0]) == 'B' and len(cur_line) == 3):
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


    #print error message when ISA is at wrong place
    elif(ISA_type(cur_line[0]) == 'B'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue


    #checking whether the ISA type of C and is present at line's second element
    if (ISA_type(cur_line[0]) == 'C' and len(cur_line) == 3):
        if (reg_addr(cur_line[1]) == -1 or reg_addr(cur_line[2]) == -1):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid Register!!!")
            continue
        if(reg_addr(cur_line[1]) == "111" or reg_addr(cur_line[2]) == "111"):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid FLAGS!!!")
            continue
        Bin_res.append(Opcode(cur_line[0]) + "00000" + reg_addr(cur_line[1]) + reg_addr(cur_line[2]))
        continue


    #print error message when ISA is at wrong place
    elif (ISA_type(cur_line[0]) == 'C'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue


    #checking whether the ISA type of D and is present at line's second element
    if (ISA_type(cur_line[0]) == 'D' and len(cur_line) == 3):
        if (reg_addr(cur_line[1]) == -1):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid Register!!!")
            continue
        if(reg_addr(cur_line[1]) == "111"):
            Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid FLAGS!!!")
            continue
        if (cur_line[2] not in var.keys()):
            if(cur_line[2] in tag.keys()):
                Errors.append("Error found at line " + str(lnum + varl + 1) + ": Label used as variable!!!")
                continue
            else:
                Errors.append("Error found at line " + str(lnum + varl + 1) + ": Undefined variable!!!")
                continue
        else:
            Bin_res.append(Opcode(cur_line[0]) + reg_addr(cur_line[1]) + var[cur_line[2]])
            continue


    #print error message when ISA is at wrong place    
    elif (ISA_type(cur_line[0]) == 'D'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue


    #checking whether the ISA type of E and is present at line's second element
    if (ISA_type(cur_line[0]) == 'E' and len(cur_line) == 2):
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


    #print error message when ISA is at wrong place
    elif (ISA_type(cur_line[0]) == 'E'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue
    

    #checking whether the ISA type of F and is present at line's second element
    if (ISA_type(cur_line[0]) == 'F' and len(cur_line) == 1):
        Bin_res.append(Opcode(cur_line[0]) + '0' * 11)
        isHalt = True
        continue


    #print error message when ISA is at wrong place
    elif (ISA_type(cur_line[0]) == 'F'):
        Errors.append("Error found at line " + str(lnum + varl + 1) + ": Invalid syntax of Instruction!!!")
        continue


#checking weather "hlt is present or not"
if (not isHalt):
    Errors.append("Error : No hlt instruction found!!!")



#checking for errors and print converted machine code while no error not found
if (len(Errors)):
    for error in Errors:
        print(error)
elif(len(Bin_res)>256):
    print("Error : Code length exceeds!!!")        
else:
    for sahi_uttar in Bin_res:
        print(sahi_uttar)
