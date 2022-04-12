.. _architecture:

============
Architecture
============

Although Toga presents a single interface to the end user, there are three
internal layers that make up every widget. They are:

* The **Interface** layer

* The **Implementation** layer

* The **Native** layer

Interface
---------

The interface layer is the public, documented interface for each widget.
Following :ref:`Toga's design philosophy <abstract-broad-concepts>`, these
widgets reflect high-level design concepts, rather than specific common
widgets. It forms the public API for creating apps, windows, widgets, and so
on.

The interface layer is responsible for validation of any API inputs, and
storage of any persistent values retained by a widget. That storage may be
supplemented or replaced by storage on the underlying native widget (or
widgets), depending on the capabilities of that widget.

The interface layer is also responsible for storing style and layout-related
attributes of the widget.

The interface layer is defined in the ``toga-core`` module.

Implementation
--------------

The implementation layer is the platform-specific representation of each
widget. Each platform that Toga supports has its own implementation layer,
named after the widget toolkit that the implementation layer is wrapping --
``toga-cocoa`` for macOS (Cocoa being the name of the underlying macOS widget
toolkit); ``toga-gtk`` for Linux (using the GTK+ toolkit); and so on. The
implementation provides a private, internal API that the interface layer can
use to create the widgets described by the interface layer.

The API exposed by the implementation layer is different to that exposed by
the interface layer and is *not* intended for end-user consumption. It is a
utility API, servicing the requirements of the interface layer.

Every widget in the implementation layer corresponds to exactly one widget in the
interface layer. However, the reverse will not always be true. Some widgets
defined by the interface layer are not available on all platforms.

An interface widget obtains its implementation when it is constructed, using
the platform factory. Each platform provides a factory implementation. When a
Toga application starts, it guesses its platform based on the value of
``sys.platform``, and uses that factory to create implementation-layer widgets.

If you have an interface layer widget, the implementation widget can be
obtained using the ``_impl`` attribute of that widget.

Native
------

The lowest layer of Toga is the native layer. The native layer represents the
widgets required by the widget toolkit of your system. These are accessed using
whatever bridging library or Python-native API is available on the
implementation platform. This layer is usually provided by system-level APIs,
not by Toga itself.

Most implementation widgets will have a single native widget. However, when a
platform doesn't expose a single widget that meets the requirements of the Toga
interface specification, the implementation layer will use multiple native
widgets to provide the required functionality.

In this case, the implementation must provide a single "container" widget that
represents the overall geometry of the combined native widgets. This widget
is called the "primary" native widget. When there's only one native widget,
the native widget is the primary native widget.

If you have an implementation widget, the interface widget can be obtained
using the ``interface`` attribute, and the primary native widget using the
``native`` attribute.

If you have a native widget, the interface widget can be obtained using the
``interface`` attribute, and the implementation widget using the ``impl``
attribute.

An example
----------

Here's how Toga's three-layer API works on the Button widget.

* ``toga.Button`` is defined in ``src/core/toga/widgets/button.py``. This
  defines the public interface for the Button widget, describing (amongst other
  things) that there is an ``on_click`` event handler on a Button. It expects
  that there will be *an* implementation, but doesn't care which implementation
  is provided.

* ``toga-gtk.widgets.Button`` is defined in
  ``src/gtk/toga-gtk/widgets/button.py``. This defines the Button at the
  implementation layer. It describes how to create a button on GTK, and how to
  connect the GTK ``clicked`` signal to the ``on_click`` Toga handler.

* ``Gtk.Button`` is the native GTK-Python widget API that implements buttons on
  GTK.

This three layered approach allows us to change the implementation of ``Button``
without changing the public API that end-users rely upon. For example, we
could switch out ``toga-gtk.widgets.Button`` with ``toga-cocoa.widgets.Button``
to provide a macOS implementation of the Button without altering the API that
end-users use to construct buttons.

The layered approach is especially useful with more complex widgets. Every
platform provides a Button widget, but other widgets are more complex. For
example, macOS doesn't provide a native DetailedList view, so it must be
constructed out of a scroll view, a table view, and a collection of other
pieces. The three layered architecture hides this complexity - the API exposed
to developers is a single (interface layer) widget; the complexity of the
implementation only matters to the maintainers of Toga.

Lastly, the layered approach provides a testing benefit. In addition to
the Cocoa, GTK, and other platform implementations, there is a "dummy"
implementation. This implementation satisfies all the API requirements of a
Toga implementation layer, but without actually performing any graphical
operations. This dummy API can be used to test code using the Toga interface
layer.
