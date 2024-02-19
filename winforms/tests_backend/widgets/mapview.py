import pytest
from Microsoft.Web.WebView2.WinForms import WebView2

from .base import SimpleProbe


class MapViewProbe(SimpleProbe):
    native_class = WebView2
    location_threshold = 0.0001

    async def latitude_span(self):
        northeast = self.impl._invoke("map.getBounds().getNorthEast()")
        southwest = self.impl._invoke("map.getBounds().getSouthWest()")
        print("northeast", northeast)
        print("southwest", southwest)
        return northeast["lat"] - southwest["lat"]

    @property
    def pin_count(self):
        return int(self.impl._invoke("Object.keys(pins).length;"))

    async def select_pin(self, pin):
        pytest.skip("Winforms MapView doesn't support selecting pins")
