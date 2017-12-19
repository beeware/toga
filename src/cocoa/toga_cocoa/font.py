from .libs import NSFont
from toga.font import MESSAGE, NORMAL, SYSTEM, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE

CACHE = {}


def font(f):
    try:
        font = CACHE[f]
    except KeyError:
        if f.family == SYSTEM:
            font = NSFont.systemFontOfSize(f.size)
        elif f.family == MESSAGE:
            font = NSFont.messageFontOfSize(f.size)
        else:
            if f.family is SERIF:
                family = 'Times-Roman'
            elif f.family is SANS_SERIF:
                family = 'Helvetica'
            elif f.family is CURSIVE:
                family = 'Apple Chancery'
            elif f.family is FANTASY:
                family = 'Papyrus'
            elif f.family is MONOSPACE:
                family = 'Courier New'
            else:
                family = f.family

            full_name = '{family}{weight}{style}'.format(
                family=family,
                weight=(' ' + f.weight.title()) if f.weight is not NORMAL else '',
                style=(' ' + f.style.title()) if f.style is not NORMAL else '',
            )
            font = NSFont.fontWithName(full_name, size=f.size)

            if font is None:
                print("Unable to load font: {}pt {}".format(f.size, full_name))
        CACHE[f] = font

    return font
