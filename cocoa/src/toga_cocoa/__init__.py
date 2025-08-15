import importlib
from pathlib import Path

from travertino import _package_version


def lazy_load():
    toga_cocoa_imports = {}
    pyi = Path(__file__).with_suffix(".pyi")
    with pyi.open() as f:
        for line in f:
            segments = line.split()
            if segments and segments[0] == "from":
                toga_cocoa_imports[segments[3]] = segments[1]
    return toga_cocoa_imports


toga_cocoa_imports = lazy_load()

__all__ = list(toga_cocoa_imports.keys())


def __getattr__(name):
    try:
        module_name = toga_cocoa_imports[name]
    except KeyError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name)
        globals()[name] = value
        return value


__version__ = _package_version(__file__, __name__)
