# Extending Toga

While Toga provides a rich set of features, it can't provide every widget that is available on every platform. Additionally, because widgets are implemented as time permits by contributors, some backends may lack a widget that another backend provides. This means that application authors may find themselves in a situation where they need to write a custom widget. This topic guide explains how Toga finds widget implementations, and how people can expand the available widgets for their application.

## Writing a widget

As noted in the [Internal architecture](architecture.md) topic guide, a widget is made up of three layers: interface, implementation, and native. Every interface widget has a `_create` method that is responsible for creating the implementation of the widget, and passing the interface object to the new implementation object's `__init__` method. The implementation in turn has its own `create` method that should create any native widgets or other state that is needed when the widget is added to the layout, and also should implement at least the `rehint` method to help the layout system determine the size of the widget.

In the simplest possible case if you are creating a widget for your own application where you only care about one backend, you can write the implementation class and and an interface where the `_create` method directly imports the implementation class and instantiates it.

### Example: A Qt dial

As an example, the Qt library has a `QDial` class that acts a lot like a [`Slider`][toga.Slider] but displays a round dial instead of a linear slider. We can write a subclass of [`Slider`][toga.Slider] that will use a `QDial` as follows.

In `dial.py` we create a subclass of [`Slider`][toga.Slider] with a `_create` method that imports the qt `Dial` implementation and instantiates it:

```python
from toga import Slider

class Dial(Slider):
    """The Dial interface."""

    def _create(self):
        from .qt_dial import Dial
        return Dial(interface=self)
```

Then in `qt_dial.py` we create a subclass of `toga_qt.widgets.slider.Slider` that creates a `QDial`:

```python
from PySide6.QtWidgets import QDial
from toga_qt.widgets.slider import Slider

class Dial(Slider):
    """The Dial implementation."""

    def create(self):
        IntSliderImpl.__init__(self)
        self.native = QDial()
        self.native.setMinimum(0)
        self.native.valueChanged.connect(self.qt_on_change)
        self.native.sliderPressed.connect(self.qt_on_press)
        self.native.sliderReleased.connect(self.qt_on_release)

    def rehint(self):
        ...
```

More complex widgets will obviously have a lot more to them, but this will often be sufficient for a one-off custom widget for an application.

## Widgets with multiple backends

The previous section is fine as long as you only care about one backend implementation, but as soon as you have multiple backends that you care about you are faced with the problem of how does the interface know which implementation to use?

Toga solves this with "factory" objects which are name-spaces that lazily load implementations based on the [`toga.backend`][toga.backend]. The default factory object uses the Python standard library [`importlib.metadata`][importlib.metadata] "entry point" system to load backend widgets in a plugin-style system. Every backend advertises where to find the widget implementations as part of its `pyproject.toml`. So if you look at the `toga_qt`'s `pyproject.toml` you will see a section that looks like:

```toml
[project.entry-points."toga_core.backend.toga_qt"]
App = "toga_qt.app:App"
Command = "toga_qt.command:Command"
Font = "toga_qt.fonts:Font"
```

and so-on. This tells [`importlib.metadata`][importlib.metadata] that there is a group of entry points called `toga_core.backend.toga_qt` and each entry point consists of an interface name (like `App`) and the location of the implementation (like `toga_qt.app:App`, which means the `App` class in the `toga_at.app` module).

The factory object is a property on the widget which calls out to [`toga.platform.get_factory`][toga.platform.get_factory] with an appropriate parameter: `"toga_core"` by default, but custom widgets can override this property to get the appropriate `Factory` instance for the widget. The factory widget has the implementation classes as lazily looked-up attributes. For example, if you have an instance of a factory called `my_factory`, `my_factory.Slider` will give you the implementation class for the Slider widget in the current backend. If you look at the widget interface classes in Toga, you will see that most of their `_create` methods look like:

```python
class Slider(Widget):

    def _create(self):
        return self.factory.Slider(interface=self)
```

### Implementing missing widgets

Not every widget is available in every backend. If a backend doesn't provide a widget, it will raise `NotImplementedError`. However, you can fill gaps in Toga's widget availability by providing a Python project that contains an implementation and an entry point for that widget.

For example, at the time of writing, the `toga_textual` backend doesn't implement the [`toga.Switch`][toga.Switch] widget. We could write one something like this in a module `my_project.textual_switch`:

```python
from textual.widgets import Checkbox as TextualCheckbox
from travertino.size import at_least
from toga_textual.widgets.base import Widget

class TogaCheckbox(TextualCheckbox):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_checkbox_changed(self, event: TextualCheckbox.Changed) -> None:
        self.interface.on_change()


class Switch(Widget):
    def create(self):
        self.native = TogaCheckbox(self)

    def get_text(self):
        return self.native.label

    def set_text(self, text):
        self.native.label = text

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        self.native.value = value

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.native.label) + 8)
        self.interface.intrinsic.height = 3
```

and then add the following to the project's `pyproject.toml`:

```toml
[project.entry-points."toga_core.backend.toga_textual"]
Switch = "my_project.textual_switch:Switch"
```

The project metadata needs to be updated in your environment, so that Python's `importlib.metadata` is aware of the new widget, which means you will likely need to re-run `pip install` on your project in your development environment. It should automatically get picked up when you run code or tests using tools like `hatch` or `tox`, which install your project into a clean environment when run, or when you build and install wheels from your project.

With this set-up, you can import and use `toga.Switch` within your application that uses the `toga_textual` backend.

Ideally, if you have a working implementation of a missing widget, you'd make a pull-request to add it to the appropriate Toga backend.

### A Note About Briefcase Applications

Briefcase projects don't use Python's entry point system, so you can't just add the entry points to a Briefcase project's `pyroject.toml`. Instead any widgets you need have to be implemented as a separate Python project with it's own `pyproject.toml` that contains the entry points, and which is a dependency of your application. The `customwidget` example in the Toga examples shows how you might do this.

### Implementing a new backend

You can use these ideas to implement a new backend for Toga. To do this, you would need to write as many of the backend class implementations as is possible in a project, and then in the `pyproject.toml` list entry points in the `toga.backend` group for each platform that supports the backend, and then have entry points for each backend implementation.

For example, Toga is not likely to ever have an official WxPython backend as part of the core library because WxPython is not a native UI toolkit. But there may be value in such a backend for applications that are already using WxPython. Since this is not an official backend, you might call it `togax_wx`, and your `pyproject.toml` would look like:

```toml
[project.entry-points."toga.backends"]
linux = "togax_wx"
windows = "togax_wx"
macOS = "togax_wx"
freeBSD = "togax_wx"

[project.entry-points."toga_core.backend.togax_wx"]
App = "togax_wx.app:App"
Command = "togax_wx.command:Command"
```

and so on, and then update your development environment using `pip` if needed every time you add a new widget to the `pyproject.toml`.

### Implementing new interfaces

All of the examples with multiple backends rely on widgets which already exist as part of the `toga_core` interface. What if we want to implement our own interface widgets?

We could implement them using the `toga_core.backend.*` groups, but this runs the risk of colliding with other libraries, or with future widgets added to Toga by the core team. The solution in this case is to create your own custom `togax_*` interface and use it instead of `toga_core`.

For example, at the time of writing the Toga core does not provide a `Toggle Button` widget (i.e. a push-button which toggles state when pressed) or a checkbox widget, relying on the similar `Switch` for this sort of UI interaction. We could write a library which provides these extra button widgets in the following way.

We will call the library `togax_extra_switches` and write a collection of implementations as `extra_switches.cocoa.toggle`, `extra_switches.cocoa.checkbox`, `extra_switches.qt.toggle`, `extra_switches.qt.checkbox`, and so-on. For example `extra_switches.qt.toggle` might look something like:

```python
from PySide6.QtWidgets import QPushButton
from travertino.size import at_least

from toga_qt.widgets.switch import Switch

class Toggle(Switch):

    def create(self):
        self.native = QPushButton()
        self.native.setCheckable(True)
        self.native.toggled.connect(self.qt_on_change)
```

Other backends would be implemented similarly. We could even include `extra_switches.wx.toggle` and `extra_switches.wx.checkbox` implementations for our WxWidgets backend.

When it comes time to write the interface class for `Toggle` we can base it directly on `Switch`, but instead of being in the `toga_core` set of widget interfaces, it is in the `togax_extra_switches` interface group. As a result, we need to override the `factory` property of the interface widget to return a factory for this interface group.

```python
from functools import cached_property

from toga import Switch

class Toggle(Switch)

    @cached_property
    def factory(self):
        # ensure we get the factory for the "togax_extra_switches" entry points
        return get_factory("togax_extra_switches")

    def _create(self):
        self.factory.Toggle(interface=self)
```

Once this is written, we can add the entry points to the `pyproject.toml`:

```toml
[project.entry-points."togax_extra_switches.backend.toga_qt"]
Toggle = "extra_switches.qt.toggle:Toggle"
Checkbox = "extra_switches.qt.checkbox:Checkbox"

[project.entry-points."togax_extra_switches.backend.toga_cocoa"]
Toggle = "extra_switches.cocoa.toggle:Toggle"
Checkbox = "extra_switches.cocoa.checkbox:Checkbox"

[project.entry-points."togax_extra_switches.backend.togax_wx"]
Toggle = "extra_switches.wx.toggle:Toggle"
Checkbox = "extra_switches.wx.checkbox:Checkbox"
```

and so on, and then update your development environment using `pip` if needed.

## Other backend-dependent objects

There are other objects beyond widgets which are dependent on different backend implementations, particularly hardware features, but also things like notification displays, clipboards, and other OS services.

To extend Toga in this way, ensure that you get the appropriate factory for your extension, and use that to create the implementation object.

For example, an accelerometer hardware interface as part of a `togax_sensors` library could look something like:

```python
from toga.platform import get_factory

class Accelerometer:

    def __init__(self, app: App):
        self.factory = get_factory('togax_sensors')
        self._app = app
        self._impl = self.factory.Accelerometer(interface=self)

    @property
    def acceleration(self):
        return self._impl.get_acceleration()
```

with the corresponding backend for Qt looking something like:

```python
from PySide6.QtSensors import QAccelerometer

class Accelerometer:

    def __init__(self, interface):
        self.interface = interface
        self.native = QAccelerometer(interface._app._impl.native)

    def get_acceleration(self):
        reading = self.native.reading()
        return (reading.x(), reading.y(), reading.z())
```

and entry points like:

```toml
[project.entry-points."togax_sensors.backend.toga_qt"]
Accelerometer = "togax_sensors.qt.accelerometer:Accelerometer"
```
