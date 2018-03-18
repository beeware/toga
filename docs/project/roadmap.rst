Toga Roadmap
============

Toga is a new project - we have lots of things that we'd like to do. If
you'd like to contribute, providing a patch for one of these features.

Widgets
-------

The core of Toga is it's widget set. Modern GUI apps have lots of native
controls that need to be represented. The following widgets have no
representation at present, and need to be added.

There's also the task of porting widgets available on one platform to
another platform.

Input
~~~~~

Inputs are mechanisms for displaying and editing input provided by the user.

* ComboBox - A free entry TextField that provides options (e.g., text with
    past choices)
    - Cocoa: NSComboBox
    - GTK+: Gtk.ComboBox.new_with_model_and_entry
    - iOS: ?
    - Winforms: ?
    - Android: ?
* Switch - A native control for enabled/disabled
    - Cocoa: Done
    - GTK+: Gtk.CheckButton (maybe Gtk.Switch?)
    - iOS: UISwitch
    - Winforms: ?
    - Android: ?
* DateInput - A widget for selecting a date
    - Cocoa: NSDatePicker, constrained to DMY
    - GTK+: Gtk.Calendar?
    - iOS: UIDatePicker
    - Winforms: ?
    - Android: ?
* TimeInput - A widget for selecting a time
    - Cocoa: NSDatePicker, Constrained to Time
    - GTK+: ?
    - iOS: UIDatePicker
    - Winforms: ?
    - Android: ?
* DateTimeInput - A widget for selecting a date and a time.
    - Cocoa: NSDatePicker
    - GTK+: Gtk.Calendar + ?
    - iOS: UIDatePicker
    - Winforms: ?
    - Android: ?
* MultilineTextInput - A widget for displaying multiline text, optionally
    editable.
    - Cocoa: NSTextView inside an NSScrollView
    - GTK+: Gtk.TextView? (is there a simpler version than a full text editor?)
    - iOS: UITextView
    - Winforms: ?
    - Android: ?
* Selection - A button that allows the user to choose from one of a fixed
    number of options
    - Cocoa: NSPopupButton, with NSMenu for options.
    - GTK+: Gtk.ComboBox.new_with_model
    - iOS: UIPickerView
    - Winforms: ?
    - Android: ?
* ColorInput - A widget for selecting a color
    - Cocoa: NSColorWell
    - GTK+: Gtk.ColorButton
    - iOS: ?
    - Winforms: ?
    - Android: ?
* SliderInput (H & V) - A widget for selecting a value from a range.
    - Cocoa: NSSlider
    - GTK+: Gtk.Scale
    - iOS: UISlider
    - Winforms: ?
    - Android: ?
* NumberInput - A widget to allow entry of a numerical value, possibly with
    helper buttons to make it easy to increase/decrease the value.
    - Cocoa: NSTextField with NSStepper
    - GTK+: GTKSpinButton
    - iOS: UITextField with UIStepper
    - Winforms: ?
    - Android: ?
* Table: A scrollable display of columns of tabular data
    - Cocoa: Done
    - GTK+: Gtk.TreeView with a Gtk.ListStore
    - iOS: UITableView
    - Winforms: ListView (ListView.View.Details)
    - Android: ?
* Tree: A scrollable display of hierarchical data
    - Cocoa: Done
    - GTK+: Gtk.TreeView with a Gtk.TreeStore
    - iOS: UITableView with navigation
    - Winforms: ?
    - Android: ?
* DetailedList: A scrollable list of a single column of detailed data
    - Cocoa: NSTableView with custom view?
    - iOS: UITableView with navigation
    - Winforms: ?
    - Android: ?
* SearchInput - A variant of TextField that is decorated as a search box.
    - Cocoa: NSSearchField
    - GTK+: ?
    - iOS: UISearchBar?
    - Winforms: ?
    - Android: ?

Views
~~~~~

Views are mechanisms for displaying rich content, usually in a read-only manner.

* Separator - a visual separator; usually a faint line.
    - Cocoa: NSSeparator
    - GTK+:
    - iOS:
    - Winforms: ?
    - Android: ?
* ProgressBar - A horizontal bar that displays progress, either progress
    against a known value, or indeterminate
    - Cocoa: Done
    - GTK+: Gtk.ProgressBar
    - iOS: UIProgressView
    - Winforms: ?
    - Android: ?
* ActivityIndicator - A spinner widget showing that something is happening
    - Cocoa: NSProgressIndicator, Spinning style
    - GTK+: Gtk.Spinner
    - iOS: UIActivityIndicatorView
    - Winforms: ?
    - Android: ?
* ImageView - Display an graphical image
    - Cocoa: Done
    - GTK+: Gtk.Image
    - iOS: UIImageView
    - Winforms: ?
    - Android: ?
* VideoView - Display a video
    - Cocoa: AVPlayerView
    - GTK+: Custom Integrate with GStreamer
    - iOS: MPMoviePlayerController
    - Winforms: ?
    - Android: ?
* WebView - Display a web page. Just the web page; no URL chrome, etc.
    - Cocoa: Done
    - GTK+: Webkit.WebView (via WebkitGtk)
    - iOS: UIWebView
    - Winforms: WebBrowser
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

* Box - A box drawn around a collection of widgets; often has a label
    - Cocoa: NSBox
    - GTK+:
    - iOS:
    - Winforms: ?
    - Android: ?
* ButtonContainer - A layout for a group of radio/checkbox options
    - Cocoa: NSMatrix, or NSView with pre-set constraints.
    - GTK+: ListBox?
    - iOS:
    - Winforms: ?
    - Android: ?
* ScrollContainer - A container whose internal content can be scrolled.
    - Cocoa: Done
    - GTK+:
    - iOS: UIScrollView?
    - Winforms: Panel
    - Android: ?
* SplitContainer - An adjustable separator bar between 2+ visible panes of content
    - Cocoa: Done
    - GTK+:
    - iOS:
    - Winforms: SplitContainer
    - Android: ?
* FormContainer - A layout for a "key/value" or "label/widget" form
    - Cocoa: NSForm, or NSView with pre-set constraints.
    - GTK+:
    - iOS:
    - Winforms: ?
    - Android: ?
* OptionContainer - (suggestions for better name welcome) A container view that
    holds a small, fixed number of subviews, only one of which is visible at any
    given time. Generally rendered as something with "lozenge" style buttons
    over a box. Examples of use: OS X System preference panes that contain
    multiple options (e.g., Keyboard settings have an option layout for "Keyboard",
    "Text", "Shortcuts" and "Input sources")
    - Cocoa: Done
    - GTK+: GtkNotebook (Maybe GtkStack on 3.10+?)
    - iOS: ?
    - Winforms: TabControl
    - Android: ?
* SectionContainer - (suggestions for better name welcome) A container view that
    holds a small number of subviews, only one of which is visible at any
    given time. Each "section" has a name and icon. Examples of use: top level
    navigation in Safari's preferences panel.
    - Cocoa: NSTabView
    - GTK+: ?
    - iOS: ?
    - Winforms: ?
    - Android: ?
* TabContainer - A container view for holding an unknown number of subviews, each
    of which is of the same type - e.g., web browser tabs.
    - Cocoa: ?
    - GTK+: GtkNotebook
    - iOS: ?
    - Winforms: ?
    - Android: ?
* NavigationContainer - A container view that holds a navigable tree of subviews;
    essentially a view that has a "back" button to return to the previous view
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
the user.

* Info - a modal dialog providing an "OK" option
    - Cocoa: Done
    - GTK+: Gtk.MessageDialog, type Gtk.MessageType.INFO, buttons Gtk.ButtonsType.OK
    - iOS:
    - Winforms: ?
    - Android: ?
* Error - a modal dialog showing an error, and a continue option.
    - Cocoa: Done
    - GTK+: Gtk.MessageDialog, type Gtk.MessageType.ERROR, buttons Gtk.ButtonsType.CANCEL
    - iOS:
    - Winforms: ?
    - Android: ?
* Question - a modal dialog that asks a Yes/No question
    - Cocoa: Done
    - GTK+: Gtk.MessageDialog, type Gtk.MessageType.QUESTION, buttons Gtk.ButtonsType.YES_NO
    - iOS:
    - Winforms: ?
    - Android: ?
* Confirm - a modal dialog confirming "OK" or "cancel"
    - Cocoa: Done
    - GTK+: Gtk.MessageDialog, type Gtk.MessageType.WARNING, buttons Gtk.ButtonsType.OK_CANCEL
    - iOS:
    - Winforms: ?
    - Android: ?
* StackTrace - a modal dialog for displaying a long stack trace.
    - Cocoa: Done
    - GTK+: Custom Gtk.Dialog
    - iOS:
    - Winforms: ?
    - Android: ?
* File Open - a mechanism for finding and specifying a file on disk.
    - Cocoa:
    - GTK+: Gtk.FileChooserDialog
    - iOS:
    - Winforms: ?
    - Android: ?
* File Save - a mechanism for finding and specifying a filename to save to.
    - Cocoa: Done
    - GTK+:
    - iOS:
    - Winforms: ?
    - Android: ?

Miscellaneous
~~~~~~~~~~~~~

One of the aims of Toga is to provide a rich, feature-driven approach to
app development. This requires the development of APIs to support rich
features.

* Long running tasks - GUI toolkits have a common pattern of needing to
  periodically update a GUI based on some long running background task.
  They usually accomplish this with some sort of timer-based API to ensure
  that the main event loop keeps running. Python has a "yield" keyword that
  can be prepurposed for this.
* Toolbar - support for adding a toolbar to an app definition. Interpretation
  in mobile will be difficult; maybe some sort of top level action menu available
  via a slideout tray (e.g., GMail account selection tray)
* Preferences - support for saving app preferences, and visualizing them in a
  platform native way.
* Easy handling of long running tasks - possibly using generators to yield
  control back to the event loop.
* Notification when updates are available
* Easy Licensing/registration of apps. Monetization is not a bad thing, and
  shouldn't be mutually exclusive with open source.

Platforms
---------

Toga currently has good support for Cocoa on OS X, GTK+, and iOS.
Proof-of-concept support exists for Windows Winforms. Support for a more
modern Windows API would be desirable.

In the mobile space, it would be great if Toga supported Android, Windows
Phone, or any other phone platform.
