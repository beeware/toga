from .libs import UIFont


CACHE = {}


def font_impl(font):
    try:
        font = CACHE[font]
    except KeyError:
        font = UIFont.fontWithName(self.family, size=self.size)

    return font
