from .base import Widget
from ..libs.activity import MainActivity
from ..libs.android_widgets import RelativeLayout


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(MainActivity.singletonThis)

    def add_child(self, child):
        super().add_child(child)
        self.native.addView(child.native)
