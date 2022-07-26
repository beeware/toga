import importlib
import sys
# If the user provided a --app:<name> argument,
# import that module as the app.
app = [
    arg.split(":")[1]
    for arg in sys.argv
    if arg.startswith("--app:")
]
main = importlib.import_module(f"{app[0]}.app").main


if __name__ == "__main__":
    main()
