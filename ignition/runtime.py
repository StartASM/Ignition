from ignition.ast import OperandType
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647

class Runtime:
    def __init__(self):
        # Registers (Val, Type)
        self.registers = [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]
        # Memory
        self.memory = {}
        # Counters and pointers
        self.s_pointer = INT32_MAX+1  # Stack Pointer
        self.p_counter = 0  # Program Counter
        # Flags (State, Iteration)
        self.z_flag = False  # Zero Flag
        self.o_flag = False  # Overflow Flag
        self.s_flag = False  # Sign Flag

    # REGISTER OPERATIONS
    def set_register(self, reg, val, type):
        self.registers[int(reg[1])] = [val,type]
    def get_register(self, reg):
        if reg == 'sp':
            return [self.s_pointer, OperandType.MEMORY_ADDRESS]
        elif self.registers[int(reg[1])][0] is None:
            return None
        else:
            return self.registers[int(reg[1])]

    # MEMORY OPERATIONS
    def set_memory(self, addr, val, type):
        self.memory[addr] = [val, type]
    def get_memory(self, addr):
        if addr not in self.memory.keys():
            return None
        else:
            return self.memory[addr]
    def addr_initialized(self, addr):
        return addr in self.memory.keys()

    # STACK OPERATIONS
    def push_stack(self, val, type):
        self.memory[self.s_pointer-1] = [val, type]
        self.s_pointer -=1
    def pop_stack(self):
        self.s_pointer += 1
        return self.memory[self.s_pointer-1]
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
    def set_flag(self, flag, state):
        match flag:
            case 'z':
                self.z_flag = state
            case 'o':
                self.o_flag = state
            case 's':
                self.s_flag = state

    def get_flag(self, flag):
        match flag:
            case 'z':
                return self.z_flag
            case 'o':
                return self.o_flag
            case 's':
                return self.s_flag

    # DUMP OPERATIONS
    def dump_registers(self):
        reg_output = " ".join(f"r{i}:{val[0]}({val[1]})" if val[0] is not None else f"r{i}:None(None)" for i, val in enumerate(self.registers))
        return reg_output
    def dump_memory(self):
        mem_output = " ".join(f"{addr}:{val[0]}({val[1]})"for addr, val in sorted(self.memory.items())if addr < self.s_pointer)
        return mem_output
    def dump_stack(self):
        stack_output = " ".join(f"{val[0]}({val[1]})"for addr, val in sorted(self.memory.items(), key=lambda item: item[0], reverse=True)if addr >= self.s_pointer)
        return stack_output
    def dump_flags(self):
        flag_output = f"zf:{int(self.z_flag)} "
        flag_output += f"sf:{int(self.s_flag)} "
        flag_output += f"of:{int(self.o_flag)}"
        return flag_output
    def dump_program_state(self):
        prog_state = f"pc:{self.p_counter} "
        if self.s_pointer > INT32_MAX:
            prog_state += f"sp:None "
        else:
            prog_state += f"sp:m<{self.s_pointer}> "
        prog_state += f"mem:{len(self.memory)*4}B "
        prog_state += f"stack:{(INT32_MAX-self.s_pointer+1)*4}B"
        return prog_state






