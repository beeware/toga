import sys
import types

# Before we import toga, check for the --interactive flag
# If that flag exists, mock the behavior of an interactive shell
# - replace the __main__ module with an in-memory representation.
sys.modules["__main__"] = types.ModuleType("__main__")

import toga  # noqa: E402


class SubclassedApp(toga.App):
    pass


def main():
    app = SubclassedApp("Interactive App", "org.testbed.interactive-app")

    print(f"app.paths.app={app.paths.app.resolve()}")
    print(f"app.paths.config={app.paths.config.resolve()}")
    print(f"app.paths.data={app.paths.data.resolve()}")
    print(f"app.paths.cache={app.paths.cache.resolve()}")
    print(f"app.paths.logs={app.paths.logs.resolve()}")
    print(f"app.paths.toga={app.paths.toga.resolve()}")


if __name__ == "__main__":
    main()
