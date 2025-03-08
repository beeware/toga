######################################################################
# Common constants
######################################################################

NORMAL = "normal"
LEFT = "left"
RIGHT = "right"
TOP = "top"
BOTTOM = "bottom"
CENTER = "center"
START = "start"
END = "end"

######################################################################
# Direction
######################################################################

ROW = "row"
COLUMN = "column"

######################################################################
# Visibility
######################################################################

VISIBLE = "visible"
HIDDEN = "hidden"
NONE = "none"

######################################################################
# Text Justification
######################################################################

JUSTIFY = "justify"

######################################################################
# Text Direction
######################################################################

RTL = "rtl"
LTR = "ltr"

######################################################################
# Font family
######################################################################

SYSTEM = "system"
MESSAGE = "message"

SERIF = "serif"
SANS_SERIF = "sans-serif"
CURSIVE = "cursive"
FANTASY = "fantasy"
MONOSPACE = "monospace"

######################################################################
# Font Styling
######################################################################

ITALIC = "italic"
OBLIQUE = "oblique"

FONT_STYLES = {ITALIC, OBLIQUE}

######################################################################
# Font Variant
######################################################################

SMALL_CAPS = "small-caps"

FONT_VARIANTS = {SMALL_CAPS}

######################################################################
# Font boldness
######################################################################

BOLD = "bold"

FONT_WEIGHTS = {BOLD}

######################################################################
# Font Size
######################################################################

SYSTEM_DEFAULT_FONT_SIZE = -1

XX_SMALL = "xx-small"
X_SMALL = "x-small"
SMALL = "small"
MEDIUM = "medium"
LARGE = "large"
X_LARGE = "x-large"
XX_LARGE = "xx-large"

ABSOLUTE_FONT_SIZES = {
    XX_SMALL,
    X_SMALL,
    SMALL,
    MEDIUM,
    LARGE,
    X_LARGE,
    XX_LARGE,
}

LARGER = "larger"
SMALLER = "smaller"

RELATIVE_FONT_SIZES = {LARGER, SMALLER}

FONT_SIZE_SCALE_FACTOR = 1.2

FONT_SIZE_SCALE = {
    XX_SMALL: 0.512,  # ~(1/FONT_SIZE_SCALE_FACTOR)^3 - 60% smaller
    X_SMALL: 0.64,  # ~(1/FONT_SIZE_SCALE_FACTOR)^2 - 40% smaller
    SMALL: 0.8,  # ~(1/FONT_SIZE_SCALE_FACTOR) - 20% smaller
    MEDIUM: 1.0,  # baseline
    LARGE: 1.2,  # ~FONT_SIZE_SCALE_FACTOR - 20% larger
    X_LARGE: 1.44,  # ~FONT_SIZE_SCALE_FACTOR^2 - 40% larger
    XX_LARGE: 1.728,  # ~FONT_SIZE_SCALE_FACTOR^3 - 60% larger
}

RELATIVE_FONT_SIZE_SCALE = {
    LARGER: FONT_SIZE_SCALE_FACTOR,  # 20% larger
    SMALLER: 1 / FONT_SIZE_SCALE_FACTOR,  # 20% smaller
}

######################################################################
# Colors
######################################################################

TRANSPARENT = "transparent"

ALICEBLUE = "aliceblue"
ANTIQUEWHITE = "antiquewhite"
AQUA = "aqua"
AQUAMARINE = "aquamarine"
AZURE = "azure"
BEIGE = "beige"
BISQUE = "bisque"
BLACK = "black"
BLANCHEDALMOND = "blanchedalmond"
BLUE = "blue"
BLUEVIOLET = "blueviolet"
BROWN = "brown"
BURLYWOOD = "burlywood"
CADETBLUE = "cadetblue"
CHARTREUSE = "chartreuse"
CHOCOLATE = "chocolate"
CORAL = "coral"
CORNFLOWERBLUE = "cornflowerblue"
CORNSILK = "cornsilk"
CRIMSON = "crimson"
CYAN = "cyan"
DARKBLUE = "darkblue"
DARKCYAN = "darkcyan"
DARKGOLDENROD = "darkgoldenrod"
DARKGRAY = "darkgray"
DARKGREY = "darkgrey"
DARKGREEN = "darkgreen"
DARKKHAKI = "darkkhaki"
DARKMAGENTA = "darkmagenta"
DARKOLIVEGREEN = "darkolivegreen"
DARKORANGE = "darkorange"
DARKORCHID = "darkorchid"
DARKRED = "darkred"
DARKSALMON = "darksalmon"
DARKSEAGREEN = "darkseagreen"
DARKSLATEBLUE = "darkslateblue"
DARKSLATEGRAY = "darkslategray"
DARKSLATEGREY = "darkslategrey"
DARKTURQUOISE = "darkturquoise"
DARKVIOLET = "darkviolet"
DEEPPINK = "deeppink"
DEEPSKYBLUE = "deepskyblue"
DIMGRAY = "dimgray"
DIMGREY = "dimgrey"
DODGERBLUE = "dodgerblue"
FIREBRICK = "firebrick"
FLORALWHITE = "floralwhite"
FORESTGREEN = "forestgreen"
FUCHSIA = "fuchsia"
GAINSBORO = "gainsboro"
GHOSTWHITE = "ghostwhite"
GOLD = "gold"
GOLDENROD = "goldenrod"
GRAY = "gray"
GREY = "grey"
GREEN = "green"
GREENYELLOW = "greenyellow"
HONEYDEW = "honeydew"
HOTPINK = "hotpink"
INDIANRED = "indianred"
INDIGO = "indigo"
IVORY = "ivory"
KHAKI = "khaki"
LAVENDER = "lavender"
LAVENDERBLUSH = "lavenderblush"
LAWNGREEN = "lawngreen"
LEMONCHIFFON = "lemonchiffon"
LIGHTBLUE = "lightblue"
LIGHTCORAL = "lightcoral"
LIGHTCYAN = "lightcyan"
LIGHTGOLDENRODYELLOW = "lightgoldenrodyellow"
LIGHTGRAY = "lightgray"
LIGHTGREY = "lightgrey"
LIGHTGREEN = "lightgreen"
LIGHTPINK = "lightpink"
LIGHTSALMON = "lightsalmon"
LIGHTSEAGREEN = "lightseagreen"
LIGHTSKYBLUE = "lightskyblue"
LIGHTSLATEGRAY = "lightslategray"
LIGHTSLATEGREY = "lightslategrey"
LIGHTSTEELBLUE = "lightsteelblue"
LIGHTYELLOW = "lightyellow"
LIME = "lime"
LIMEGREEN = "limegreen"
LINEN = "linen"
MAGENTA = "magenta"
MAROON = "maroon"
MEDIUMAQUAMARINE = "mediumaquamarine"
MEDIUMBLUE = "mediumblue"
MEDIUMORCHID = "mediumorchid"
MEDIUMPURPLE = "mediumpurple"
MEDIUMSEAGREEN = "mediumseagreen"
MEDIUMSLATEBLUE = "mediumslateblue"
MEDIUMSPRINGGREEN = "mediumspringgreen"
MEDIUMTURQUOISE = "mediumturquoise"
MEDIUMVIOLETRED = "mediumvioletred"
MIDNIGHTBLUE = "midnightblue"
MINTCREAM = "mintcream"
MISTYROSE = "mistyrose"
MOCCASIN = "moccasin"
NAVAJOWHITE = "navajowhite"
NAVY = "navy"
OLDLACE = "oldlace"
OLIVE = "olive"
OLIVEDRAB = "olivedrab"
ORANGE = "orange"
ORANGERED = "orangered"
ORCHID = "orchid"
PALEGOLDENROD = "palegoldenrod"
PALEGREEN = "palegreen"
PALETURQUOISE = "paleturquoise"
PALEVIOLETRED = "palevioletred"
PAPAYAWHIP = "papayawhip"
PEACHPUFF = "peachpuff"
PERU = "peru"
PINK = "pink"
PLUM = "plum"
POWDERBLUE = "powderblue"
PURPLE = "purple"
REBECCAPURPLE = "rebeccapurple"
RED = "red"
ROSYBROWN = "rosybrown"
ROYALBLUE = "royalblue"
SADDLEBROWN = "saddlebrown"
SALMON = "salmon"
SANDYBROWN = "sandybrown"
SEAGREEN = "seagreen"
SEASHELL = "seashell"
SIENNA = "sienna"
SILVER = "silver"
SKYBLUE = "skyblue"
SLATEBLUE = "slateblue"
SLATEGRAY = "slategray"
SLATEGREY = "slategrey"
SNOW = "snow"
SPRINGGREEN = "springgreen"
STEELBLUE = "steelblue"
TAN = "tan"
TEAL = "teal"
THISTLE = "thistle"
TOMATO = "tomato"
TURQUOISE = "turquoise"
VIOLET = "violet"
WHEAT = "wheat"
WHITE = "white"
WHITESMOKE = "whitesmoke"
YELLOW = "yellow"
YELLOWGREEN = "yellowgreen"
