from ..probe import BaseProbe


class ScaffoldProbe(BaseProbe):
    def __init__(self, scaffold):
        self.scaffold = scaffold
        self.impl = scaffold._impl
        self.container = self.impl.container

    @property
    def content_size(self):
        size = self.container.native.size()
        return (size.width(), size.height())
