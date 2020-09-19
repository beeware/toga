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
widgets. In other words, it's the public API for creating apps, windows, widgets
etc.

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
toolkit); ``toga-gtk`` for Linux (using the GTK+ toolkit); and so on. In other
words, it's the layer that provides the implementation of the public API for a
specific platform. It provides a private, internal API that the interface can
use to create widgets.

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
widgets required by the widget toolkit of your system. These are accessed
using whatever bridging or Python-native API is available on the implementation
platform. In other words, it's the API for the underlying system widgets. This
is usually provided by system-level APIs, not by Toga itself.

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

Put all together
----------------

If you want to develop ``Toga`` you must be have deep understanding about these
layers and how they are work together, so in the following few lines we will
provide you with an example of ``How they are work together`` in linux as a one
of the available platforms, do not wary they are really very simple unlike they
are appearing:
* ``toga.Button`` defined in ``toga/src/core`` folder. This is the public
  interface, and defines (amongst other things) that there is an ``on_click``
  event handler on a Button.
* ``toga-gtk.widgets.Button`` defined in ``toga/scr/toga-gtk`` folder. This
  provides the implementation of ``toga.Button``, describing how to create a
  button on GTK, and how to connect the ``GTK`` clicked signal to the ``on_click``
  Toga handler.
* ``Gtk.Button`` the native GTK-Python Widget API that implements buttons on GTK.

As you may conclude, in this way we can change the implementation of ``Button``
without changing the public API that end-users rely on. We're also able to provide.

The last note in this section, as you may be note if you browsed the ``toga``
code, ``toga-dummy`` in the ``toga/scr/dummy`` folder - an implementation of the
internal API that is completely platform independent that can be used for testing
purposes.
