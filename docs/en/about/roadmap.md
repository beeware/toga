# Toga's Road Map { #road-map }

Toga is a new project - we have lots of things that we'd like to do. If you'd like to contribute, you can provide a patch for one of these features.

## Widgets

The core of Toga is its widget set. Modern GUI apps have lots of native controls that need to be represented. The following widgets have no representation at present, and need to be added.

There's also the task of porting widgets available on one platform to another platform.

### Input

Inputs are mechanisms for displaying and editing input provided by the user.

#### Partially implemented widgets

- `Table`  Mobile platforms don't provide a native "Table" widget; however, table-like data could be rendered by using a [`DetailedList`][toga.DetailedList], where the title and subtitle are the "important" columns selected by the user, and selecting a row on the table navigates to a sub-page showing the full row detail.

- `Tree`  As with Table, mobile platforms don't provide a native "Tree" widget; however, we could use a similar approach to Table.  On Windows, the native widget doesn't provide support for more than one column. This means we either need to make a special case on Windows for a "simple" tree; or we need to form a composite widget that pairs the scrolling of a table with a tree.

- `DateTimeInput` - A widget for selecting a date and a time.
  - Cocoa: `NSDatePicker`
  - GTK: `Gtk.Calendar` + ?
  - iOS: `UIDatePicker`

#### New widgets

- `RadioButton` - a set of mutually exclusive options.  Functionally, the use case of "select one from a list of options" can be met with a [`Selection`][toga.Selection]; however, from a UI design perspective, a radio button is a common design pattern.  See [this issue](https://github.com/beeware/toga/issues/2225) for discussion of how this widget may be implemented in a way that compliments existing widgets.

- `ComboBox` - A free entry text field that provides options (e.g., text with past choices)
  - Cocoa: `NSComboBox`
  - GTK: `Gtk.ComboBox.new_with_model_and_entry`
  - iOS: ?
  - Winforms: `ComboBox`
  - Android: `Spinner`

- `ColorInput` - A widget for selecting a color
  - Cocoa: `NSColorWell`
  - GTK: `Gtk.ColorButton` or `Gtk.ColorSelection`
  - iOS: ?
  - Winforms: ?
  - Android: ?

- `SearchInput` - A variant of `TextField` that is decorated as a search box.
  - Cocoa: `NSSearchField`
  - GTK: `Gtk.Entry`
  - iOS: `UISearchBar`?
  - Winforms: ?
  - Android: ?

### Views

Views are mechanisms for displaying rich content, usually in a read-only manner.

- `VideoView` - Display a video
  - Cocoa: `AVPlayerView`
  - GTK: Custom integration with `GStreamer`
  - iOS: `MPMoviePlayerController`
  - Winforms: ?
  - Android: ?
- `PDFView` - Display a PDF document
  - Cocoa: `PDFView`
  - GTK: ?
  - iOS: Integration with QuickLook?
  - Winforms: ?
  - Android: ?

### Container widgets

Containers are widgets that can contain other widgets.

- `FormContainer` - A layout for a "key/value" or "label/widget" form
  - Cocoa: `NSForm`, or `NSView` with pre-set constraints.
  - GTK:
  - iOS:
  - Winforms: ?
  - Android: ?

- `NavigationContainer` - A container view that holds a navigable tree of sub-views  Essentially a view that has a "back" button to return to the previous view in a hierarchy. Example of use: Top level navigation in the macOS System Preferences panel.
  - Cocoa: No native control
  - GTK: No native control; `Gtk.HeaderBar` in 3.10+
  - iOS: `UINavigationBar` + `NavigationController`
  - Winforms: ?
  - Android: ?

## Other capabilities

One of the aims of Toga is to provide a rich, feature-driven approach to app development. This requires the development of APIs to support rich features.

- **Preferences** - Support for saving app preferences, and visualizing them in a platform native way.
- **Notification** - A mechanism to display popup "toast"-style notifications
- **System tray icons** - Presenting an icon and/or menu in the platform's system tray -possibly without having a main app window at all.
- **Licensing/registration** - Monetization is not a bad thing, and shouldn't be mutually exclusive with open source.
- **Audio** - The ability to play sound files, either once off, or on a loop.
- **Cloud data access** - Traditional apps store all their files locally; however, using cloud services or network resources is increasingly common, especially in mobile apps. However, accessing cloud-based files can be very complicated; Toga is in a position to provide a file-like API that abstracts accessing these APIs.
- **QR code scanning** - The ability to scan QR codes and bar codes in an app, and return the encoded data.

## Platforms

Toga currently has good support for Cocoa on macOS, GTK on Linux, Winforms on Windows, iOS and Android. Proof-of-concept support exists for single page web apps and consoles. Support for a more modern Windows API would be desirable, as would support for Qt.
