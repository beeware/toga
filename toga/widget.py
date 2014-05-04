from __future__ import print_function, unicode_literals, absolute_import, division

from toga.constraint import Attribute


class Widget(object):
    def __init__(self):
        self.LEFT = Attribute(self, Attribute.LEFT)
        self.RIGHT = Attribute(self, Attribute.RIGHT)
        self.TOP = Attribute(self, Attribute.TOP)
        self.BOTTOM = Attribute(self, Attribute.BOTTOM)
        self.LEADING = Attribute(self, Attribute.LEADING)
        self.TRAILING = Attribute(self, Attribute.TRAILING)
        self.WIDTH = Attribute(self, Attribute.WIDTH)
        self.HEIGHT = Attribute(self, Attribute.HEIGHT)
        self.CENTER_X = Attribute(self, Attribute.CENTER_X)
        self.CENTER_Y = Attribute(self, Attribute.CENTER_Y)
        # self.BASELINE = Attribute(self, Attribute.BASELINE)
