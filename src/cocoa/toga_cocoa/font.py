from .libs import NSFont
from toga.font import MESSAGE, NORMAL, SYSTEM, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE

_FONT_CACHE = {}


def native_font(font):
    try:
        native = _FONT_CACHE[font]
    except KeyError:
        if font.family == SYSTEM:
            native = NSFont.systemFontOfSize(font.size)
        elif font.family == MESSAGE:
            native = NSFont.messageFontOfSize(font.size)
        else:
            if font.family is SERIF:
                family = 'Times-Roman'
            elif font.family is SANS_SERIF:
                family = 'Helvetica'
            elif font.family is CURSIVE:
                family = 'Apple Chancery'
            elif font.family is FANTASY:
                family = 'Papyrus'
            elif font.family is MONOSPACE:
                family = 'Courier New'
            else:
                family = font.family

            full_name = '{family}{weight}{style}'.format(
                family=family,
                weight=(' ' + font.weight.title()) if font.weight is not NORMAL else '',
                style=(' ' + font.style.title()) if font.style is not NORMAL else '',
            )
            native = NSFont.fontWithName(full_name, size=font.size)

            if native is None:
                print("Unable to load font: {}pt {}".format(font.size, full_name))
            else:
                _FONT_CACHE[font] = native

    return native


def measure_text(font, text, tight=False):
    # TODO
    pass
