from .toggle import *  # noqa
from .toggle import Toggle


class Switch(Toggle):
    """The functionality of Switch is now implemented by Toggle.
    This class exists to ensure backwards compatibility."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
