from __future__ import print_function, unicode_literals, absolute_import, division

from .base import Widget

class Container(Widget):

    def __init__(self):
        super(Container, self).__init__()

    def add(self, widget):
        pass

    def constrain(self, constraint):
        pass