from ignition.ast import AbstractSyntaxTree
from ignition.runtime import Runtime

class ExecutionEngine:
    def __init__(self, runtime):
        self._runtime = runtime

    def execute(self, instruction):
        print(f"Executing instruction {instruction}")