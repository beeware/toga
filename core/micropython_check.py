#!/usr/bin/env python3
#
# This script should be run under MicroPython to check that the modules required by
# Invent can be imported.

# Toga must be imported first to enable the standard library compatibility shims.
# isort: off
import toga

# isort: on
import sys
import traceback

# Access attributes to trigger lazy import.
failures = 0
for name in [
    "App",
    # TODO: all other names required to support Invent
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
