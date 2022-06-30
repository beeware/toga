import importlib
import sys

import toga

# If the user provided a --backend:<name> argument,
# use that backend as the factory.
backend = [
    arg.split(":")[1]
    for arg in sys.argv
    if arg.startswith("--backend:")
]
try:
    factory = importlib.import_module(f"toga_{backend[0]}").factory
except IndexError:
    factory = None


def main():
    app = toga.App('Testbed App', 'org.testbed.simple-app', factory=factory)

    print(f"app.paths.app={app.paths.app}")
    print(f"app.paths.data={app.paths.data}")
    print(f"app.paths.cache={app.paths.cache}")
    print(f"app.paths.logs={app.paths.logs}")
    print(f"app.paths.toga={app.paths.toga}")


if __name__ == '__main__':
    main()
