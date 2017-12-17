from .libs import NSFont


CACHE = {}


def font_impl(font):
    try:
        font = CACHE[font]
    except KeyError:
        font = NSFont.fontWithName(self.family, size=self.size)

    return font
