from concurrent.futures import Future

from travertino.size import at_least

from toga.types import LatLng

from ..libs import Gtk, WebKit2
from .base import Widget

MAPVIEW_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>
    <script
        src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>

    <style>
        html, body {
            height: 100%;
            margin: 0;
        }
        #map {
            height: 100%;
            width: 100%;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = L.map("map");
        const pins = {};
        const tiles = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 20,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
    </script>
</body>
</html>
"""


def pin_id(pin):
    "Rendering utility; output the ID of the pin"
    return hex(id(pin))


def latlng(location):
    "Rendering utility; output a lat/lng coordinate"
    return f"[{location.lat}, {location.lng}]"


def popup(pin):
    "Rendering utility; output the content of the pin popup"
    if pin.subtitle:
        return f"<b>{pin.title}</b><br>{pin.subtitle}"
    else:
        return f"<b>{pin.title}</b>"


class MapView(Widget):
    SUPPORTS_ON_SELECT = False

    def create(self):
        if WebKit2 is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import WebKit2. Ensure that the system package "
                "providing WebKit2 and its GTK bindings have been installed. "
                "See https://toga.readthedocs.io/en/stable/reference/api/widgets/mapview.html#system-requirements "
                "for details."
            )

        self.native = WebKit2.WebView()

        # Debugging: to enable the developer view.
        # settings = self.native.get_settings()
        # settings.set_property("enable-developer-extras", True)

        # The default cache model is WEB_BROWSER, which will
        # use the backing cache to minimize hits on the web server.
        # This can result in stale web content being served, even if
        # the source document (and the web server response) changes.
        context = self.native.get_context()
        context.set_cache_model(WebKit2.CacheModel.DOCUMENT_VIEWER)

        self.native.connect("load-changed", self.gtk_on_load_changed)
        self.backlog = []

        # Load the MapView content into the view.
        self.native.load_html(MAPVIEW_HTML_CONTENT, None)

    def gtk_on_load_changed(self, widget, load_event, *args):
        if load_event == WebKit2.LoadEvent.FINISHED:
            # The Toga API allows you to invoke methods on the MapView as soon
            # as it has been created; however, the web view implementing the map
            # can't process requests until the page has finished loading. As
            # soon as the page has finished loading, we can process the backlog
            # of API requests. Any return values will be ignored.
            for kwargs in self.backlog:
                self.native.evaluate_javascript(**kwargs)
            self.backlog = None

    def _invoke(self, javascript):
        # A future to collect the Javascript result
        future = Future()

        # A callback that will update the future when the Javascript is
        # complete.
        def js_finished(webview, result, *user_data):
            """If `evaluate_javascript_finish` from GTK returns a result, unmarshal it, and
            call back with the result."""
            try:
                value = webview.evaluate_javascript_finish(result)
                if value.is_number():
                    value = value.to_double()
                else:
                    value = value.to_string()
                    if value.startswith("LatLng("):
                        value = LatLng(*tuple(float(v) for v in value[7:-1].split(",")))

                future.set_result(value)
            except Exception as e:
                if e.code == WebKit2.JavascriptError.INVALID_RESULT:
                    # The object returned can't be parsed; it's probably a
                    # Javascript Object.
                    future.set_result(None)
                else:  # pragma: no cover
                    exc = RuntimeError(str(e))
                    future.set_exception(exc)

        kwargs = {
            "script": javascript,
            "length": len(javascript),
            "world_name": None,
            "source_uri": None,
            "cancellable": None,
            "callback": js_finished,
        }

        if self.backlog is not None:
            # If the WebView implementing the map isn't initialized yet, put the
            # request onto the backlog to be invoked once it is ready.
            self.backlog.append(kwargs)
            return None
        else:
            # Javascript evaluation is asynchronous, and all occurs in the GTK
            # GUI thread. Invoke the method with a callback; then internally
            # tick the GTK event loop until the Javascript result is returned.
            self.native.evaluate_javascript(**kwargs)

            while not future.done():
                Gtk.main_iteration_do(blocking=False)

            return future.result()

    def get_location(self):
        if self.backlog is None:
            return self._invoke("map.getCenter().toString();")
        else:  # pragma: no cover
            print(
                "MapView isn't fully initialized. "
                "MapView.location result will be unreliable"
            )
            return LatLng(0.0, 0.0)

    def set_location(self, position):
        self._invoke(f"map.panTo({latlng(position)});")

    def get_zoom(self):
        return self._invoke("map.getZoom();")

    def set_zoom(self, zoom):
        self._invoke(f"map.setZoom({zoom});")

    def add_pin(self, pin):
        self._invoke(
            f'pins["{pin_id(pin)}"] = L.marker({latlng(pin.location)}).addTo(map)'
            f'.bindPopup("{popup(pin)}");'
        )

    def update_pin(self, pin):
        self._invoke(
            f'pins["{pin_id(pin)}"].setLatLng({latlng(pin.location)})'
            f'.setPopupContent("{popup(pin)}");'
        )

    def remove_pin(self, pin):
        self._invoke(
            f'map.removeLayer(pins["{pin_id(pin)}"]); delete pins["{pin_id(pin)}"];'
        )

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
