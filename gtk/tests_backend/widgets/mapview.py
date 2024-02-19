import pytest

from toga_gtk.libs import WebKit2

from .base import SimpleProbe


class MapViewProbe(SimpleProbe):
    native_class = WebKit2.WebView

    async def latitude_span(self):
        northeast = self.impl._invoke("map.getBounds().getNorthEast().toString();")
        southwest = self.impl._invoke("map.getBounds().getSouthWest().toString();")
        return northeast.lat - southwest.lat

    @property
    def pin_count(self):
        return int(self.impl._invoke("Object.keys(pins).length;"))

    async def select_pin(self, pin):
        pytest.skip("GTK MapView doesn't support selecting pins")
