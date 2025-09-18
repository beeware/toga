import site
import sys


def import_pyside6():
    """Temporarily break isolation to import system PySide6."""
    system_site = site.getsitepackages()
    print(system_site)
    old_path = sys.path.copy()
    sys.path.extend(system_site)
    import PySide6  # noqa

    sys.path = old_path


import_pyside6()
