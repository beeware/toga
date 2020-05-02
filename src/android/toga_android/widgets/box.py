from .base import Widget
from ..libs.activity import MainActivity
from ..libs.android_widgets import RelativeLayout


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(MainActivity.singletonThis)
