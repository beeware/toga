Toga Roadmap
============

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

* ComboBox - A free entry TextField that provides options (e.g., text with past choices)

    - Cocoa: NSComboBox
    - GTK+: Gtk.ComboBox.new_with_model_and_entry
    - iOS: ?
    - Winforms: ComboBox
    - Android: Spinner

* DateInput - A widget for selecting a date

    - Cocoa: NSDatePicker, constrained to DMY
    - GTK+: Gtk.Calendar
    - iOS: UIDatePicker
    - Winforms: DateTimePicker
    - Android: ?

* TimeInput - A widget for selecting a time

    - Cocoa: NSDatePicker, Constrained to Time
    - GTK+: Custom Gtk.SpinButton
    - iOS: UIDatePicker
    - Winforms: DateTimePicker
    - Android: ?

* DateTimeInput - A widget for selecting a date and a time.

    - Cocoa: NSDatePicker
    - GTK+: Gtk.Calendar + ?
    - iOS: UIDatePicker
    - Winforms: DateTimePicker
    - Android: ?

* ColorInput - A widget for selecting a color

    - Cocoa: NSColorWell
    - GTK+: Gtk.ColorButton or Gtk.ColorSelection
    - iOS: ?
    - Winforms: ?
    - Android: ?

* SliderInput (H & V) - A widget for selecting a value from a range.

    - Cocoa: NSSlider
    - GTK+: Done
    - iOS: UISlider
    - Winforms: ?
    - Android: ?

* SearchInput - A variant of TextField that is decorated as a search box.

    - Cocoa: NSSearchField
    - GTK+: Gtk.Entry
    - iOS: UISearchBar?
    - Winforms: ?
    - Android: ?

Views
~~~~~

Views are mechanisms for displaying rich content,
usually in a read-only manner.

* Separator - a visual separator; usually a faint line.

    - Cocoa: NSSeparator
    - GTK+: Gtk.Separator
    - iOS:
    - Winforms: ?
    - Android: ?

* ActivityIndicator - A spinner widget showing that something is happening

    - Cocoa: NSProgressIndicator, Spinning style
    - GTK+: Gtk.Spinner
    - iOS: UIActivityIndicatorView
    - Winforms: ?
    - Android: ?

* VideoView - Display a video

    - Cocoa: AVPlayerView
    - GTK+: Custom Integrate with GStreamer
    - iOS: MPMoviePlayerController
    - Winforms: ?
    - Android: ?

* PDFView - Display a PDF document

    - Cocoa: PDFView
    - GTK+: ?
    - iOS: ? Integration with QuickLook?
    - Winforms: ?
    - Android: ?

* MapView - Display a map

    - Cocoa: MKMapView
    - GTK+: Probably a Webkit.WebView pointing at Google Maps/OpenStreetMap.org
    - iOS: MKMapView
    - Winforms: ?
    - Android: ?


Container widgets
~~~~~~~~~~~~~~~~~

Containers are widgets that can contain other widgets.

* ButtonContainer - A layout for a group of radio/checkbox options

    - Cocoa: NSMatrix, or NSView with pre-set constraints.
    - GTK+: Gtk.ListBox
    - iOS:
    - Winforms: ?
    - Android: ?

* FormContainer - A layout for a "key/value" or "label/widget" form

    - Cocoa: NSForm, or NSView with pre-set constraints.
    - GTK+:
    - iOS:
    - Winforms: ?
    - Android: ?

* SectionContainer - (suggestions for better name welcome)

    A container view that holds a small number of subviews,
    only one of which is visible at any given time.
    Each "section" has a name and icon.
    Examples of use: top level navigation in Safari's preferences panel.

    - Cocoa: NSTabView
    - GTK+: ?
    - iOS: ?
    - Winforms: ?
    - Android: ?

* TabContainer - A container view for holding an unknown number of subviews, each of which is of the same type - e.g., web browser tabs.

    - Cocoa: ?
    - GTK+: GtkNotebook
    - iOS: ?
    - Winforms: ?
    - Android: ?

* NavigationContainer - A container view that holds a navigable tree of subviews

    Essentially a view that has a "back" button to return to the previous view
    in a hierarchy. Example of use: Top level navigation in the OS X System
    Preferences panel.

    - Cocoa: No native control
    - GTK+: No native control; Gtk.HeaderBar in 3.10+
    - iOS: UINavigationBar + NavigationController
    - Winforms: ?
    - Android: ?

Dialogs and windows
~~~~~~~~~~~~~~~~~~~

GUIs aren't all about widgets - sometimes you need to pop up a dialog to query
the user. Info, Error, Question, Confirm, StackTrace and Save File Dialogs have been
implemented.

* File Open - a mechanism for finding and specifying a file on disk.

    - Cocoa:
    - GTK+: Gtk.FileChooserDialog
    - iOS:
    - Winforms: ?
    - Android: ?

Miscellaneous
~~~~~~~~~~~~~

One of the aims of Toga is to provide a rich, feature-driven approach to
app development. This requires the development of APIs to support rich
features.

* Long running tasks -

    GUI toolkits have a common pattern of needing to
    periodically update a GUI based on some long running background task.
    They usually accomplish this with some sort of timer-based API to ensure
    that the main event loop keeps running. Python has a "yield" keyword that
    can be repurposed for this.

* Toolbar -

    Support for adding a toolbar to an app definition.
    Interpretation in mobile will be difficult;
    maybe some sort of top level action menu available via a slideout tray
    (e.g., GMail account selection tray)

* Preferences -

    Support for saving app preferences, and visualizing them in a
    platform native way.

* Easy handling of long running tasks -

    Possibly using generators to yield control back to the event loop.

* Notification when updates are available

* Easy Licensing/registration of apps -

    Monetization is not a bad thing,
    and shouldn't be mutually exclusive with open source.

Platforms
---------

Toga currently has good support for Cocoa on OS X, GTK+, and iOS.
Proof-of-concept support exists for Windows Winforms. Support for a more
modern Windows API would be desirable.

In the mobile space, it would be great if Toga supported Android, Windows
Phone, or any other phone platform.
