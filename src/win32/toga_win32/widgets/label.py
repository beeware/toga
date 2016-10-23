from __future__ import print_function, absolute_import, division

from ..libs import *
from toga.constants import LEFT_ALIGNED, RIGHT_ALIGNED

from .base import Widget

class Label(Widget):
    window_class = 'static'
    default_style = WS_VISIBLE | WS_CHILD


    def __init__(self, text=None, alignment=LEFT_ALIGNED):
        super(Label, self).__init__(text=text)
        self.alignment = alignment
        alignments = {LEFT_ALIGNED: SS_LEFT, RIGHT_ALIGNED: SS_RIGHT}
        alignment = alignments[self.alignment]
        self.control_style |= alignment
