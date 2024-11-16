from ignition.parser import Parser
from ignition.runtime import Runtime
from ignition.ast import AbstractSyntaxTree

class Interpreter:
    _instance = None  #Singleton

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Interpreter, cls).__new__(cls)
        return cls._instance

    def __init__(self, compiler_image):
        if not hasattr(self, "_initialized"):
            # Core components (all singletons)
            self.ast = None  # Abstract Syntax Tree
            self.parser = Parser()  # Parser
            self.runtime = None  # Runtime environment
            self.error_string = ""  # Error messages
            self.compiler_image = compiler_image
            self._initialized = True
            self._EOF = False
            self._prog_len = 0

    # PUBLIC METHODS
    def initialize(self, program):
        #Create a new blank runtime
        self.runtime = Runtime()
        #Call the parser to parse the given program at the local path
        self.ast = self.parser.parse_program(program, self.compiler_image)
        if self.ast is None:
            return False
        self._prog_len = len(self.ast.root.get_children())-1
        return True

    def forward(self):
        print("Stepping forward")
        self._execute_step()

    def finish(self):
        print("Moving to EOF")
        while not self._EOF:
            self._execute_step()

    def dump(self, dump_reg, dump_mem, dump_stack, dump_flags, dump_prog, is_verbose):
        def make_verbose(output, category):
            if category == "registers":
                verbose_output = []
                for reg_entry in output.split():
                    reg, value = reg_entry.split(":")
                    val_0, val_1 = value.strip("()").split("(")
                    verbose_output.append(f"Register {reg} -> Value: {val_0}, Type: {val_1}")
                return "\n".join(verbose_output)

            elif category == "memory":
                verbose_output = []
                for mem_entry in output.split():
                    addr, value = mem_entry.split(":")
                    val_0, val_1 = value.strip("()").split("(")
                    verbose_output.append(f"Memory Address {addr} -> Value: {val_0}, Type: {val_1}")
                return "\n".join(verbose_output)

            elif category == "stack":
                verbose_output = []
                for stack_entry in output.split():
                    val_0, val_1 = stack_entry.strip("()").split("(")
                    verbose_output.append(f"Stack Entry -> Value: {val_0}, Type: {val_1}")
                return "\n".join(verbose_output)

            elif category == "flags":
                verbose_output = []
                # Map of flag acronyms to full names
                flag_names = {
                    "zf": "Zero Flag",
                    "cf": "Carry Flag",
                    "sf": "Sign Flag",
                    "of": "Overflow Flag"
                }
                for flag_entry in output.split():
                    flag, value = flag_entry.split(":")
                    full_name = flag_names.get(flag, flag.upper())  # Default to uppercase acronym if not found
                    verbose_output.append(f"{full_name} -> State: {value}")
                return "\n".join(verbose_output)

            elif category == "program":
                verbose_output = []
                for prog_entry in output.split():
                    key, value = prog_entry.split(":")
                    if key == "pc":
                        verbose_output.append(f"Program Counter -> Line: {value}")
                    elif key == "sp":
                        val_0, val_1 = value.strip("()").split("(")
                        verbose_output.append(f"Stack Pointer -> Value: {val_0}, Type: {val_1}")
                    elif key == "mem_size":
                        verbose_output.append(f"Memory Size -> {value[:(len(value)-1)]} Bytes")
                    elif key == "stack_size":
                        verbose_output.append(f"Stack Size (Bytes) -> {value[:(len(value)-1)]} Bytes")
                return "\n".join(verbose_output)

        if dump_reg:
            reg_output = self.runtime.dump_registers()
            if is_verbose:
                print("=== Register Dump ===")
                print(make_verbose(reg_output, "registers"))
                print("=====================")
            else:
                print(reg_output)

        if dump_mem:
            mem_output = self.runtime.dump_memory()
            if is_verbose:
                print("=== Memory Dump ===")
                print(make_verbose(mem_output, "memory"))
                print("===================")
            else:
                print(mem_output)

        if dump_stack:
            stack_output = self.runtime.dump_stack()
            if is_verbose:
                print("=== Stack Dump ===")
                print(make_verbose(stack_output, "stack"))
                print("==================")
            else:
                print(stack_output)

        if dump_flags:
            flags_output = self.runtime.dump_flags()
            if is_verbose:
                print("=== Flags Dump ===")
                print(make_verbose(flags_output, "flags"))
                print("==================")
            else:
                print(flags_output)

        if dump_prog:
            prog_output = self.runtime.dump_program_state()
            if is_verbose:
                print("=== Program State ===")
                print(make_verbose(prog_output, "program"))
                print("=====================")
            else:
                print(prog_output)

    def terminate(self):
        #Clear the runtime and AST
        self.runtime = None
        self.ast = None
        self._EOF = False
        self._prog_len = 0

    # PRIVATE METHODS
    def _execute_step(self):
        if self._EOF:
            self.error_string += "Runtime Error: Already reached end of execution."
        else:
            curr_instruction = self.ast.root.child_at(self.runtime.get_program_counter())
            print(f"Executing instruction {curr_instruction}")
            self.runtime.increment_program_counter()

        # Set EOF Var if reached EOF
        if (self.runtime.get_program_counter() > self._prog_len):
            self._EOF = True
         #Error handling
        if len(self.error_string)>0:
            print(self.error_string)
            self.error_string = ""



