from travertino.size import at_least

from ..libs import android_widgets
from .base import Widget
from toga_android.window import AndroidViewport


class Table(Widget):
    table_layout = None

    def create(self):
        self.table_layout = android_widgets.TableLayout(self._native_activity)
        table_layout_params = android_widgets.TableLayout__Layoutparams(
            android_widgets.TableLayout__Layoutparams.MATCH_PARENT,
            android_widgets.TableLayout__Layoutparams.MATCH_PARENT
        )
        self.table_layout.setLayoutParams(table_layout_params)
        self.native = self.table_layout
        widget.viewport = AndroidViewport(widget.native)

    def change_source(self, source):
        pass

    def get_selection(self):
        pass

    def scroll_to_row(self, row):
        pass

    def set_on_select(self, _on_select):
        pass

    def set_on_double_click(self, _on_double_click):
        pass

    def add_column(self, heading, accessor):
        pass

    def remove_column(self, accessor):
        pass

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            android_widgets.View__MeasureSpec.UNSPECIFIED,
            android_widgets.View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
