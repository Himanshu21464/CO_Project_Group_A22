import math

def result(a,b):
    p= a-b
    if(p>0):
        print("-",p)
    else:
        temp3=-(2*p)+p
        print("+",temp3)


def Calculate_power(x):
    count=0
    if(x>0):
        while( x!=0):
            x=int(x/2)
            count+=1
        
    elif(x==0):
        return 0
    return count-1

def memorytype():
    print("-------------------------------------")
    print("|---------TYPES OF MEMORY-----------|")
    print("|-----------------------------------|")
    print("|                                   |")
    print("| 1. Bit Addressable Memory         |")
    print("| 2. Nibble Addressable Memory      |")
    print("| 3. Byte Addressable Memory        |")
    print("| 4. Word Addressable Memory        |")
    print("|-----------------------------------|\n")


def type1():
    print("---------------------TYPE OF INSTRUCTION-------------------------------------------")
    print("|                                                                                 |")
    print("| 1. Type A: <Q bit opcode> <P-bit address> <7 bit register>                      |")
    print("| 2. Type B: <Q bit opcode> <R bits filler> <7 bit register> <7 bit register>     |")
    print("-----------------------------------------------------------------------------------")

    Inst_length=int(input("Enter the length of ISA in bits: "))
    Reg_len=int(input("Enter length of Register in bits: "))
    print("\n")

    opcode=Calculate_power(Inst_length)
    Addr=Inst_length-(opcode+Reg_len)
    filler=Inst_length-((2*Reg_len)+opcode)
    max_inst=2**opcode
    max_reg=Inst_length

    print("Opcode                                  :",int(opcode))
    print("Address size                            :",int(Addr))
    print("Filler bits for 'Type B' ISA            :",int(filler))
    print("Maximum Instruction this ISA can Support:",int(max_inst))
    print("Maximum Registers this ISA can support  :",int(max_reg))
    print("\n")

def q2type1():
    mem_space=list(map(str,input("Enter Memory Space: ").split()))
    if(mem_space[1]=='KB'):
        mem_space_in_bytes=int(mem_space[0])*(2**10)
    elif(mem_space[1]=='MB'):
        mem_space_in_bytes=int(mem_space[0])*(2**20)
    elif(mem_space[1]=='GB'):
        mem_space_in_bytes=int(mem_space[0])*(2**30)
    elif(mem_space[1]=='Kb'):
        mem_space_in_bytes=int(mem_space[0])*(2**10)/8
    elif(mem_space[1]=='Mb'):
        mem_space_in_bytes=int(mem_space[0])*(2**20)/8
    elif(mem_space[1]=='Gb'):
        mem_space_in_bytes=int(mem_space[0])*(2**30)/8
    elif(mem_space[1]=='B'):
        mem_space_in_bytes=int(mem_space[0])
    elif(mem_space[1]=='b'):
        mem_space_in_bytes=int(mem_space[0])/8
    else:
        print("Error-The value you are trying to enter is either much large or very small :/ \n")
        exit()


    memorytype()

    mem_type=int(input("Select any one from the above Memory type: "))
    if(mem_type>4 and mem_type<1):
        print("Wrong Input !!!!\n")
        exit()
    else:    
        mem_pins=Calculate_power(mem_space_in_bytes)

    cpu_type=int(input("Enter the architecture bits of Supported System: "))
    print("\n")
    temp2=Calculate_power(cpu_type/8)
    word_pins=mem_pins-temp2
    bits_pins=mem_pins-3
    nibble_pins=mem_pins+1
    bytes_pins=mem_pins

    memorytype()
    Converted_memory_type=int(input("Select any above type of memory would want to change the current addressable memory to any of the rest 3 options: "))

    if(Converted_memory_type==1 and Converted_memory_type!=mem_type):
        result(mem_pins,bits_pins)

    elif(Converted_memory_type==2 and Converted_memory_type!=mem_type):
        result(mem_pins,nibble_pins)
    
    elif(Converted_memory_type==3 and Converted_memory_type!=mem_type):
        result(mem_pins,bytes_pins)

    elif(Converted_memory_type==4 and Converted_memory_type!=mem_type):
        result(mem_pins,word_pins)

    else:
        print("Wrong Input!!\n")
        exit()
    

def q2type2():
    cpu_bits=int(input("Enter the architecture bits of Supported System: "))
    addr_pins=int(input("Enter number of address pins: "))
    memorytype()
    mem_type=int(input("Select any one  from the above Memory type: "))
    if(mem_type==1):
        memory_size=int((2**addr_pins)*0.125)
    elif(mem_type==2):
        memory_size=int((2**addr_pins)*0.5)
    elif(mem_type==3):
        memory_size=int(2**addr_pins)
    elif(mem_type==4):
        memory_size=int((2**addr_pins)*(cpu_bits/8))
    
    print(memory_size,"Bytes")     
     


'''-----------------------MAIN PROGRAM----------------------------'''
print("-----------------------------------------------------------")
print("|Welcome to command line interface for Memory Organisation|")
print("-----------------------------------------------------------\n")

qt=int(input("Enter type of Question i.e. 1 or 2: "))
if(qt==1):
    type1()   
elif(qt==2):
    temp=int(input("Enter type of question i.e. 1 or 2:"))
    print("\n")
    if(temp==1):
        q2type1()
    elif(temp==2):
        q2type2()
    else:
        print("Wrong Input!!!\n")  
        exit()      
    
else:
    print("Wrong Input\n")
    exit()

