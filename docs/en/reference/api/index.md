# API Reference

## Core application components

| Component                           | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| [App](app.md)                       | The top-level representation of an application.                             |
| [Window](window.md)                 | An operating system-managed container of widgets.                           |
| [MainWindow](mainwindow.md)         | A window that can use the full set of window-level user interface elements. |
| [DocumentWindow](documentwindow.md) | A window that can be used as the main interface to a document-based app.    |


## General widgets

| Component                                                            | Description                                                                                                                                                                                  |
|----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ActivityIndicator &lt;/reference/api/widgets/activityindicator&gt;   | A small animated indicator showing activity on a task of indeterminate length, usually rendered as a "spinner" animation.                                                                    |
| Button &lt;/reference/api/widgets/button&gt;                         | A button that can be pressed or clicked.                                                                                                                                                     |
| Canvas &lt;/reference/api/widgets/canvas&gt;                         | A drawing area for 2D vector graphics.                                                                                                                                                       |
| DateInput &lt;/reference/api/widgets/dateinput&gt;                   | A widget to select a calendar date                                                                                                                                                           |
| DetailedList &lt;/reference/api/widgets/detailedlist&gt;             | An ordered list of content where each item has an icon, a main heading, and a line of supplementary text.                                                                                    |
| Divider &lt;/reference/api/widgets/divider&gt;                       | A separator used to visually distinguish two sections of content in a layout.                                                                                                                |
| ImageView &lt;/reference/api/widgets/imageview&gt;                   | Image Viewer                                                                                                                                                                                 |
| Label &lt;/reference/api/widgets/label&gt;                           | A text label for annotating forms or interfaces.                                                                                                                                             |
| MapView &lt;/reference/api/widgets/mapview&gt;                       | A zoomable map that can be annotated with location pins.                                                                                                                                     |
| MultilineTextInput &lt;/reference/api/widgets/multilinetextinput&gt; | A scrollable panel that allows for the display and editing of multiple lines of text.                                                                                                        |
| NumberInput &lt;/reference/api/widgets/numberinput&gt;               | A text input that is limited to numeric input.                                                                                                                                               |
| PasswordInput &lt;/reference/api/widgets/passwordinput&gt;           | A widget to allow the entry of a password. Any value typed by the user will be obscured, allowing the user to see the number of characters  sthey have typed, but not the actual characters. |
| ProgressBar &lt;/reference/api/widgets/progressbar&gt;               | A horizontal bar to visualize task progress. The task being monitored can be of known or indeterminate length.                                                                               |
| Selection &lt;/reference/api/widgets/selection&gt;                   | A widget to select an single option from a list of alternatives.                                                                                                                             |
| Slider &lt;/reference/api/widgets/slider&gt;                         | A widget for selecting a value within a range. The range is shown asa horizontal line, and the selected value is shown as a draggablemarker.                                                 |
| Switch &lt;/reference/api/widgets/switch&gt;                         | A clickable button with two stable states: True (on, checked); andFalse (off, unchecked). The button has a text label.                                                                       |
| Table &lt;/reference/api/widgets/table&gt;                           | A widget for displaying columns of tabular data.                                                                                                                                             |
| TextInput &lt;/reference/api/widgets/textinput&gt;                   | A widget for the display and editing of a single line of text.                                                                                                                               |
| TimeInput &lt;/reference/api/widgets/timeinput&gt;                   | A widget to select a clock time                                                                                                                                                              |
| Tree &lt;/reference/api/widgets/tree&gt;                             | A widget for displaying a hierarchical tree of tabular data.                                                                                                                                 |
| WebView &lt;/reference/api/widgets/webview&gt;                       | An embedded web browser.                                                                                                                                                                     |
| Widget &lt;/reference/api/widgets/widget&gt;                         | The abstract base class of all widgets. This class should not be be instantiated directly.                                                                                                   |


## Layout widgets

| Component                                                            | Description                                                                                                                                                                                |
|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ActivityIndicator &lt;/reference/api/widgets/activityindicator&gt;   | A small animated indicator showing activity on a task of indeterminate length, usually rendered as a "spinner" animation.                                                                  |
| Button &lt;/reference/api/widgets/button&gt;                         | A button that can be pressed or clicked.                                                                                                                                                   |
| Canvas &lt;/reference/api/widgets/canvas&gt;                         | A drawing area for 2D vector graphics.                                                                                                                                                     |
| DateInput &lt;/reference/api/widgets/dateinput&gt;                   | A widget to select a calendar date                                                                                                                                                         |
| DetailedList &lt;/reference/api/widgets/detailedlist&gt;             | An ordered list of content where each item has an icon, a main heading, and a line of supplementary text.                                                                                  |
| Divider &lt;/reference/api/widgets/divider&gt;                       | A separator used to visually distinguish two sections of content in a layout.                                                                                                              |
| ImageView &lt;/reference/api/widgets/imageview&gt;                   | Image Viewer                                                                                                                                                                               |
| Label &lt;/reference/api/widgets/label&gt;                           | A text label for annotating forms or interfaces.                                                                                                                                           |
| MapView &lt;/reference/api/widgets/mapview&gt;                       | A zoomable map that can be annotated with location pins.                                                                                                                                   |
| MultilineTextInput &lt;/reference/api/widgets/multilinetextinput&gt; | A scrollable panel that allows for the display and editing of multiple lines of text.                                                                                                      |
| NumberInput &lt;/reference/api/widgets/numberinput&gt;               | A text input that is limited to numeric input.                                                                                                                                             |
| PasswordInput &lt;/reference/api/widgets/passwordinput&gt;           | A widget to allow the entry of a password. Any value typed by the user will be obscured, allowing the user to see the number of characters they have typed, but not the actual characters. |
| ProgressBar &lt;/reference/api/widgets/progressbar&gt;               | A horizontal bar to visualize task progress. The task being monitored can be of known or indeterminate length.                                                                             |
| Selection &lt;/reference/api/widgets/selection&gt;                   | A widget to select a single option from a list of alternatives.                                                                                                                            |
| Slider &lt;/reference/api/widgets/slider&gt;                         | A widget for selecting a value within a range. The range is shown asa horizontal line, and the selected value is shown as a draggable marker.                                              |
| Switch &lt;/reference/api/widgets/switch&gt;                         | A clickable button with two stable states: True (on, checked); andFalse (off, unchecked). The button has a text label.                                                                     |
| Table &lt;/reference/api/widgets/table&gt;                           | A widget for displaying columns of tabular data.                                                                                                                                           |
| TextInput &lt;/reference/api/widgets/textinput&gt;                   | A widget for the display and editing of a single line of text.                                                                                                                             |
| TimeInput &lt;/reference/api/widgets/timeinput&gt;                   | A widget to select a clock time                                                                                                                                                            |
| Tree &lt;/reference/api/widgets/tree&gt;                             | A widget for displaying a hierarchical tree of tabular data.                                                                                                                               |
| WebView &lt;/reference/api/widgets/webview&gt;                       | An embedded web browser.                                                                                                                                                                   |
| Widget &lt;/reference/api/widgets/widget&gt;                         | The abstract base class of all widgets. This class should not be be instantiated directly.                                                                                                 |


## Resources

| Component                                                         | Description                                                                                   |
|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| App Paths &lt;/reference/api/resources/app_paths&gt;              | A mechanism for obtaining platform-appropriate file system locations for an application.      |
| Command &lt;/reference/api/resources/command&gt;                  | A representation of app functionality that the user can invoke from menus or toolbars.        |
| Dialogs &lt;/reference/api/resources/dialogs&gt;                  | A short-lived window asking the user for input.                                               |
| Document &lt;/reference/api/resources/document&gt;                | A representation of a file on disk that will be displayed in one or more windows              |
| Font &lt;/reference/api/resources/fonts&gt;                       | A representation of a Font                                                                    |
| Icon &lt;/reference/api/resources/icons&gt;                       | An icon for buttons, menus, etc                                                               |
| Image &lt;/reference/api/resources/images&gt;                     | An image                                                                                      |
| Source &lt;/reference/api/resources/sources/source&gt;            | A base class for data source implementations.                                                 |
| Status Icons &lt;/reference/api/resources/statusicons&gt;         | Icons that appear in the system tray for representing app status while the app isn't visible. |
| ListSource &lt;/reference/api/resources/sources/list_source&gt;   | A data source describing an ordered list of data.                                             |
| TreeSource &lt;/reference/api/resources/sources/tree_source&gt;   | A data source describing an ordered hierarchical tree of data.                                |
| ValueSource &lt;/reference/api/resources/sources/value_source&gt; | A data source describing a single value.                                                      |
| Validators &lt;/reference/api/resources/validators&gt;            | A mechanism for validating that input meets a given set of criteria.                          |


## Hardware

| Usage                                             | Description                                                        |
|---------------------------------------------------|--------------------------------------------------------------------|
| Camera &lt;/reference/api/hardware/camera&gt;     | A sensor that can capture photos and/or video.                     |
| Location &lt;/reference/api/hardware/location&gt; | A sensor that can capture the geographical location of the device. |
| Screen &lt;/reference/api/hardware/screens&gt;    | A representation of a screen attached to a device.                 |


## Other

| Component                                  | Description                                                  |
|--------------------------------------------|--------------------------------------------------------------|
| Constants &lt;/reference/api/constants&gt; | Symbolic constants used by various APIs.                     |
| Keys &lt;/reference/api/keys&gt;           | Symbolic representation of keys used for keyboard shortcuts. |
| Types &lt;/reference/api/types&gt;         | Utility data structures used by Toga APIs.                   |
