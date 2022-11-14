import sys
import types

# Before we import toga, check for the --interactive flag
# If that flag exists, mock the behavior of an interactive shell
# - replace the __main__ module with an in-memory representation.
if "--interactive" in sys.argv:
    sys.modules["__main__"] = types.ModuleType("__main__")

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
    app = toga.App("Standalone App", "org.testbed.standalone-app")

    print(f"app.paths.app={app.paths.app.resolve()}")
    print(f"app.paths.data={app.paths.data.resolve()}")
    print(f"app.paths.cache={app.paths.cache.resolve()}")
    print(f"app.paths.logs={app.paths.logs.resolve()}")
    print(f"app.paths.toga={app.paths.toga.resolve()}")


if __name__ == "__main__":
    main()
