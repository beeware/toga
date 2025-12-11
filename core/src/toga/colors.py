from typing import TYPE_CHECKING

# Color, rgb, and hsl need to be explicitly imported in order for mkdocstrings to see
# them. However, we also want to import all 148 named colors, and it seems silly to
# list them here individually.
from travertino.colors import *  # noqa: F401, F403, I001
from travertino.colors import Color, hsl, rgb  # noqa: F401, I001

if TYPE_CHECKING:
    from typing import TypeAlias

    ColorT: TypeAlias = Color | str
    """
    Toga's color APIs accept:

    - An instance of Toga's [`rgb`][toga.colors.rgb] or [`hsl`][toga.colors.hsl] class.
    - The name of a [CSS named color](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/named-color).
      Strings of all available color names are available as constants. These constants
      are named the same as their value, except in all caps, as is the convention for
      Python constants. In other words, `toga.colors.ORANGE == "orange"`.
    - A string representing the color as [hexadecimal RGB or RGBA](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/hex-color).

    The following color definitions would all be equivalent:

    ```python
    import toga
    from toga.colors import hsl, rgb, YELLOW

    toga.Box(color=rgb(255, 255, 0))
    toga.Box(color=hsl(60, 1, .5))
    toga.Box(color="yellow")
    toga.Box(color=YELLOW)
    toga.Box(color="#FF0")
    toga.Box(color="#FFFF00")
    ```

    None of these specify alpha (transparency), so the color defaults to fully opaque.
    [`rgb`][toga.colors.rgb], [`hsl`][toga.colors.hsl], and the hex string format allow
    alpha to be specified as well. Thus, the following, which explicitly set the alpha
    to opaque, are *also* equivalent:

    ```python
    toga.Box(color=rgb(255, 255, 0, 1))
    toga.Box(color=hsl(60, 1, .5, 1))
    toga.Box(color="#FF0F")
    toga.Box(color="#FFFF00FF")
    ```

    As is the case in CSS, `rgba` and `hsla` are available as aliases for `rgb` and
    `hsl`, respectively. `rgb` and `hsl` are the preferred forms, but either will work
    identically.
    """
