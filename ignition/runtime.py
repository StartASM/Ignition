class Runtime:
    def __init__(self):
        # Registers (Val, Type)
        self.registers = {
            "r1": [None, None],
            "r2": [None, None],
            "r3": [None, None],
            "r4": [None, None],
            "r5": [None, None],
            "r6": [None, None],
            "r7": [None, None],
            "r8": [None, None],
            "r9": [None, None],
        }
        # Memory
        self.memory = {}
        # Stack
        self.stack = []
        # Counters (with state and iterations)
        self.p_counter = 0  # Program Counter
        self.s_pointer = None # Stack Pointer
        self.z_flag = [False,0]  # Zero Flag
        self.c_flag = [False,0]  # Carry Flag
        self.o_flag = [False,0]  # Overflow Flag
        self.s_flag = [False,0]  # Sign Flag
        self.error = ""

    #REGISTER OPERATIONS
    def set_register(self, reg, val, type):
        self.registers[reg] = [val,type]
    def get_register(self, reg):
        if self.registers[reg][0] is None:
            self.error = "Runtime Error: Non-initialized register access at " + reg
            return None
        else:
            return self.registers[reg]

    #MEMORY OPERATIONS
    def set_memory(self, addr, val, type):
        self.memory[addr] = [val, type]
    def get_memory(self, addr):
        if addr not in self.memory:
            self.error = "Runtime Error: Non-initialized memory access at " + addr
            return None
        else:
            return self.memory[addr]

    #FLAG OPERATIONS
    def set_flag(self, flag):
        if flag == 'z':
            self.z_flag = [True, 0]
        elif flag == 'c':
            self.c_flag = [True, 0]
        elif flag =='o':
            self.o_flag = [True, 0]
        elif flag == 's':
            self.s_flag = [True, 0]
        else:
            self.error = "Runtime Error: Undefined flag"
    def get_flag(self, flag):
        if flag == 'z':
            return self.z_flag[0]
        elif flag == 'c':
            return self.c_flag[0]
        elif flag == 'o':
            return self.o_flag[0]
        elif flag == 's':
            return self.s_flag[0]
        else:
            self.error = "Runtime Error: Undefined flag"

    def refresh_flags(self):
        if not self.z_flag[0]:
            if self.z_flag[1] > 1:
                self.z_flag = [False, 0]
            else:
                self.z_flag[1] += 1
        if not self.c_flag[0]:
            if self.c_flag[1] > 1:
                self.c_flag = [False, 0]
            else:
                self.c_flag[1] += 1
        if not self.o_flag[0]:
            if self.o_flag[1] > 1:
                self.o_flag = [False, 0]
            else:
                self.o_flag[1] += 1
        if not self.s_flag[0]:
            if self.s_flag[1] > 1:
                self.s_flag = [False, 0]
            else:
                self.s_flag[1] += 1




