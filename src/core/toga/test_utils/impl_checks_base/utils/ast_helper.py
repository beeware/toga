import ast


class DefinitionExtractor:
    def __init__(self, file):
        self._classes = {}
        # load the file and parse it with the ast module.
        with open(file, 'r') as f:
            lines = f.read()
        self.tree = ast.parse(lines)
        self.extract_classes()

    @property
    def class_names(self):
        return self._classes.keys()

    def extract_classes(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self._classes[node.name] = node

    def methods_of_class(self, class_name):
        class_node = self._classes[class_name]
        methods = []
        for node in ast.walk(class_node):
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)
        else:
            return methods
