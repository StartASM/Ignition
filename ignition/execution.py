from jinja2.nodes import Operand

from ignition.ast import InstructionType, OperandType
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647

class ExecutionEngine:
    def __init__(self, runtime, prog_len):
        self.runtime = runtime
        self._prog_len = prog_len+1
        self.instruction_handlers = {
            InstructionType.MOVE: self._execute_move,
            InstructionType.LOAD: self._execute_load,
            InstructionType.STORE: self._execute_store,
            InstructionType.CREATE: self._execute_create,
            InstructionType.CAST: self._execute_cast,
            InstructionType.ADD: self._execute_add,
            InstructionType.SUB: self._execute_sub,
            InstructionType.MULTIPLY: self._execute_multiply,
            InstructionType.DIVIDE: self._execute_divide,
            InstructionType.OR: self._execute_or,
            InstructionType.AND: self._execute_and,
            InstructionType.NOT: self._execute_not,
            InstructionType.SHIFT: self._execute_shift,
            InstructionType.COMPARE: self._execute_compare,
            InstructionType.JUMP: self._execute_jump,
            InstructionType.CALL: self._execute_call,
            InstructionType.PUSH: self._execute_push,
            InstructionType.POP: self._execute_pop,
            InstructionType.RETURN: self._execute_return,
            InstructionType.STOP: self._execute_stop,
            InstructionType.INPUT: self._execute_input,
            InstructionType.OUTPUT: self._execute_output,
            InstructionType.PRINT: self._execute_print,
            InstructionType.LABEL: self._execute_pass,
            InstructionType.COMMENT: self._execute_pass
        }

    def execute(self, instruction):
        instruction_type = instruction.instruction_type
        operands = instruction.get_children()
        handler = self.instruction_handlers.get(instruction_type)
        handler(operands)

    # Define the execute functions
    def _execute_move(self, operands):
        source_reg = operands[0].value
        target_reg = operands[1].value
        source_val_type = self.runtime.get_register(source_reg)
        if source_val_type is None:
            print(f"Runtime Error: Source register {source_reg} is not initialized.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            self.runtime.set_register(target_reg, source_val_type[0], source_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_load(self, operands):
        source = operands[0].value
        target_reg = operands[1].value
        if source[0] == 'r':
            source_val_type = self.runtime.get_register(source)
            if source_val_type[1] != OperandType.MEMORY_ADDRESS:
                print(f"Runtime Error: Source register {target_reg[0]} does not contain a memory address.")
                self.runtime.set_program_counter(self._prog_len)
            elif not self.runtime.addr_initialized(source_val_type[0]):
                print(f"Runtime Error: Memory address {source_val_type[0]} is not initialized.")
                self.runtime.set_program_counter(self._prog_len)
            else:
                mem_val_type = self.runtime.get_memory(source_val_type[0])
                self.runtime.set_register(target_reg, mem_val_type[0], mem_val_type[1])
                self.runtime.increment_program_counter()
        elif source[0] == 'm':
            source_mem = source[2:len(source) - 1]
            print(source_mem)
            if not self.runtime.addr_initialized(source_mem):
                print(f"Runtime Error: Memory address {source_mem} is not initialized.")
                self.runtime.set_program_counter(self._prog_len)
            else:
                mem_val_type = self.runtime.get_memory(source_mem)
                self.runtime.set_register(target_reg, mem_val_type[0], mem_val_type[1])
                self.runtime.increment_program_counter()

    def _execute_store(self, operands):
        source_reg = operands[0].value
        target = operands[1].value
        source_val_type = self.runtime.get_register(source_reg)
        if target[0] == 'r':
            target_val_type = self.runtime.get_register(target)
            if source_val_type is None:
                print(f"Runtime Error: Source register {source_reg} is uninitialized.")
                self.runtime.set_program_counter(self._prog_len)
            elif target_val_type[1] != OperandType.MEMORY_ADDRESS:
                print(f"Runtime Error: Target register {target} does not contain a memory address.")
                self.runtime.set_program_counter(self._prog_len)
            else:
                self.runtime.set_memory(target_val_type[0], source_val_type[0], source_val_type[1])
                self.runtime.increment_program_counter()
        elif target[0] == 'm':
            target_mem = target[2:len(target) - 1]
            if source_val_type is None:
                print(f"Runtime Error: Source register {source_reg} is uninitialized.")
                self.runtime.set_program_counter(self._prog_len)
            else:
                self.runtime.set_memory(target_mem, source_val_type[0], source_val_type[1])
                self.runtime.increment_program_counter()


    def _execute_create(self, operands):
        val_type = self._convert_type_enum(operands[0].value)
        val = self._convert_value(operands[1])
        reg = operands[2].value
        self.runtime.set_register(reg, val, val_type)
        self.runtime.increment_program_counter()

    def _execute_cast(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_add(self, operands):
        permitted_types = [OperandType.INTEGER, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN, OperandType.CHARACTER]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            print(f"Runtime Error: Source reg {source_reg_1} and/or source reg {source_reg_2} is not initialized.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} for addition.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] + s2_val_type[0]
            self.runtime.set_register(dest_reg, self._handle_overflow(result, s1_val_type[1]), s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_sub(self, operands):
        permitted_types = [OperandType.INTEGER, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN, OperandType.CHARACTER]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            print(f"Runtime Error: Source reg {source_reg_1} and/or source reg {source_reg_2} is not initialized.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for subtraction.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] - s2_val_type[0]
            self.runtime.set_register(dest_reg, self._handle_overflow(result, s1_val_type[1]), s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_multiply(self, operands):
        permitted_types = [OperandType.INTEGER, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN, OperandType.CHARACTER]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            print(f"Runtime Error: Source reg {source_reg_1} and/or source reg {source_reg_2} is not initialized.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for multiplication.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] * s2_val_type[0]
            self.runtime.set_register(dest_reg, self._handle_overflow(result, s1_val_type[1]), s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_divide(self, operands):
        permitted_types = [OperandType.INTEGER]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            print(f"Runtime Error: Source reg {source_reg_1} and/or source reg {source_reg_2} is not initialized.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for division.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] // s2_val_type[0]
            self.runtime.set_register(dest_reg, self._handle_overflow(result, s1_val_type[1]), s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_or(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_and(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_not(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_shift(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_compare(self, operands):
        permitted_types = [OperandType.INTEGER, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN, OperandType.CHARACTER]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            print(f"Runtime Error: Source reg {source_reg_1} and/or source reg {source_reg_2} is not initialized.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for subtraction.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] - s2_val_type[0]
            self._handle_overflow(result, s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_jump(self, operands):
        condition = operands[0].value
        destination = int(operands[1].value[2:len(operands[1].value) - 1])
        s_flag = self.runtime.get_flag('s')
        o_flag = self.runtime.get_flag('o')
        z_flag = self.runtime.get_flag('z')
        if condition == "greater" and not z_flag and (s_flag == o_flag):
            self.runtime.set_program_counter(destination)
        elif condition == "less" and (s_flag != o_flag):
            self.runtime.set_program_counter(destination)
        elif (condition == "equal" or condition == "zero") and z_flag:
            self.runtime.set_program_counter(destination)
        elif (condition == "unequal" or condition == "nonzero") and not z_flag:
            self.runtime.set_program_counter(destination)
        elif condition == "negative" and s_flag:
            self.runtime.set_program_counter(destination)
        elif condition == "positive" and not s_flag and not z_flag:
            self.runtime.set_program_counter(destination)
        elif condition == "unconditional":
            self.runtime.set_program_counter(destination)
        else:
            self.runtime.increment_program_counter()

    def _execute_call(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_push(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_pop(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_return(self, operands):
        self.runtime.increment_program_counter()
        pass

    def _execute_stop(self, operands):
        self.runtime.set_program_counter(self._prog_len)

    def _execute_input(self, operands):
        input_type = self._convert_type_enum(operands[0].value)
        input_dest = operands[1].value
        user_input = input("stdin: ")
        if input_type == OperandType.INTEGER:
            try:
                user_input = int(user_input)
                self.runtime.set_register(input_dest, user_input, input_type)
                self.runtime.increment_program_counter()
            except ValueError:
                print(f"Input Error: Invalid input {user_input} for type int.")
        elif input_type == OperandType.CHARACTER:
            if len(user_input) > 1:
                print(f"Input Error: Excess input {user_input} for type char.")
            elif ord(user_input) > 127:
                print(f"Input Error: Input {user_input} out of extended ASCII range.")
            else:
                self.runtime.set_register(input_dest, ord(user_input), input_type)
                self.runtime.increment_program_counter()
        elif input_type == OperandType.BOOLEAN:
            valid_trues = ['true', '1', 'True', 't', 'TRUE', 'T']
            valid_falses = ['false', '0', 'False', 'f', 'FALSE', 'F']
            if user_input not in valid_trues or user_input not in valid_falses:
                print(f"Input Error: Invalid input {user_input} for type bool.")
            elif user_input in valid_trues:
                self.runtime.set_register(input_dest, True, input_type)
                self.runtime.increment_program_counter()
            elif user_input in valid_falses:
                self.runtime.set_register(input_dest, False, input_type)
                self.runtime.increment_program_counter()

    def _execute_output(self, operands):
        source_reg = operands[0].value
        source_val_type = self.runtime.get_register(source_reg)
        if source_val_type is None:
            print(f"Runtime Error: {source_reg} is not defined.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            converted_output = self._convert_output(source_val_type)
            print(f"stdout: {converted_output}")
            self.runtime.increment_program_counter()

    def _execute_print(self, operands):
        if operands[0].value == "newline":
            print()
        else:
            print(operands[0].value[1:(len(operands[0].value)-1)], end="")
        self.runtime.increment_program_counter()

    def _execute_pass(self, operands):
        self.runtime.increment_program_counter()


    # HELPER FUNCTIONS
    def _handle_overflow(self, result, type):
        if type == OperandType.CHARACTER:
            wrapped_result = result % 256
        else:
            wrapped_result = (result + 2 ** 31) % 2 ** 32 - 2 ** 31
            if result < INT32_MIN or result > INT32_MAX:
                self.runtime.set_flag('o', True)
            else:
                self.runtime.set_flag('o', False)

        if wrapped_result == 0:
            self.runtime.set_flag('z', True)
            self.runtime.set_flag('s', False)
        elif wrapped_result < 0:
            self.runtime.set_flag('z', False)
            self.runtime.set_flag('s', True)
        else:
            self.runtime.set_flag('z', False)
            self.runtime.set_flag('s', False)
        return wrapped_result


    def _convert_value(self, operand):
        op_type = operand.operand_type
        if op_type == OperandType.MEMORY_ADDRESS or op_type == OperandType.INSTRUCTION_ADDRESS:
            return int(operand.value[2:len(operand.value) - 1])
        elif op_type == OperandType.INTEGER:
            return int(operand.value)
        elif op_type == OperandType.BOOLEAN:
            if operand.value == 'true':
                return True
            elif operand.value == 'false':
                return False
        elif op_type == OperandType.CHARACTER:
            return ord(operand.value)
        elif op_type == OperandType.STRING:
            return str(operand.value)
        else:
            return None

    def _convert_output(self, operand):
        op_type = operand[1]
        op_value = operand[0]
        if op_type == OperandType.MEMORY_ADDRESS:
            return f"m<{op_value}>"
        elif op_type == OperandType.INSTRUCTION_ADDRESS:
            return f"i[{op_value}]"
        elif op_type == OperandType.INTEGER:
            return op_value
        elif op_type == OperandType.BOOLEAN:
            if op_value:
                return 'true'
            else:
                return 'false'
        elif op_type == OperandType.CHARACTER:
            return chr(op_value)
        elif op_type == OperandType.STRING:
            return str(op_value)
        else:
            return None

    def _convert_type_enum(self, str_type):
        if str_type == "integer":
            return OperandType.INTEGER
        elif str_type == "boolean":
            return OperandType.BOOLEAN
        elif str_type == "character":
            return OperandType.CHARACTER
        elif str_type == "memory":
            return OperandType.MEMORY_ADDRESS

