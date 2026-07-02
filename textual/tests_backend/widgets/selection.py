from textual.widgets import Select as TextualSelect

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    native_class = TextualSelect
    minimum_required_height = 80

    def assert_resizes_on_content_change(self):
        pass

    @property
    def width(self):
        return max(
            super().width,
            self.impl.scale_out_horizontal(self.impl.intrinsic_width),
        )

    @property
    def titles(self):
        return self.impl.titles

    @property
    def selected_title(self):
        selected_index = self.impl.get_selected_index()
        if selected_index is None:
            return None

        return self.widget._title_for_item(self.widget.items[selected_index])

    async def select_item(self):
        self.native.value = 1

    def assert_vertical_text_align(self, expected):
        return
