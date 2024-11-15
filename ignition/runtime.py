from ignition.ast import OperandType

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
        # Counters and pointers
        self.s_pointer = [None,None]  # Stack Pointer
        self.p_counter = 0  # Program Counter
        # Flags (State, Iteration)
        self.z_flag = [False,0]  # Zero Flag
        self.c_flag = [False,0]  # Carry Flag
        self.o_flag = [False,0]  # Overflow Flag
        self.s_flag = [False,0]  # Sign Flag
        self.error = ""

    # REGISTER OPERATIONS
    def set_register(self, reg, val, type):
        self.registers[reg] = [val,type]
    def get_register(self, reg):
        if self.registers[reg][0] is None:
            self.error = "Runtime Error: Non-initialized register access at " + reg
            return None
        else:
            return self.registers[reg]

    # MEMORY OPERATIONS
    def set_memory(self, addr, val, type):
        self.memory[addr] = [val, type]
    def get_memory(self, addr):
        if addr not in self.memory:
            self.error = "Runtime Error: Non-initialized memory access at " + addr
            return None
        else:
            return self.memory[addr]

    # STACK OPERATIONS
    def push_stack(self, val, type):
        self.stack.append([val, type])
        self.s_pointer = self.stack[-1]
    def pop_stack(self):
        if self.stack:
            ret = self.stack[-1]
            self.stack.pop()
            self.s_pointer = self.stack[-1]
            return ret
        else:
            self.error = "Runtime Error: Stack is already empty"
            return None
    def get_stack_pointer(self):
        return self.s_pointer

    # PROGRAM COUNTER OPERATIONS
    def increment_program_counter(self):
        self.p_counter += 1
    def set_program_counter(self, line):
        self.p_counter = line
    def get_program_counter(self):
        return self.p_counter

    # FLAG OPERATIONS
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
    def clear_flags(self):
        self.z_flag[0] = [False, 0]
        self.c_flag[0] = [False, 0]
        self.s_flag[0] = [False, 0]
        self.o_flag[0] = [False, 0]

    # DUMP OPERATIONS
    def dump_registers(self):
        reg_output = " ".join(f"{reg}:{val[0]}({val[1]})" for reg, val in self.registers.items())
        return reg_output
    def dump_memory(self):
        mem_output = " ".join(f"{addr}:{val[0]}({val[1]})" for addr, val in sorted(self.memory.items()))
        return mem_output
    def dump_stack(self):
        stack_output = " ".join(f"{val[0]}({val[1]})" for val in self.stack)
        return stack_output
    def dump_flags(self):
        flag_output = f"zf:{int(self.z_flag[0])} "
        flag_output += f"cf:{int(self.c_flag[0])} "
        flag_output += f"sf:{int(self.s_flag[0])} "
        flag_output += f"of:{int(self.o_flag[0])}"
        return flag_output
    def dump_program_state(self):
        prog_state = f"pc:{self.p_counter} "
        prog_state += f"sp:{self.s_pointer[0]}({self.s_pointer[1]}) "
        prog_state += f"mem:{len(self.memory)*8}B "
        prog_state += f"stack:{len(self.stack)*8}B"
        return prog_state






