from rubicon.objc import *

# from toga.interface import Box as BoxInterface

from ..libs import *
from .base import Widget


class Box(Widget):
    def create(self):
        self.native = None
        self.constraints = None
