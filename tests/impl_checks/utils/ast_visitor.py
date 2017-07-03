import ast


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.function_names = []
        self.class_names = []

    def visit_FunctionDef(self, node):
        self.function_names.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.class_names.append(node.name)
        self.generic_visit(node)
