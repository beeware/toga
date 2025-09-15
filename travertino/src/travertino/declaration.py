######################################################################
# 2-2025: Backwards compatibility for Toga < 0.5.0
######################################################################

# declaration.py has been split into two modules. Toga < 0.5.0 will look here for
# BaseStyle and Choices.

from warnings import filterwarnings, warn

# Make sure deprecation warnings are shown by default
filterwarnings("default", category=DeprecationWarning)

warn(
    (
        "The travertino.declaration module is deprecated; its contents are now"
        "located in travertino.style and travertino.properties.\n"
        "This error probably means you've updated Travertino to 0.5.0 but are "
        "still using Toga <= 0.4.8; to fix, either update Toga to >= 0.5.0, or "
        "pin Travertino to 0.3.0."
    ),
    DeprecationWarning,
    stacklevel=2,
)

from .properties.choices import Choices  # noqa
from .style import BaseStyle  # noqa
