from rubicon.objc import *

from .base import Widget
from ..libs import *


class Box(Widget):
    def __init__(self, creator):
        self._creator = creator
        self._create()

    def _create(self):
        self._native = None
        self._constraints = None