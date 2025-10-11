# API Reference

## Core application components { #api-reference-core }

| Component                           | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| [App](app.md)                       | The top-level representation of an application.                             |
| [Window](window.md)                 | An operating system-managed container of widgets.                           |
| [MainWindow](mainwindow.md)         | A window that can use the full set of window-level user interface elements. |
| [DocumentWindow](documentwindow.md) | A window that can be used as the main interface to a document-based app.    |

## General widgets { #api-reference-general }

| Component                                                          | Description                                                                                                                                                                                |
|--------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [ActivityIndicator](/reference/api/widgets/activityindicator.md)   | A small animated indicator showing activity on a task of indeterminate length, usually rendered as a "spinner" animation.                                                                  |
| [Button](/reference/api/widgets/button.md)                         | A button that can be pressed or clicked.                                                                                                                                                   |
| [Canvas](/reference/api/widgets/canvas.md)                         | A drawing area for 2D vector graphics.                                                                                                                                                     |
| [DateInput](/reference/api/widgets/dateinput.md)                   | A widget to select a calendar date                                                                                                                                                         |
| [DetailedList](/reference/api/widgets/detailedlist.md)             | An ordered list of content where each item has an icon, a main heading, and a line of supplementary text.                                                                                  |
| [Divider](/reference/api/widgets/divider.md)                       | A separator used to visually distinguish two sections of content in a layout.                                                                                                              |
| [ImageView](/reference/api/widgets/imageview.md)                   | Image Viewer                                                                                                                                                                               |
| [Label](/reference/api/widgets/label.md)                           | A text label for annotating forms or interfaces.                                                                                                                                           |
| [MapView](/reference/api/widgets/mapview.md)                       | A zoomable map that can be annotated with location pins.                                                                                                                                   |
| [MultilineTextInput](/reference/api/widgets/multilinetextinput.md) | A scrollable panel that allows for the display and editing of multiple lines of text.                                                                                                      |
| [NumberInput](/reference/api/widgets/numberinput.md)               | A text input that is limited to numeric input.                                                                                                                                             |
| [PasswordInput](/reference/api/widgets/passwordinput.md)           | A widget to allow the entry of a password. Any value typed by the user will be obscured, allowing the user to see the number of characters they have typed, but not the actual characters. |
| [ProgressBar](/reference/api/widgets/progressbar.md)               | A horizontal bar to visualize task progress. The task being monitored can be of known or indeterminate length.                                                                             |
| [Selection](/reference/api/widgets/selection.md)                   | A widget to select an single option from a list of alternatives.                                                                                                                           |
| [Slider](/reference/api/widgets/slider.md)                         | A widget for selecting a value within a range. The range is shown as a horizontal line, and the selected value is shown as a draggable marker.                                             |
| [Switch](/reference/api/widgets/switch.md)                         | A clickable button with two stable states: True (on, checked); and False (off, unchecked). The button has a text label.                                                                    |
| [Table](/reference/api/widgets/table.md)                           | A widget for displaying columns of tabular data.                                                                                                                                           |
| [TextInput](/reference/api/widgets/textinput.md)                   | A widget for the display and editing of a single line of text.                                                                                                                             |
| [TimeInput](/reference/api/widgets/timeinput.md)                   | A widget to select a clock time                                                                                                                                                            |
| [Tree](/reference/api/widgets/tree.md)                             | A widget for displaying a hierarchical tree of tabular data.                                                                                                                               |
| [WebView](/reference/api/widgets/webview.md)                       | An embedded web browser.                                                                                                                                                                   |
| [Widget](/reference/api/widgets/widget.md)                         | The abstract base class of all widgets. This class should not be be instantiated directly.                                                                                                 |

## Layout widgets { #api-reference-layout }

| Component                                                       | Description                                                                                                           |
|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [Box](/reference/api/containers/box.md)                         | A generic container for other widgets. Used to construct layouts.                                                     |
| [OptionContainer](/reference/api/containers/optioncontainer.md) | A container that can display multiple labeled tabs of content.                                                        |
| [ScrollContainer](/reference/api/containers/scrollcontainer.md) | A container that can display a layout larger that the area of the container, with overflow controlled by scroll bars. |
| [SplitContainer](/reference/api/containers/splitcontainer.md)   | A container that divides an area into two panels with a movable border.                                               |

## Resources { #api-reference-resources }

| Component                                                       | Description                                                                                   |
|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| [App Paths](/reference/api/resources/app_paths.md)              | A mechanism for obtaining platform-appropriate file system locations for an application.      |
| [Command](/reference/api/resources/command.md)                  | A representation of app functionality that the user can invoke from menus or toolbars.        |
| [Dialogs](/reference/api/resources/dialogs.md)                  | A short-lived window asking the user for input.                                               |
| [Document](/reference/api/resources/document.md)                | A representation of a file on disk that will be displayed in one or more windows              |
| [Font](/reference/api/resources/fonts.md)                       | A representation of a Font                                                                    |
| [Icon](/reference/api/resources/icons.md)                       | An icon for buttons, menus, etc                                                               |
| [Image](/reference/api/resources/images.md)                     | An image                                                                                      |
| [Source](/reference/api/resources/sources/source.md)            | A base class for data source implementations.                                                 |
| [Status Icons](/reference/api/resources/statusicons.md)         | Icons that appear in the system tray for representing app status while the app isn't visible. |
| [ListSource](/reference/api/resources/sources/list_source.md)   | A data source describing an ordered list of data.                                             |
| [TreeSource](/reference/api/resources/sources/tree_source.md)   | A data source describing an ordered hierarchical tree of data.                                |
| [ValueSource](/reference/api/resources/sources/value_source.md) | A data source describing a single value.                                                      |
| [Validators](/reference/api/resources/validators.md)            | A mechanism for validating that input meets a given set of criteria.                          |

## Hardware { #api-reference-hardware }

| Usage                                           | Description                                                        |
|-------------------------------------------------|--------------------------------------------------------------------|
| [Camera](/reference/api/hardware/camera.md)     | A sensor that can capture photos and/or video.                     |
| [Location](/reference/api/hardware/location.md) | A sensor that can capture the geographical location of the device. |
| [Screen](/reference/api/hardware/screens.md)    | A representation of a screen attached to a device.                 |

## Other { #api-reference-other }

| Component                                | Description                                                  |
|------------------------------------------|--------------------------------------------------------------|
| [Constants](/reference/api/constants.md) | Symbolic constants used by various APIs.                     |
| [Keys](/reference/api/keys.md)           | Symbolic representation of keys used for keyboard shortcuts. |
| [Types](/reference/api/types.md)         | Utility data structures used by Toga APIs.                   |
