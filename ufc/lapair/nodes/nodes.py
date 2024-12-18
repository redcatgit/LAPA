from dataclasses import dataclass
from typing import List, Optional
from ufc.iast.nodes import ClassNode, MethodNode, ReturnNode, BinaryOperationNode, VariableNode, FunctionNode

@dataclass
class IRBinaryExpression:
    operator: str
    left: str
    right: str

    def __post_init__(self):
        valid_operators = {"+", "-", "*", "/", "&&", "||", "==", "!=", "<", ">", "<=", ">="}
        if not self.operator or not self.left or not self.right:
            raise ValueError("Binary expression must have operator, left and right operands")
        if self.operator not in valid_operators:
            raise ValueError(f"Invalid operator: {self.operator}")

    @classmethod
    def from_iast(cls, node):
        if not hasattr(node, 'operator') or not hasattr(node, 'left') or not hasattr(node, 'right'):
            raise ValueError("Invalid binary expression node")
        return cls(
            operator=node.operator,
            left=node.left.name if hasattr(node.left, 'name') else str(node.left),
            right=node.right.name if hasattr(node.right, 'name') else str(node.right)
        )

@dataclass
class IRReturn:
    expression: Optional[IRBinaryExpression] = None

    @classmethod
    def from_iast(cls, node):
        if not node.expression:
            return cls(expression=None)
        return cls(expression=IRBinaryExpression.from_iast(node.expression))

@dataclass
class IRFunction:
    name: str
    parameters: List[str]
    body: List[IRReturn]
    return_type: str

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Function name must be a non-empty string")
        if self.name[0].isdigit():
            raise ValueError("Function name cannot start with a digit")

    @classmethod
    def from_iast(cls, node):
        # Handle direct function nodes from C code
        if isinstance(node, FunctionNode):
            body = []
            parameters = []
            if hasattr(node, 'parameters'):
                parameters = [p.name for p in node.parameters]
            if node.body and node.body.statements:
                for stmt in node.body.statements:
                    if isinstance(stmt, ReturnNode):
                        body.append(IRReturn.from_iast(stmt))
                    # Add handling for other statement types as needed
            return cls(
                name=node.name,
                parameters=parameters,
                return_type=node.return_type if hasattr(node, 'return_type') else 'void',
                body=body
            )

        # Handle method nodes from classes
        if not isinstance(node, MethodNode):
            raise ValueError(f"Expected MethodNode, got {type(node)}")

        body = []
        parameters = []
        if hasattr(node, 'parameters'):
            parameters = [p.name for p in node.parameters]
        if node.body and node.body.statements:
            for stmt in node.body.statements:
                if isinstance(stmt, ReturnNode):
                    body.append(IRReturn.from_iast(stmt))
                # Add handling for other statement types as needed
        return cls(
            name=node.name,
            parameters=parameters,
            return_type=node.return_type if hasattr(node, 'return_type') else 'void',
            body=body
        )

@dataclass
class IRClass:
    name: str
    methods: List[IRFunction]

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Class name must be a non-empty string")
        if self.name[0].isdigit():
            raise ValueError("Class name cannot start with a digit")

    @classmethod
    def from_iast(cls, nodes):
        # Handle list of nodes
        if isinstance(nodes, list):
            print(f"DEBUG: Processing list of nodes, length: {len(nodes)}")
            if not nodes:
                raise ValueError("Empty list of nodes provided")

            # If all nodes are FunctionNodes, wrap them in a GlobalScope class
            if all(isinstance(node, FunctionNode) for node in nodes):
                print(f"DEBUG: Converting all function nodes to GlobalScope")
                functions = [IRFunction.from_iast(node) for node in nodes]
                return cls(name="GlobalScope", methods=functions)

            # If mixed or other types, use first node (existing behavior)
            node = nodes[0]
        else:
            node = nodes

        # Handle direct function nodes from C code by wrapping in GlobalScope class
        if isinstance(node, FunctionNode):
            print(f"DEBUG: Converting function node: {node.name}")
            function = IRFunction.from_iast(node)
            return cls(name="GlobalScope", methods=[function])

        if not isinstance(node, ClassNode):
            raise ValueError(f"Expected ClassNode or FunctionNode, got {type(node)}")

        methods = [IRFunction.from_iast(method) for method in node.methods]
        return cls(name=node.name, methods=methods)
