from ignition.ast import InstructionType, OperandType

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
        print("Executing move")
        source_reg = operands[0].value
        target_reg = operands[1].value
        source_val_type = self.runtime.get_register(source_reg)
        if source_val_type is None:
            self.runtime.set_program_counter(self._prog_len)
        else:
            self.runtime.set_register(target_reg, source_val_type[0], source_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_load(self, operands):
        print("Executing load")
        pass

    def _execute_store(self, operands):
        print("Executing store")
        source_reg = operands[0].value
        target_mem = operands[1].value
        source_val_type = self.runtime.get_register(source_reg)
        if source_val_type is None:
            self.runtime.set_program_counter(self._prog_len)
        else:
            self.runtime.set_memory(target_mem, source_val_type[0], source_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_create(self, operands):
        print("Executing create")
        val_type = self._convert_type_enum(operands[0].value)
        val = self._convert_value(operands[1])
        reg = operands[2].value
        self.runtime.set_register(reg, val, val_type)
        self.runtime.increment_program_counter()

    def _execute_cast(self, operands):
        print("Executing cast")
        pass

    def _execute_add(self, operands):
        print("Executing add")
        permitted_types = [OperandType.INTEGER, OperandType.FLOAT, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} for addition.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] + s2_val_type[0]
            self.runtime.set_register(dest_reg, result, s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_sub(self, operands):
        print("Executing sub")
        permitted_types = [OperandType.INTEGER, OperandType.FLOAT, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(
                f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(
                f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for subtraction.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] - s2_val_type[0]
            self.runtime.set_register(dest_reg, result, s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_multiply(self, operands):
        print("Executing multiply")
        permitted_types = [OperandType.INTEGER, OperandType.FLOAT, OperandType.MEMORY_ADDRESS, OperandType.BOOLEAN]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(
                f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(
                f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for multiplication.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] * s2_val_type[0]
            self.runtime.set_register(dest_reg, result, s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_divide(self, operands):
        print("Executing divide")
        permitted_types = [OperandType.INTEGER, OperandType.FLOAT]
        source_reg_1 = operands[0].value
        source_reg_2 = operands[1].value
        dest_reg = operands[2].value
        s1_val_type = self.runtime.get_register(source_reg_1)
        s2_val_type = self.runtime.get_register(source_reg_2)
        if s1_val_type is None or s2_val_type is None:
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] != s2_val_type[1]:
            print(
                f"Runtime Error: {source_reg_1} and {source_reg_2} are of different types {s1_val_type[1]}, {s2_val_type[1]}.")
            self.runtime.set_program_counter(self._prog_len)
        elif s1_val_type[1] not in permitted_types:
            print(
                f"Runtime Error: {source_reg_1} and {source_reg_2} are of incompatible types {s1_val_type[1]}, {s2_val_type[1]} are of different types for division.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            result = s1_val_type[0] // s2_val_type[0]
            self.runtime.set_register(dest_reg, result, s1_val_type[1])
            self.runtime.increment_program_counter()

    def _execute_or(self, operands):
        print("Executing or")
        pass

    def _execute_and(self, operands):
        print("Executing and")
        pass

    def _execute_not(self, operands):
        print("Executing not")
        pass

    def _execute_shift(self, operands):
        print("Executing shift")
        pass

    def _execute_compare(self, operands):
        print("Executing compare")
        pass

    def _execute_jump(self, operands):
        print("Executing jump")
        pass

    def _execute_call(self, operands):
        print("Executing call")
        pass

    def _execute_push(self, operands):
        print("Executing push")
        pass

    def _execute_pop(self, operands):
        print("Executing pop")
        pass

    def _execute_return(self, operands):
        print("Executing return")
        pass

    def _execute_stop(self, operands):
        print("Executing stop")
        self.runtime.set_program_counter(self._prog_len)

    def _execute_input(self, operands):
        print("Executing input")
        pass

    def _execute_output(self, operands):
        print("Executing output")
        source_reg = operands[0].value
        source_val_type = self.runtime.get_register(source_reg)
        if source_val_type is None:
            print(f"Runtime Error: {source_reg} is not defined.")
            self.runtime.set_program_counter(self._prog_len)
        else:
            print(source_val_type[0])
            self.runtime.increment_program_counter()

    def _execute_print(self, operands):
        print("Executing print")
        if operands[0].value == "newline":
            print()
        else:
            print(operands[0].value[1:(len(operands[0].value)-1)], end="")
        self.runtime.increment_program_counter()

    def _execute_pass(self, operands):
        print("Executing pass")
        self.runtime.increment_program_counter()


    # HELPER FUNCTIONS
    def _convert_value(self, operand):
        op_type = operand.operand_type
        if op_type == OperandType.MEMORY_ADDRESS or op_type == OperandType.INSTRUCTION_ADDRESS:
            return int(operand.value[2:len(operand.value) - 1])
        elif op_type == OperandType.INTEGER:
            return int(operand.value)
        elif op_type == OperandType.FLOAT:
            return float(operand.value)
        elif op_type == OperandType.BOOLEAN:
            if operand.value == 'true':
                return True
            elif operand.value == 'false':
                return False
        elif op_type == OperandType.CHARACTER or op_type == OperandType.STRING:
            return str(operand.value)
        else:
            return None

    def _convert_type_enum(self, str_type):
        if str_type == "integer":
            return OperandType.INTEGER
        elif str_type == "float":
            return OperandType.FLOAT
        elif str_type == "boolean":
            return OperandType.BOOLEAN
        elif str_type == "character":
            return OperandType.CHARACTER
        elif str_type == "memory":
            return OperandType.MEMORY_ADDRESS

