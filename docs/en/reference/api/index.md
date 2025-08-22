# API Reference

## Core application components

<table>
<thead>
<tr>
<th>Component</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">App &lt;/reference/api/app&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>The top-level representation of an application.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Window &lt;/reference/api/window&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>An operating system-managed container of widgets.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">MainWindow &lt;/reference/api/mainwindow&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A window that can use the full set of window-level user interface
elements.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">DocumentWindow &lt;/reference/api/documentwindow&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A window that can be used as the main interface to a document-based
app.</p>
</blockquote></td>
</tr>
</tbody>
</table>

## General widgets

<table>
<thead>
<tr>
<th>Component</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">ActivityIndicator &lt;/reference/api/widgets/activityindicator&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A small animated indicator showing activity on a task of
indeterminate length, usually rendered as a "spinner" animation.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Button &lt;/reference/api/widgets/button&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A button that can be pressed or clicked.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Canvas &lt;/reference/api/widgets/canvas&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A drawing area for 2D vector graphics.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">DateInput &lt;/reference/api/widgets/dateinput&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget to select a calendar date</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">DetailedList &lt;/reference/api/widgets/detailedlist&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>An ordered list of content where each item has an icon, a main
heading, and a line of supplementary text.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Divider &lt;/reference/api/widgets/divider&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A separator used to visually distinguish two sections of content in a
layout.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">ImageView &lt;/reference/api/widgets/imageview&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>Image Viewer</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Label &lt;/reference/api/widgets/label&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A text label for annotating forms or interfaces.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">MapView &lt;/reference/api/widgets/mapview&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A zoomable map that can be annotated with location pins.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">MultilineTextInput &lt;/reference/api/widgets/multilinetextinput&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A scrollable panel that allows for the display and editing of
multiple lines of text.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">NumberInput &lt;/reference/api/widgets/numberinput&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A text input that is limited to numeric input.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">PasswordInput &lt;/reference/api/widgets/passwordinput&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget to allow the entry of a password. Any value typed by the
user will be obscured, allowing the user to see the number of characters
they have typed, but not the actual characters.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">ProgressBar &lt;/reference/api/widgets/progressbar&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A horizontal bar to visualize task progress. The task being monitored
can be of known or indeterminate length.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Selection &lt;/reference/api/widgets/selection&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget to select an single option from a list of alternatives.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Slider &lt;/reference/api/widgets/slider&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget for selecting a value within a range. The range is shown as
a horizontal line, and the selected value is shown as a draggable
marker.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Switch &lt;/reference/api/widgets/switch&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A clickable button with two stable states: True (on, checked); and
False (off, unchecked). The button has a text label.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Table &lt;/reference/api/widgets/table&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget for displaying columns of tabular data.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">TextInput &lt;/reference/api/widgets/textinput&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget for the display and editing of a single line of text.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">TimeInput &lt;/reference/api/widgets/timeinput&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget to select a clock time</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Tree &lt;/reference/api/widgets/tree&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A widget for displaying a hierarchical tree of tabular data.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">WebView &lt;/reference/api/widgets/webview&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>An embedded web browser.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Widget &lt;/reference/api/widgets/widget&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>The abstract base class of all widgets. This class should not be be
instantiated directly.</p>
</blockquote></td>
</tr>
</tbody>
</table>

## Layout widgets

<table>
<thead>
<tr>
<th>Usage</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Box &lt;/reference/api/containers/box&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A generic container for other widgets. Used to construct layouts.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">ScrollContainer &lt;/reference/api/containers/scrollcontainer&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A container that can display a layout larger that the area of the
container, with overflow controlled by scroll bars.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">SplitContainer &lt;/reference/api/containers/splitcontainer&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A container that divides an area into two panels with a movable
border.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">OptionContainer &lt;/reference/api/containers/optioncontainer&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A container that can display multiple labeled tabs of content.</p>
</blockquote></td>
</tr>
</tbody>
</table>

## Resources

<table>
<thead>
<tr>
<th>Component</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">App Paths &lt;/reference/api/resources/app_paths&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A mechanism for obtaining platform-appropriate file system locations
for an application.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Command &lt;/reference/api/resources/command&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A representation of app functionality that the user can invoke from
menus or toolbars.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Dialogs &lt;/reference/api/resources/dialogs&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A short-lived window asking the user for input.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Document &lt;/reference/api/resources/document&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A representation of a file on disk that will be displayed in one or
more windows</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Font &lt;/reference/api/resources/fonts&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A representation of a Font</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Icon &lt;/reference/api/resources/icons&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>An icon for buttons, menus, etc</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Image &lt;/reference/api/resources/images&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>An image</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Source &lt;/reference/api/resources/sources/source&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A base class for data source implementations.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Status Icons &lt;/reference/api/resources/statusicons&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>Icons that appear in the system tray for representing app status
while the app isn't visible.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">ListSource &lt;/reference/api/resources/sources/list_source&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A data source describing an ordered list of data.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">TreeSource &lt;/reference/api/resources/sources/tree_source&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A data source describing an ordered hierarchical tree of data.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">ValueSource &lt;/reference/api/resources/sources/value_source&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A data source describing a single value.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Validators &lt;/reference/api/resources/validators&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A mechanism for validating that input meets a given set of
criteria.</p>
</blockquote></td>
</tr>
</tbody>
</table>

## Hardware

<table>
<thead>
<tr>
<th>Usage</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Camera &lt;/reference/api/hardware/camera&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A sensor that can capture photos and/or video.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Location &lt;/reference/api/hardware/location&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A sensor that can capture the geographical location of the
device.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Screen &lt;/reference/api/hardware/screens&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>A representation of a screen attached to a device.</p>
</blockquote></td>
</tr>
</tbody>
</table>

## Other

<table>
<thead>
<tr>
<th>Component</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Constants &lt;/reference/api/constants&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>Symbolic constants used by various APIs.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Keys &lt;/reference/api/keys&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>Symbolic representation of keys used for keyboard shortcuts.</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p><code class="interpreted-text"
role="doc">Types &lt;/reference/api/types&gt;</code></p>
</blockquote></td>
<td><blockquote>
<p>Utility data structures used by Toga APIs.</p>
</blockquote></td>
</tr>
</tbody>
</table>

::: {.toctree hidden=""}
app window mainwindow documentwindow containers/index hardware/index
resources/index widgets/index constants keys types
:::
