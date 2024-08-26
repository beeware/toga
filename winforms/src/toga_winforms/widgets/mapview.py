import json
import webbrowser
from concurrent.futures import Future

import System.Windows.Forms as WinForms
from System import Action, String
from System.Drawing import Color
from System.Threading.Tasks import Task, TaskScheduler

import toga
from toga.types import LatLng
from toga_winforms.libs.extensions import (
    CoreWebView2CreationProperties,
    WebView2,
    WebView2RuntimeNotFoundException,
)

from ..libs.wrapper import WeakrefCallable
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
        self.native = WebView2()
        # WebView has a 2 phase startup; the widget needs to be initialized,
        # the content needs to be loaded. We can't actually use the widget
        # until the content is fully loaded.
        self.native.CoreWebView2InitializationCompleted += WeakrefCallable(
            self.winforms_initialization_completed
        )
        self.native.NavigationCompleted += WeakrefCallable(
            self.winforms_navigation_completed
        )
        self.loaded_future = None

        props = CoreWebView2CreationProperties()
        props.UserDataFolder = str(toga.App.app.paths.cache / "WebView2")
        self.native.CreationProperties = props

        # Trigger the configuration of the webview
        self.corewebview2_available = None
        self.native.EnsureCoreWebView2Async(None)
        self.native.DefaultBackgroundColor = Color.Transparent

        self.backlog = []

    def winforms_initialization_completed(self, sender, args):
        # The WebView2 widget has an "internal" widget (CoreWebView2) that is
        # the actual web view. The view isn't ready until the internal widget has
        # completed initialization, and that isn't done until an explicit
        # request is made (EnsureCoreWebView2Async).
        if args.IsSuccess:
            # We've initialized, so we must have the runtime
            self.corewebview2_available = True
            settings = self.native.CoreWebView2.Settings
            self.default_user_agent = settings.UserAgent

            # To enable debugging,
            settings.AreDefaultContextMenusEnabled = False
            settings.AreDevToolsEnabled = False

            settings.IsZoomControlEnabled = True

            # Now that the widget is initialized, we can load the HTML content
            self.native.NavigateToString(MAPVIEW_HTML_CONTENT)

        elif isinstance(
            args.InitializationException, WebView2RuntimeNotFoundException
        ):  # pragma: nocover
            print("Could not find the Microsoft Edge WebView2 Runtime.")
            if self.corewebview2_available is None:
                # The initialize message is sent twice on failure.
                # We only want to show the dialog once, so track that we
                # know the runtime is missing.
                self.corewebview2_available = False
                WinForms.MessageBox.Show(
                    "The Microsoft Edge WebView2 Runtime is not installed. "
                    "Web content will not be displayed.\n\n"
                    "Click OK to download the WebView2 Evergreen Runtime "
                    "Bootstrapper from Microsoft.",
                    "Missing Edge Webview2 runtime",
                    WinForms.MessageBoxButtons.OK,
                    WinForms.MessageBoxIcon.Error,
                )
                webbrowser.open(
                    "https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download"
                )

        else:  # pragma: nocover
            WinForms.MessageBox.Show(
                "A critical error has occurred and functionality may be impaired.\n\n"
                "The WebView2 initialization failed with an exception:\n\n"
                f"{args.InitializationException}",
                "Error",
                WinForms.MessageBoxButtons.OK,
                WinForms.MessageBoxIcon.Error,
            )

    def winforms_navigation_completed(self, sender, args):
        # The Toga API allows you to invoke methods on the MapView as soon
        # as it has been created; however, the web view implementing the map
        # can't process requests until the page has finished loading. As
        # soon as the page has finished loading, we can process the backlog
        # of API requests. Any return values will be ignored.
        for javascript in self.backlog:
            self.native.ExecuteScriptAsync(javascript)
        self.backlog = None

    def _invoke(self, javascript):
        if self.backlog is not None:
            self.backlog.append(javascript)
            return None
        else:
            future = Future()
            task_scheduler = TaskScheduler.FromCurrentSynchronizationContext()

            def callback(task):
                # If the evaluation fails, task.Result will be "null", with no way to
                # distinguish it from an actual null return value.
                value = json.loads(task.Result)
                future.set_result(value)

            self.native.ExecuteScriptAsync(javascript).ContinueWith(
                Action[Task[String]](callback), task_scheduler
            )

            # Process Winforms events until the result is available
            while not future.done():
                WinForms.Application.DoEvents()

            return future.result()

    def get_location(self):
        if self.backlog is None:
            result = self._invoke("map.getCenter();")
            return LatLng(result["lat"], result["lng"])
        else:  # pragma: no cover
            print(
                "MapView isn't fully initialized. "
                "Mapview.location result will be unreliable"
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
