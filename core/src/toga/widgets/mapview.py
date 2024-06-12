from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Protocol

import toga
from toga.handlers import wrapped_handler

from .base import StyleT, Widget


class MapPin:
    def __init__(
        self,
        location: toga.LatLng | tuple[float, float],
        *,
        title: str,
        subtitle: str | None = None,
    ):
        """Create a new map pin.

        :param location: A tuple describing the (latitude, longitude) for the pin.
        :param title: The title to apply to the pin.
        :param subtitle: A subtitle label to apply to the pin.
        """
        self._location = toga.LatLng(*location)
        self._title = title
        self._subtitle = subtitle

        # A pin isn't tied to a map at time of creation.
        self.interface: MapView | None = None
        self._native = None

    def __repr__(self) -> str:
        if self.subtitle:
            label = f"; {self.title} - {self.subtitle}"
        else:
            label = f"; {self.title}"

        return f"<MapPin @ {self.location}{label}>"

    @property
    def location(self) -> toga.LatLng:
        """The (latitude, longitude) where the pin is located."""
        return self._location

    @location.setter
    def location(self, coord: toga.LatLng | tuple[float, float]) -> None:
        self._location = toga.LatLng(*coord)
        if self.interface:
            self.interface._impl.update_pin(self)

    @property
    def title(self) -> str:
        """The title of the pin."""
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = str(title)
        if self.interface:
            self.interface._impl.update_pin(self)

    @property
    def subtitle(self) -> str | None:
        """The subtitle of the pin."""
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str | None) -> None:
        if subtitle is not None:
            subtitle = str(subtitle)
        self._subtitle = subtitle
        if self.interface:
            self.interface._impl.update_pin(self)


class MapPinSet:
    def __init__(self, interface: MapView, pins: Iterable[MapPin] | None):
        self.interface = interface
        self._pins: set[MapPin] = set()

        if pins is not None:
            for item in pins:
                self.add(item)

    def __repr__(self) -> str:
        return f"<MapPinSet ({len(self)} pins)>"

    def __iter__(self) -> Iterator[MapPin]:
        """Return an iterator over the pins on the map."""
        return iter(self._pins)

    def __len__(self) -> int:
        """Return the number of pins being displayed."""
        return len(self._pins)

    def add(self, pin: MapPin) -> None:
        """Add a new pin to the map.

        :param pin: The :any:`toga.MapPin` instance to add.
        """
        pin.interface = self.interface
        self._pins.add(pin)
        self.interface._impl.add_pin(pin)

    def remove(self, pin: MapPin) -> None:
        """Remove a pin from the map.

        :param pin: The  :any:`toga.MapPin` instance to remove.
        """
        self.interface._impl.remove_pin(pin)
        self._pins.remove(pin)
        pin.interface = None

    def clear(self) -> None:
        """Remove all pins from the map."""
        for pin in self._pins:
            self.interface._impl.remove_pin(pin)
        self._pins = set()


class OnSelectHandler(Protocol):
    def __call__(self, widget: MapView, /, *, pin: MapPin, **kwargs: Any) -> object:
        """A handler that will be invoked when the user selects a map pin.

        :param widget: The MapView that was selected.
        :param pin: The pin that was selected.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class MapView(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        location: toga.LatLng | tuple[float, float] | None = None,
        zoom: int = 11,
        pins: Iterable[MapPin] | None = None,
        on_select: toga.widgets.mapview.OnSelectHandler | None = None,
    ):
        """Create a new MapView widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param location: The initial latitude/longitude where the map should be
            centered. If not provided, the initial location for the map is Perth,
            Australia.
        :param zoom: The initial zoom level for the map.
        :param pins: The initial pins to display on the map.
        :param on_select: A handler that will be invoked when the user selects a map
            pin.
        """
        super().__init__(id=id, style=style)

        self._impl: Any = self.factory.MapView(interface=self)

        self._pins = MapPinSet(self, pins)

        if location:
            self.location = location
        else:
            # Default location is Perth, Australia. Because why not?
            self.location = (-31.9559, 115.8606)

        self.zoom = zoom

        self.on_select = on_select

    @property
    def location(self) -> toga.LatLng:
        """The latitude/longitude where the map is centered.

        A tuple of ``(latitude, longitude)`` can be provided as input; this will be
        converted into a :any:`toga.LatLng` object.
        """
        return self._impl.get_location()

    @location.setter
    def location(self, coordinates: toga.LatLng | tuple[float, float]) -> None:
        self._impl.set_location(toga.LatLng(*coordinates))

    @property
    def zoom(self) -> int:
        """Set the zoom level for the map.

        The zoom level is an integer in the range 0-20 (inclusive). It can be used to
        set the number of degrees of longitude that will span a 256 :ref:`CSS pixel
        <css-units>` region in the horizontal axis of the map, following the
        relationship::

            longitude_per_256_pixels = 360 / (2**zoom)

        In practical terms, this means a 256px square will cover:

        * 0-2: Whole world
        * 3-6: Large countries
        * 7-8: Small countries, or a state in a large country
        * 9-11: The extent of a city
        * 12-14: Suburbs of a city, or small towns
        * 15-17: Roads at the level useful for navigation
        * 18-19: Individual buildings
        * 20: A single building

        These zoom levels use the same mathematical basis as the OpenStreetMap API. See
        `OpenStreetMap's documentation on zoom levels
        <https://wiki.openstreetmap.org/wiki/Zoom_levels>`__ for more details.

        If the provided zoom value is outside the supported range, it will be clipped.

        At very low zoom levels, some backends may constrain the viewable range to avoid
        repeating map tiles in the visible area. This effectively sets a minimum bound
        on the zoom level that can be requested. The value of this minimum varies
        depending on the size and aspect ratio of the map view.
        """
        return round(self._impl.get_zoom())

    @zoom.setter
    def zoom(self, value: int) -> None:
        value = int(value)
        if value < 0:
            value = 0
        elif value > 20:
            value = 20

        self._impl.set_zoom(value)

    @property
    def pins(self) -> MapPinSet:
        """The set of pins currently being displayed on the map"""
        return self._pins

    @property
    def on_select(self) -> OnSelectHandler:
        """The handler to invoke when the user selects a pin on a map.

        **Note:** This is not currently supported on GTK or Windows.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler: toga.widgets.mapview.OnSelectHandler | None) -> None:
        if handler and not getattr(self._impl, "SUPPORTS_ON_SELECT", True):
            self.factory.not_implemented("MapView.on_select")

        self._on_select = wrapped_handler(self, handler)
