import sys

import toga
from toga import platform

# If the user provided a --backend:<name> argument,
# use that backend as the factory.
backend = [arg.split(":")[1] for arg in sys.argv if arg.startswith("--backend:")]
try:
    platform.current_platform = backend[0]
except IndexError:
    pass


def main():
    app = toga.App()

    print(f"app.paths.app={app.paths.app.resolve()}")
    print(f"app.paths.data={app.paths.data.resolve()}")
    print(f"app.paths.cache={app.paths.cache.resolve()}")
    print(f"app.paths.logs={app.paths.logs.resolve()}")
    print(f"app.paths.toga={app.paths.toga.resolve()}")


if __name__ == "__main__":
    main()
