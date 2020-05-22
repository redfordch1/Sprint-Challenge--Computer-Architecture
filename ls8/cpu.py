"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flag = 0
        self.reg[7] = 0xF4
        self.branchtable = {
            HLT: self.handle_HLT,
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            ADD: self.handle_ADD,
            MUL: self.handle_MUL,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            CALL: self.handle_CALL,
            RET: self.handle_RET,
            CMP: self.handle_CMP,
            JMP: self.handle_JMP,
            JEQ: self.handle_JEQ,
            JNE: self.handle_JNE,
        }

    def handle_HLT(self, register_a, register_b):
        self.running = False

    def handle_LDI(self, register, immediate):
        self.reg[register] = immediate

    def handle_PRN(self, register_a, register_b):
        value = self.reg[register_a]
        print(value)
    
    def handle_ADD(self, register_a, register_b):
        self.alu(ADD, register_a, register_b)
    
    def handle_MUL(self, register_a, register_b):
        self.alu(MUL, register_a, register_b)
    
    def handle_PUSH(self, register_a, register_b):
        value = self.reg[register_a]
        self.reg[7] -= 1
        sp = self.reg[7]
        self.ram_write(value, sp)
    
    def handle_POP(self, register_a, register_b):
        sp = self.reg[7]
        value = self.ram_read(sp)
        self.reg[register_a] = value
        self.reg[7] += 1

    def handle_CALL(self, register_a, register_b):
        self.reg[7] -= 1
        sp = self.reg[7]
        return_location = self.pc + 2
        self.ram_write(return_location, sp)

        register = self.ram_read(self.pc + 1)
        self.pc = self.reg[register]

    def handle_RET(self, register_a, register_b):
        sp = self.reg[7]
        return_location = self.ram_read(sp)
        self.pc = return_location

    def handle_CMP(self, register_a, register_b):
        if self.reg[register_a] == self.reg[register_b]:
            self.flag = 0b1
        elif self.reg[register_a] > self.reg[register_b]:
            self.flag = 0b10
        else:
            self.flag = 0b100

    def handle_JMP(self, register_a, register_b):
        self.pc = self.reg[register_a]

    def handle_JEQ(self, register_a, register_b):
        if self.flag & 0b1 == 1:
            self.pc = self.reg[register_a]
        else:
            self.pc += 2

    def handle_JNE(self, register_a, register_b):
        if self.flag & 0b1 == 0:
            self.pc = self.reg[register_a]
        else:
            self.pc += 2

    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR


    def load(self):
        """Load a program into memory."""
        try:
            with open(sys.argv[1]) as file:
                address = 0
                for line in file:
                    split_line = line.split("#")
                    command = split_line[0]
                    command = command.strip(" \n")
                    if len(command) > 0:
                        self.ram_write(int(command, 2), address)
                        address += 1
        except FileNotFoundError:
            print("Sorry file does not exist")


    def alu(self, op, register_a, register_b):
        """ALU operations."""
        if op == ADD:
            result = self.reg[register_a] + self.reg[register_b]
        elif op == MUL: 
            result = self.reg[register_a] * self.reg[register_b]
        else:
            raise Exception("Unsupported ALU operation")

        # mask = "11111111"
        # self.reg[register_a] = f"{result & int(mask, 2)}"

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            num_operands = IR >> 6
            pc_mask = "00010000"
            pc_set = (IR & int(pc_mask, 2)) >> 4

            if IR in self.branchtable:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.branchtable[IR](operand_a, operand_b)
                if pc_set != 1:
                    self.pc += num_operands + 1








# def counter(num):
#     print(bin(num))
#     #          1     2       4         8         16      32       64      128
#     langs = ["C#", "C++", "Java", "JavaScript", "PHP", "Python", "Ruby", "Swift"]
#     result = []
#     for i in range(len(langs)):
#             print(bin(i))
#             if num & (1 << i):
#                 result.append(langs[i])
        
#     print(result)
            
            
# counter(25)