import subprocess
import json
from ignition.ast import AbstractSyntaxTree, RootNode, InstructionNode, OperandNode, InstructionType, OperandType
from ignition.ast import decode_operand_type, decode_instruction_type, NumOperands


class Parser:
    def __init__(self):
        self.json_output = None

    def parse_program(self, program_path, compiler_image) -> AbstractSyntaxTree:
        self._call_compiler(program_path, compiler_image)
        ast = AbstractSyntaxTree()
        if self.json_output is None:
            return None
        root_node = self._build_ast(self.json_output)
        ast.set_root(root_node)
        return ast

    def _call_compiler(self, program_path, compiler_image):
        compiler_command = ["docker", "run", "--rm", compiler_image, "ast", program_path]
        try:
            result = subprocess.run(
                compiler_command,
                text=True,
                capture_output=True,
                check=False
            )
            if result.returncode != 0:
                print(f"Compiler error: {result.stderr.strip()}")
                self.json_output = None
            else:
                self.json_output = json.loads(result.stdout)
        except Exception as e:
            print(f"Failed to call compiler image: {str(e)}")
            self.json_output = None

    def _build_ast(self, json_node) -> RootNode:
        node_type = json_node.get("type")
        value = json_node.get("value", "")
        children = json_node.get("children", [])
        ast_node = None
        if node_type == "ROOT":
            ast_node = RootNode()
        elif node_type == "INSTRUCTION":
            instruction_type = decode_instruction_type(json_node.get("instruction_type"))
            num_operands = NumOperands(json_node.get("num_operands"))
            line = json_node.get("line", -1)
            ast_node = InstructionNode(
                value=value,
                instruction_type=instruction_type,
                num_operands=num_operands,
                line=line,
            )
        elif node_type == "OPERAND":
            operand_type = decode_operand_type(json_node.get("operand_type"))
            line = json_node.get("line", -1)
            pos = json_node.get("position", -1)
            ast_node = OperandNode(
                value=value,
                operand_type=operand_type,
                line=line,
                pos=pos,
            )
        else:
            raise ValueError(f"Unknown node type: {node_type}")

        # Recursively process and add children
        for child_json in children:
            child_node = self._build_ast(child_json)
            ast_node.add_child(child_node)

        return ast_node
