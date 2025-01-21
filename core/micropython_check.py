#!/usr/bin/env python3
#
# This script should be run under MicroPython to check that it can import all the Toga
# modules required by Invent.

# The top-level Toga module must be imported first, to enable the standard library
# compatibility shims.
#
# isort: off
import toga

# isort: on
import sys
import traceback

# Access attributes to trigger lazy import.
failures = 0
for name in [
    "App",
    "Font",
    "Image",
    "Window",
    #
    "Widget",
    "Box",
    "Button",
    "DateInput",
    "Divider",
    "ImageView",
    "Label",
    "MultilineTextInput",
    "PasswordInput",
    "ProgressBar",
    "Slider",
    "Switch",
    "TextInput",
    "TimeInput",
]:
    try:
        getattr(toga, name)
    except Exception:
        failures += 1
        print(f"Failed to import toga.{name}:")
        traceback.print_exc()
        print()

if failures:
    print(f"{failures} names failed to import")
    sys.exit(1)
else:
    print("All names imported successfully")
