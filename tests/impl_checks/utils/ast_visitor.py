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


def get_class_methods(tree, class_name):
    methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for node_ in ast.walk(node):
                if isinstance(node_, ast.FunctionDef):
                    methods.append(node_.name)
            else:
                return methods