from sys import stdin

def intTOBin16bit(Val):
    rawBin = bin(Val)[2::]
    length = len(rawBin)
    binary = '0' * (16 - length) + rawBin
    return binary

def intToBin8bit(Val):
    rawBin = bin(Val)[2::]
    length = len(rawBin)
    binary = '0' * (8 - length) + rawBin
    return binary


def bin8bitToInt(binaryVal):
    return int(binaryVal, 2)


def isOverflow(Val):
    if(Val > (2**16 - 1)):
        return True
    else:
        return False


class Reg:
    
    flagRegr = "0000000000000000"
    Reg = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0,}
                  #R1       #R2       #R3       #R4       #R5       #R6       #R7

    
    def resetflagRegr(self):
        self.flagRegr = "0000000000000000"
   
    def setsOverflowFlag(self):
        self.flagRegr = "0000000000001000"
    
    def setsLessThanFlag(self):
        self.flagRegr = "0000000000000100"
    
    def setsGreaterThanFlag(self):
        self.flagRegr = "0000000000000010"
    
    def setsEqualsFlag(self):
        self.flagRegr = "0000000000000001"
    
    def printFlag(self):
        print(self.flagRegr, end=" ")
    
    def setReg(self, Reg_Addr, Val):
        if(not isOverflow(Val)):
            self.Reg[Reg_Addr] = Val
        else:
            rawBin = bin(Val)[2::]
            self.Reg[Reg_Addr] = int(rawBin[len(rawBin)-16::], 2)


    def getReg(self, Reg_Addr, Bin_or_Dec):
        if(Bin_or_Dec):
            if(Reg_Addr == "111"):
                return self.flagRegr
            rawBin = bin(self.Reg[Reg_Addr])[2::]
            if(len(rawBin)>16):
                return rawBin[len(rawBin)-16::]
            else:
                return intTOBin16bit(self.Reg[Reg_Addr])
        else:
            if(Reg_Addr == "111"):
                return int(self.flagRegr, 2)
            return self.Reg[Reg_Addr]
    
    def dump(self):
        for key in self.Reg.keys():
            print(intTOBin16bit(self.Reg[key]), end = " ")
        print(self.flagRegr)
    

RF = Reg()

class ProgramCounter:
    cur_cntr = 0
    
    def initialize(self):
        self.cur_cntr = 0
      
    def run(self):
        return self.cur_cntr
  
    def modify(self, new_cntr):
        
        self.cur_cntr = new_cntr
   
    def dump(self):
        
        print(intToBin8bit(self.cur_cntr), end = " ")

PC = ProgramCounter()
\
class Memory:
    
    mem = []                     
    X_axis = []
    Y_axis = []
    cycle = 0
    
    def initialize(self):
        for line in stdin:
            self.mem.append(line[0:16:])
        if(len(self.mem)<256):
            lineDifference = 256 - len(self.mem)
            while(lineDifference):
                self.mem.append("0000000000000000")
                lineDifference -= 1
   
    def getData(self, currentPC):
        return self.mem[currentPC]
    
    def dump(self):
        for ins in self.mem:
            print(ins)
   
    def runFromAddress(self, Mem_Addr):
        return int(self.mem[bin8bitToInt(Mem_Addr)], 2)
    

    def setValOfAddress(self, Mem_Addr, intVal):
        self.mem[bin8bitToInt(Mem_Addr)] = intTOBin16bit(intVal)
    
    def plotMemoryAccessTrace(self):
        import matplotlib.pyplot as plt
        plt.style.use('dark_background')
        plt.scatter(self.X_axis, self.Y_axis, c="blue")
        plt.ylabel("Memory Address")
        plt.xlabel("Cycle Number")
        plt.title("Memory Access Trace Graph")
        plt.show()
        plt.savefig('Memory_Access_Trace.png')

MEM = Memory()

class ExecutionEngine:

    def run(self, Inst):
        opcode = Inst[:5:]
    
        MEM.X_axis.append(MEM.cycle)
        MEM.Y_axis.append(PC.run())
        

        if(opcode == "10000"):
            reg1 = Inst[ 7:10:]      
            reg2 = Inst[10:13:]      
            reg3 = Inst[13:16:]      
            res = RF.getReg(reg2, False) + RF.getReg(reg3, False)
            if(isOverflow(res)):
                RF.setsOverflowFlag()
            else:
                RF.resetflagRegr()
            RF.setReg(reg1, res)
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "10001"):
            reg1 = Inst[ 7:10:]      
            reg2 = Inst[10:13:]      
            reg3 = Inst[13:16:]      
            res = RF.getReg(reg2,False) - RF.getReg(reg3,False)
            if (res < 0):
                RF.setsOverflowFlag()
                RF.setReg(reg1,0)
            else:
                RF.setReg(reg1,res)
                RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
       
        elif(opcode == "10010"):
            reg1 = Inst[5:8:]        
            Val = Inst[8::]        
            Val = bin8bitToInt(Val)
            RF.setReg(reg1, Val)
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "10011"):
            reg1 = Inst[10:13:]     
            reg2 = Inst[13::]       
            RF.setReg(reg1, RF.getReg(reg2, False))
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "10100"):
            reg1 = Inst[5:8:]
            Mem_Addr = Inst[8::]
            MEM.X_axis.append(MEM.cycle)                         
            MEM.Y_axis.append(bin8bitToInt(Mem_Addr))    
            ValAtMemory = MEM.runFromAddress(Mem_Addr)
            RF.setReg(reg1, ValAtMemory)
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "10101"):
            # st reg1 mem_addr
            # 5  3    8
            reg1 = Inst[5:8:]
            Mem_Addr = Inst[8::]
            MEM.X_axis.append(MEM.cycle)                         
            MEM.Y_axis.append(bin8bitToInt(Mem_Addr))     
            MEM.setValOfAddress(Mem_Addr, RF.getReg(reg1, False))
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "10110"):
            reg1 = Inst[ 7:10:]      
            reg2 = Inst[10:13:]      
            reg3 = Inst[13:16:]      
            res = RF.getReg(reg2, False) * RF.getReg(reg3, False)
            if(isOverflow(res)):
                RF.setsOverflowFlag()
            else:
                RF.resetflagRegr()
            RF.setReg(reg1, res)
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "10111"):
            reg3 = Inst[10:13:]      
            reg4 = Inst[13::]       
            remainder = RF.getReg(reg3,False) % RF.getReg(reg4,False)
            quotient = RF.getReg(reg3,False) // RF.getReg(reg3,False)
            RF.setReg("000",quotient)
            RF.setReg("111",remainder)
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
       
        elif(opcode == "11000"):
            reg1 = Inst[5:8:]
            immediateVal = bin8bitToInt(Inst[8::])
            shiftedString = '0' * immediateVal + RF.getReg(reg1, True)[:len(RF.getReg(reg1, True)) - immediateVal:]
            RF.setReg(reg1, int(shiftedString, 2))
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "11001"):
            reg1 = Inst[5:8:]
            immediateVal = bin8bitToInt(Inst[8::])
            shiftedString = RF.getReg(reg1, True)[immediateVal::] + '0' * immediateVal
            RF.setReg(reg1, int(shiftedString, 2))
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "11010"):
            reg1 = Inst[ 7:10:]     
            reg2 = Inst[10:13:]     
            reg3 = Inst[13:16:]      
            res = RF.getReg(reg2,False) ^ RF.getReg(reg3,False)
            RF.setReg(reg1,res)
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "11011"):
            reg1 = Inst[ 7:10:]    
            reg2 = Inst[10:13:]     
            reg3 = Inst[13:16:]     
            res = RF.getReg(reg2,False) | RF.getReg(reg3,False)
            RF.setReg(reg1,res)
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "11100"):
            reg1 = Inst[ 7:10:]     
            reg2 = Inst[10:13:]     
            reg3 = Inst[13:16:]     
            res = RF.getReg(reg2,False) & RF.getReg(reg3,False)
            RF.setReg(reg1,res)
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "11101"):
            reg1 = Inst[10:13:]     
            reg2 = Inst[13::]       
            inverted = ""
            for bit in reg2:
                if bit=='1':
                    inverted += '0'
                else:
                    inverted += '1'
            RF.setReg(reg1, int(inverted, 2))
            RF.resetflagRegr()
            (halt, newPC) = (False, PC.run() + 1)
        
        elif(opcode == "11110"):
            reg1 = Inst[10:13:]   
            reg2 = Inst[13::]      
            if RF.getReg(reg1, False) < RF.getReg(reg2, False):
                RF.setsLessThanFlag()
            elif RF.getReg(reg1, False) > RF.getReg(reg2, False):
                RF.setsGreaterThanFlag()
            else:
                RF.setsEqualsFlag()
            (halt, newPC) = (False, PC.run() + 1)
       
        elif(opcode == "11111"):
            Mem_Addr = Inst[8::]
            (halt, newPC) = (False, bin8bitToInt(Mem_Addr))
            RF.resetflagRegr()
        
        elif(opcode == "01100"):
            if RF.flagRegr == "0000000000000100":
                Mem_Addr = Inst[8::]
                (halt, newPC) = (False, bin8bitToInt(Mem_Addr))
            else:
                (halt, newPC) = (False, PC.run() + 1)
            RF.resetflagRegr()
        
        elif(opcode == "01101"):
            if RF.flagRegr == "0000000000000010":
                Mem_Addr = Inst[8::]
                (halt, newPC) = (False, bin8bitToInt(Mem_Addr))
            else:
                (halt, newPC) = (False, PC.run() + 1)
            RF.resetflagRegr()
        
        elif(opcode == "01111"):
            if RF.flagRegr == "0000000000000001":
                Mem_Addr = Inst[8::]
                (halt, newPC) = (False, bin8bitToInt(Mem_Addr))
            else:
                (halt, newPC) = (False, PC.run() + 1)
            RF.resetflagRegr()
        
        elif(opcode == "01010"):
            RF.resetflagRegr()
            (halt, newPC) = (True, PC.run() + 1)
       
        MEM.cycle += 1
        return (halt, newPC)
        

EE = ExecutionEngine()


MEM.initialize()
PC.initialize()
halted = False

while(not halted):
    Inst = MEM.getData(PC.run())
    halted, newPC = EE.run(Inst)
    PC.dump()
    RF.dump()
    PC.modify(newPC)

MEM.dump()
MEM.plotMemoryAccessTrace()
