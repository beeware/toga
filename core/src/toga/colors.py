# Color, rgb, and hsl need to be explicitly imported in order for mkdocstrings to see
# them. However, we also want to import all 148 named colors, and it seems silly to
# list them here individually.
from travertino.colors import *  # noqa: F401, F403, I001
from travertino.colors import Color, rgb, hsl  # noqa: F401, I001
