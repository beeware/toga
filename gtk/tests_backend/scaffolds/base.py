import pytest

from toga_gtk.libs import GTK_VERSION

from ..probe import BaseProbe


class ScaffoldProbe(BaseProbe):
    def __init__(self, scaffold):
        super().__init__()
        self.scaffold = scaffold
        self.impl = scaffold._impl
        self.container = self.impl.container

    @property
    def content_size(self):
        if GTK_VERSION < (4, 0, 0):
            allocation = self.container.get_allocation()
            return allocation.width, allocation.height
        else:
            pytest.skip("Content size in GTK4 is not implemented")
