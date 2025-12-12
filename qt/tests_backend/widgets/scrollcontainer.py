from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QScrollArea, QStyle

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = QScrollArea
    scrollbar_inset = 16  # this is approximate, get exact value in init
    frame_inset = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrollbar_inset = (
            QApplication.instance()
            .style()
            .pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)
            + 1
        )

    @property
    def has_content(self):
        return self.impl.document_container.content is not None

    @property
    def document_height(self):
        return self.impl.document_container.native.height()

    @property
    def document_width(self):
        return self.impl.document_container.native.width()

    async def scroll(self):
        if (
            self.native.verticalScrollBarPolicy()
            != Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        ):
            self.native.verticalScrollBar().setValue(200)

    async def wait_for_scroll_completion(self):
        # Scroll isn't animated, so this is a no-op.
        pass
