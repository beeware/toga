from .textinput import TextInputProbe


class MultilineTextInputProbe(TextInputProbe):
    @property
    def document_height(self):
        return self.native.getLayout().getHeight() / self.scale_factor

    @property
    def document_width(self):
        return self.native.getLayout().getWidth() / self.scale_factor

    @property
    def vertical_scroll_position(self):
        return self.native.getScrollY() / self.scale_factor

    async def wait_for_scroll_completion(self):
        pass
