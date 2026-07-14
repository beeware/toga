from textual.containers import Container as TextualContainer

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = TextualContainer
