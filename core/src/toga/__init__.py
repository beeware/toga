import importlib
import warnings
from pathlib import Path

from travertino import _package_version


def lazy_load():
    toga_core_imports = {}
    pyi = Path(__file__).with_suffix(".pyi")
    with pyi.open() as f:
        for line in f:
            segments = line.split()
            if segments[0] == "from":
                toga_core_imports[segments[3]] = segments[1]
    return toga_core_imports


toga_core_imports = lazy_load()

__all__ = list(toga_core_imports.keys())


def __getattr__(name):
    try:
        module_name = toga_core_imports[name]
    except KeyError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    else:
        module = importlib.import_module(module_name)
        value = getattr(module, name)
        globals()[name] = value
        return value


class NotImplementedWarning(RuntimeWarning):
    # pytest.warns() requires that Warning() subclasses are constructed by passing a
    # single argument (the warning message). Use a factory method to avoid reproducing
    # the message format and the warn invocation.
    @classmethod
    def warn(cls, platform: str, feature: str) -> None:
        """Raise a warning that a feature isn't implemented on a platform."""
        warnings.warn(
            NotImplementedWarning(f"[{platform}] Not implemented: {feature}"),
            stacklevel=2,
        )


# __name__ is "toga" in this file, but the distribution name is "toga-core".
__version__ = _package_version(__file__, "toga-core")
