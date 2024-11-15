from enum import Enum, auto

#AST Enum Declerations
class NodeType(Enum):
    ROOT = auto()
    INSTRUCTION = auto()
    OPERAND = auto()

class InstructionType(Enum):
    MOVE = 0
    LOAD = 1
    STORE = 2
    CREATE = 3
    CAST = 4
    ADD = 5
    SUB = 6
    MULTIPLY = 7
    DIVIDE = 8
    OR = 9
    AND = 10
    NOT = 11
    SHIFT = 12
    COMPARE = 13
    JUMP = 14
    CALL = 15
    PUSH = 16
    POP = 17
    RETURN = 18
    STOP = 19
    INPUT = 20
    OUTPUT = 21
    PRINT = 22
    LABEL = 23
    COMMENT = 24
    NONE = 25

class OperandType(Enum):
    REGISTER = 0
    INSTRUCTION_ADDRESS = 1
    MEMORY_ADDRESS = 2
    INTEGER = 3
    FLOAT = 4
    BOOLEAN = 5
    CHARACTER = 6
    STRING = 7
    NEWLINE = 8
    TYPE_CONDITION = 9
    SHIFT_CONDITION = 10
    JUMP_CONDITION = 11
    UNKNOWN = 12
    EMPTY = 13

class NumOperands(Enum):
    NULLARY = 0
    UNARY = 1
    BINARY = 2
    TERNARY = 3
    INVALID = 4


 #AST Class
class ASTNode:
    def __init__(self, node_type: str, value: str):
        self.node_type = node_type  #Corresponds to ASTConstants::NodeType
        self.value = value  #Corresponds to m_nodeValue
        self.children = []  #Corresponds to m_children

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def __repr__(self):
        """String representation for debugging."""
        return f"{self.__class__.__name__}(type={self.node_type}, value={self.value}, children={len(self.children)})"


class RootNode(ASTNode):
    def __init__(self):
        super().__init__(node_type="ROOT", value="root")


class InstructionNode(ASTNode):
    def __init__(self, value: str, instruction_type: str, num_operands: str, line: int):
        super().__init__(node_type="INSTRUCTION", value=value)
        self.instruction_type = instruction_type  # Corresponds to m_instructionType
        self.num_operands = num_operands  # Corresponds to m_numOperands
        self.line = line  # Corresponds to m_line

    def __repr__(self):
        """String representation for debugging."""
        return (f"{self.__class__.__name__}(type={self.node_type}, value={self.value}, "
                f"instruction_type={self.instruction_type}, num_operands={self.num_operands}, line={self.line})")


class OperandNode(ASTNode):
    def __init__(self, value: str, operand_type: str, line: int, pos: int):
        super().__init__(node_type="OPERAND", value=value)
        self.operand_type = operand_type  # Corresponds to m_operandType
        self.line = line  # Corresponds to m_line
        self.pos = pos  # Corresponds to m_pos

    def __repr__(self):
        """String representation for debugging."""
        return (f"{self.__class__.__name__}(type={self.node_type}, value={self.value}, "
                f"operand_type={self.operand_type}, line={self.line}, pos={self.pos})")


class AbstractSyntaxTree:
    def __init__(self):
        self.root = None

    def set_root(self, root: RootNode):
        self.root = root

    def traverse(self, node=None, level=0):
        if node is None:
            node = self.root
        if node is not None:
            print("  " * level + repr(node))
            for child in node.get_children():
                self.traverse(child, level + 1)


#Enum Decoders
def decode_instruction_type(value: int) -> InstructionType:
    try:
        return InstructionType(value)
    except ValueError:
        raise ValueError(f"Unknown instruction type: {value}")


def decode_operand_type(value: int) -> OperandType:
    try:
        return OperandType(value)
    except ValueError:
        raise ValueError(f"Unknown operand type: {value}")
