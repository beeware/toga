from __future__ import annotations

from typing import Any, Protocol

from toga.handlers import wrapped_handler

from .base import Widget


class MapPin:
    def __init__(
        self,
        location: tuple[float, float],
        *,
        title: str | None = None,
        subtitle: str | None = None,
    ):
        """Create a new map pin.

        :param location: A tuple describing the (latitude, longitude) for the pin.
        :param title: The title to apply to the pin.
        :param subtitle: A subtitle label to apply to the pin.
        """
        self._location = location
        self._title = title
        self._subtitle = subtitle

        # A pin isn't tied to a map at time of creation.
        self.interface = None
        self._native = None

    def __repr__(self):
        if self.title and self.subtitle:
            label = f"; {self.title} - {self.subtitle}"
        elif self.title:
            label = f"; {self.title}"
        else:
            label = ""

        return f"<Map Pin @ {self.location}{label}>"

    @property
    def location(self) -> tuple[float, float]:
        "The (latitude, longitude) where the pin is located."
        return self._location

    @location.setter
    def location(self, coord: tuple[float, float]) -> None:
        self._location = coord
        if self.interface:
            self.interface._impl.update_pin(self)

    @property
    def title(self) -> tuple[float, float]:
        "The title of the pin."
        return self._title

    @title.setter
    def title(self, coord: tuple[float, float]) -> None:
        self._title = coord
        if self.interface:
            self.interface._impl.update_pin(self)

    @property
    def subtitle(self) -> tuple[float, float]:
        "The subtitle of the pin."
        return self._subtitle

    @subtitle.setter
    def subtitle(self, coord: tuple[float, float]) -> None:
        self._subtitle = coord
        if self.interface:
            self.interface._impl.update_pin(self)


class MapPinSet:
    def __init__(self, interface, pins):
        self.interface = interface
        self._pins = set()

        if pins:
            for item in pins:
                self.add(item)

    def __repr__(self):
        return f"<MapPinSet: ({len(self)} pins)>"

    def __iter__(self):
        """Return an iterator over the pins on the map."""
        return iter(self._pins)

    def __len__(self):
        """Return the number of pins being displayed."""
        return len(self._pins)

    def add(self, pin):
        """Add a new pin to the map.

        :param pin: The :any:`toga.MapPin` instance to add.
        """
        pin.interface = self.interface
        self._pins.add(pin)
        self.interface._impl.add_pin(pin)

    def remove(self, pin):
        """Remove a pin from the map.

        :param pin: The  :any:`toga.MapPin` instance to remove.
        """
        self.interface._impl.remove_pin(pin)
        self._pins.remove(pin)
        pin.interface = None

    def clear(self):
        """Remove all pins from the map."""
        for pin in self._pins:
            self._impl.interface.remove_pin(pin)
        self._pins = set()


class OnSelectHandler(Protocol):
    def __call__(self, widget: MapView, *, pin: MapPin, **kwargs: Any) -> None:
        """A handler that will be invoked when the user selects a map pin.

        .. note::
            ``**kwargs`` ensures compatibility with additional arguments
            introduced in future versions.

        :param widget: The button that was pressed.
        :param pin: The pin that was selected.
        """
        ...


class MapView(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        location: tuple[float, float] | None = None,
        zoom: int | None = 2,
        pins: list[MapPin] | None = None,
        on_select: OnSelectHandler | None = None,
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

        self._impl = self.factory.MapView(interface=self)

        self._pins = MapPinSet(self, pins)

        # Set zoom before location, because on some platforms changing the
        # zoom requires reading (and therefore resetting) the location.
        self.zoom = zoom

        if location:
            self.location = location
        else:
            # Default location is Perth, Australia. Because why not?
            self.location = (-31.9513, 115.8553)

        self.on_select = on_select

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
    def zoom(self, value: int):
        if value < 0:
            value = 0
        elif value > 5:
            value = 5

        self._impl.set_zoom(int(value))

    @property
    def pins(self) -> MapPinSet:
        """The set of pins currently being displayed on the map"""
        return self._pins

    @property
    def on_select(self) -> OnSelectHandler:
        """The handler to invoke when the user selects a pin on a map."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: OnSelectHandler | None):
        self._on_select = wrapped_handler(self, handler)
