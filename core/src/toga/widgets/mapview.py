from __future__ import annotations

import sys
from typing import TYPE_CHECKING, overload

from .base import Widget

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias

    import toga

    MapPinContent: TypeAlias = (
        tuple[tuple[float, float], str | None]
        | tuple[tuple[float, float], str | None, str | None]
        | toga.MapPin
    )


class MapPin:
    def __init__(self, location, *, title=None, subtitle=None):
        self.location = location
        self.title = title
        self.subtitle = subtitle

    def __repr__(self):
        if self.title and self.subtitle:
            label = f"; {self.title} - {self.subtitle}"
        elif self.title:
            label = f"; {self.title}"
        else:
            label = ""

        return f"<Map Pin @ ({self.location}); {label}"


class MapPinSet:
    def __init__(self, interface, pins):
        self.interface = interface
        self._pins = set()

        if pins:
            for item in pins:
                if isinstance(item, tuple):
                    location, title, subtitle = item
                    pin = MapPin(location, title=title, subtitle=subtitle)

                    self.add(pin)
                else:
                    self.add(item)

    def __repr__(self):
        return f"<MapPinSet: ({len(self)} pins)>"

    def __iter__(self):
        """Return an iterator over the pins on the map."""
        return iter(self._pins)

    def __len__(self):
        """Return the number of pins being displayed."""
        return len(self._pins)

    @overload
    def add(
        self,
        location_or_pin: MapPin,
    ): ...

    @overload
    def add(
        self,
        location_or_pin: tuple[float, float],
        *,
        title: str | None = None,
        subtitle: str | None = None,
    ): ...

    def add(
        self,
        location_or_pin: MapPin | tuple[float, float],
        *,
        title: str | None = None,
        subtitle: str | None = None,
    ) -> MapPin:
        """Add a new pin to the map.

        The new pin can be specified as an existing :any:`MapPin` instance, or by
        specifying the full details of the new pin. If a :any:`MapPin` is provided,
        specifying ``title`` or ``subtitle`` will raise an error.

        :param location_or_pin: The location of the pin as a (latitude, longitude)
            tuple, or a :any:`toga.MapPin` instance.
        :param title: The title to apply to the pin.
        :param subtitle: The subtitle to apply to the pin.
        :return
        """
        if isinstance(location_or_pin, MapPin):
            if title is not None:
                raise ValueError("Cannot specify title if using a MapPin instance.")
            if subtitle is not None:
                raise ValueError("Cannot specify subtitle if using a MapPin instance.")

            pin = location_or_pin
        else:
            pin = MapPin(location_or_pin, title=title, subtitle=subtitle)

        self._pins.add(pin)
        self.interface._impl.add_pin(pin)
        return pin

    def remove(self, pin):
        """Remove a pin from the map.

        :param pin: The pin to remove.
        """
        self._pins.remove(pin)
        self.interface._impl.remove_pin(pin)

    def clear(self):
        """Remove all pins from the map."""
        for pin in self._pins:
            self._impl.interface.remove_pin(pin)
        self._pins = set()


class MapView(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        location: tuple[float, float] | None = None,
        zoom: int | None = 2,
        pins: list[MapPinContent] | None = None,
    ):
        """Create a new MapView widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param location: The initial latitude/longitude where the map should be
            centered. If not provided, the initial location for the map is undefined.
        :param zoom: The initial zoom level for the map.
        :param pins: The initial pins to display on the map.
        """
        super().__init__(id=id, style=style)

        self._impl = self.factory.MapView(interface=self)

        self._pins = MapPinSet(self, pins)

        if location:
            self.location = location

        self.zoom = zoom

    @property
    def location(self) -> tuple[float, float]:
        "The latitude/longitude where the map is centered."
        return self._impl.get_location()

    @location.setter
    def location(self, coordinates: tuple[float, float]):
        self._impl.set_location(coordinates)

    @property
    def zoom(self) -> int:
        """Set the zoom level for the map.

        The zoom level is an integer in the range 0-5 (inclusive). The level of detail
        visible at each zoom level is:

        * 0: An entire country
        * 1: The location of a city in relation to nearby cities.
        * 2: The extents of a large city.
        * 3: The relationship of the neighborhood to surrounding areas.
        * 4: The relationship of a city block to nearby blocks
        * 5: The names of individual roads and buildings

        The zoom level can be set, but not read.

        If the provided zoom value is outside the 0-5 range, it will be clipped.
        """
        raise RuntimeError("zoom is not a readable property")

    @zoom.setter
    def zoom(self, value):
        if value < 0:
            value = 0
        elif value > 5:
            value = 5

        self._impl.set_zoom(value)

    @property
    def pins(self) -> MapPinSet:
        """The set of pins currently being displayed on the map"""
        return self._pins
