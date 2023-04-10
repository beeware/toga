========
Road Map
========

Toga is a new project - we have lots of things that we'd like to do. If
you'd like to contribute, you can provide a patch for one of these features.

Widgets
-------

The core of Toga is its widget set. Modern GUI apps have lots of native
controls that need to be represented. The following widgets have no
representation at present, and need to be added.

There's also the task of porting widgets available on one platform to
another platform.

Input
~~~~~

Inputs are mechanisms for displaying and editing input provided by the user.

* ``ComboBox`` - A free entry text field that provides options (e.g., text with past choices)

    - Cocoa: ``NSComboBox``
    - GTK: ``Gtk.ComboBox.new_with_model_and_entry``
    - iOS: ?
    - Winforms: ``ComboBox``
    - Android: ``Spinner``

* ``DateTimeInput`` - A widget for selecting a date and a time.

    - Cocoa: ``NSDatePicker``
    - GTK: `Gtk.Calendar` + ?
    - iOS: ``UIDatePicker``
    - Winforms: ``DateTimePicker``
    - Android: ?

* ``ColorInput`` - A widget for selecting a color

    - Cocoa: ``NSColorWell``
    - GTK: ``Gtk.ColorButton`` or ``Gtk.ColorSelection``
    - iOS: ?
    - Winforms: ?
    - Android: ?

* ``SearchInput`` - A variant of ``TextField`` that is decorated as a search box.

    - Cocoa: ``NSSearchField``
    - GTK: ``Gtk.Entry``
    - iOS: ``UISearchBar``?
    - Winforms: ?
    - Android: ?

Views
~~~~~

Views are mechanisms for displaying rich content,
usually in a read-only manner.

* ``VideoView`` - Display a video

    - Cocoa: ``AVPlayerView``
    - GTK: Custom integration with ``GStreamer``
    - iOS: ``MPMoviePlayerController``
    - Winforms: ?
    - Android: ?

* ``PDFView`` - Display a PDF document

    - Cocoa: ``PDFView``
    - GTK: ?
    - iOS: Integration with QuickLook?
    - Winforms: ?
    - Android: ?

* ``MapView`` - Display a map

    - Cocoa: ``MKMapView``
    - GTK: Probably a ``Webkit.WebView`` pointing at Google Maps/OpenStreetMap
    - iOS: ``MKMapView``
    - Winforms: ?
    - Android: ?


Container widgets
~~~~~~~~~~~~~~~~~

Containers are widgets that can contain other widgets.

* ``ButtonContainer`` - A layout for a group of radio/checkbox options

    - Cocoa: ``NSMatrix``, or ``NSView`` with pre-set constraints.
    - GTK: ``Gtk.ListBox``
    - iOS: ?
    - Winforms: ?
    - Android: ?

* ``FormContainer`` - A layout for a "key/value" or "label/widget" form

    - Cocoa: ``NSForm``, or ``NSView`` with pre-set constraints.
    - GTK:
    - iOS:
    - Winforms: ?
    - Android: ?

* ``NavigationContainer`` - A container view that holds a navigable tree of sub-views

    Essentially a view that has a "back" button to return to the previous view
    in a hierarchy. Example of use: Top level navigation in the macOS System
    Preferences panel.

    - Cocoa: No native control
    - GTK: No native control; ``Gtk.HeaderBar`` in 3.10+
    - iOS: ``UINavigationBar`` + ``NavigationController``
    - Winforms: ?
    - Android: ?

Miscellaneous
~~~~~~~~~~~~~

One of the aims of Toga is to provide a rich, feature-driven approach to
app development. This requires the development of APIs to support rich
features.

* Preferences - Support for saving app preferences, and visualizing them in a
  platform native way.

* Notification when updates are available

* Easy Licensing/registration of apps - Monetization is not a bad thing, and
  shouldn't be mutually exclusive with open source.

Platforms
---------

Toga currently has good support for Cocoa on macOS, GTK on Linux, Winforms on
Windows, iOS and Android. Proof-of-concept support exists for single page web
apps. Support for a more modern Windows API would be desirable.
