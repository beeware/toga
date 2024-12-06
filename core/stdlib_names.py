#!/usr/bin/env python3
import ast
import builtins
import sys
from argparse import ArgumentParser
from collections import defaultdict
from importlib import import_module
from pprint import pformat
from textwrap import dedent

# Structure: mod_name: {attr_name, ...}
# Built-in names are stored with a mod_name of "builtins".
imports = defaultdict(set)


def main():
    args = parse_args()
    for filename in args.inputs:
        try:
            with open(filename) as f:
                root = ast.parse(f.read(), filename)
                Visitor().visit(root)
        except Exception:
            print(f"Failed to process {filename}", file=sys.stderr)
            raise

    if args.list:
        print(format_list())
    elif args.test:
        print(format_test())


def parse_args():
    parser = ArgumentParser(
        description="Analyse some Python code to determine the names it "
        "uses from the standard library."
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--list", action="store_true", help="Output a list of names to stdout."
    )
    mode.add_argument(
        "--test",
        action="store_true",
        help="Output a test script to stdout. This can be run on a different version "
        "of Python to get an idea of how difficult the code would be to port.",
    )

    parser.add_argument(
        "inputs", metavar="filename.py", nargs="+", help="Python source file"
    )
    return parser.parse_args()


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.modules = {}

    def add_module(self, mod_name, alias):
        imports[mod_name]  # Create if it doesn't already exist.
        if alias.asname:
            self.modules[alias.asname] = mod_name
        else:
            package = mod_name.split(".")[0]
            self.modules[package] = package

    def visit_Import(self, node):
        for alias in node.names:
            if is_stdlib_module(alias.name):
                self.add_module(alias.name, alias)

    def visit_ImportFrom(self, node):
        if node.level == 0 and is_stdlib_module(node.module):
            for alias in node.names:
                full_name = f"{node.module}.{alias.name}"
                if is_stdlib_module(full_name):
                    self.add_module(full_name, alias)
                else:
                    imports[node.module].add(alias.name)

    def visit_Name(self, node):
        if (
            isinstance(node.ctx, ast.Load)
            and hasattr(builtins, node.id)
            and not node.id.startswith("__")
        ):
            imports["builtins"].add(node.id)
        elif mod_name := self.modules.get(node.id):
            return mod_name
        else:
            return None

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        if value:
            value_attr = f"{value}.{node.attr}"
            if is_stdlib_module(value_attr):
                imports[value_attr]  # Create if it doesn't already exist.
                return value_attr
            else:
                imports[value].add(node.attr)

        return None


def is_stdlib_module(mod_name):
    if mod_name.split(".")[0] in sys.stdlib_module_names:
        try:
            import_module(mod_name)
            return True
        except ImportError:
            pass

    return False


def format_list():
    # Transform the defaultdict into a sorted list, as dicts may not retain
    # their sort order on other versions of Python.
    imports_list = sorted(
        (mod_name, sorted(attr_names)) for mod_name, attr_names in imports.items()
    )

    # Format each module separately to ensure maximum one module per line.
    lines = []
    lines.append("[")
    for item in imports_list:
        for line in pformat(item, width=87, compact=True).splitlines():
            lines.append(f" {line}")
        lines[-1] += ","
    lines.append("]")

    return "\n".join(lines)


def format_test():
    return dedent(
        """\
        #!/usr/bin/env python3

        success = True

        def print_exception(e, mod_name, attr):
            global success
            success = False
            print(f"{type(e).__name__}: {mod_name}.{attr}")

        imports = {{ imports }}

        for mod_name, attrs in imports:
            try:
                # Pass a dummy `from` list so __import__ will return the actual module
                # rather than the top-level package.
                mod = __import__(mod_name, {}, {}, ["dummy"])
            except ImportError as e:
                for attr in attrs:
                    print_exception(e, mod_name, attr)
            else:
                for attr in attrs:
                    try:
                        getattr(mod, attr)
                    except AttributeError as e:
                        print_exception(e, mod_name, attr)

        if success:
            print("All names found")
    """
    ).replace("{{ imports }}", format_list())


if __name__ == "__main__":
    main()
