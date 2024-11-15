from ignition.parser import Parser
from ignition.runtime import Runtime
from ignition.ast import AbstractSyntaxTree

class Interpreter:
    _instance = None  #Singleton

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Interpreter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            #Core components (all singletons)
            self.ast = None  #Abstract Syntax Tree
            self.parser = None  #Parser
            self.runtime = None  #Runtime environment
            self.error_string = ""  #Error messages

            self._initialized = True

    # PUBLIC METHODS

    def initialize(self):
        #Initialize AST, parser, and runtime
        self.ast = AbstractSyntaxTree()
        self.parser = Parser()
        self.runtime = Runtime()

    def forward(self, input_data):
        print("Stepping forward")

    def finish(self):
        print("Moving to EOF")

    def dump(self):
        print("Dumping state")

    # PRIVATE METHODS

