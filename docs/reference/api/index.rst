.. _api-reference:

==============
API Reference
==============

Core application components
---------------------------

======================================================= =============================================================================
 Component                                                       Description
======================================================= =============================================================================
 :doc:`App </reference/api/app>`                         The top-level representation of an application.
 :doc:`Window </reference/api/window>`                   An operating system-managed container of widgets.
 :doc:`MainWindow </reference/api/mainwindow>`           A window that can use the full set of window-level user interface elements.
 :doc:`DocumentWindow </reference/api/documentwindow>`   A window that can be used as the main interface to a document-based app.
======================================================= =============================================================================

General widgets
---------------

======================================================================= ========================================================================
 Component                                                               Description
======================================================================= ========================================================================
 :doc:`ActivityIndicator </reference/api/widgets/activityindicator>`     A small animated indicator showing activity on a task of indeterminate
                                                                         length, usually rendered as a "spinner" animation.
 :doc:`Button </reference/api/widgets/button>`                           A button that can be pressed or clicked.
 :doc:`Canvas </reference/api/widgets/canvas>`                           A drawing area for 2D vector graphics.
 :doc:`DateInput </reference/api/widgets/dateinput>`                     A widget to select a calendar date
 :doc:`DetailedList </reference/api/widgets/detailedlist>`               An ordered list of content where each item has an icon, a main heading,
                                                                         and a line of supplementary text.
 :doc:`Divider </reference/api/widgets/divider>`                         A separator used to visually distinguish two sections of content in a
                                                                         layout.
 :doc:`ImageView </reference/api/widgets/imageview>`                     Image Viewer
 :doc:`Label </reference/api/widgets/label>`                             A text label for annotating forms or interfaces.
 :doc:`MapView </reference/api/widgets/mapview>`                         A zoomable map that can be annotated with location pins.
 :doc:`MultilineTextInput </reference/api/widgets/multilinetextinput>`   A scrollable panel that allows for the display and editing of multiple
                                                                         lines of text.
 :doc:`NumberInput </reference/api/widgets/numberinput>`                 A text input that is limited to numeric input.
 :doc:`PasswordInput </reference/api/widgets/passwordinput>`             A widget to allow the entry of a password. Any value typed by the
                                                                         user will be obscured, allowing the user to see the number of
                                                                         characters they have typed, but not the actual characters.
 :doc:`ProgressBar </reference/api/widgets/progressbar>`                 A horizontal bar to visualize task progress. The task being monitored
                                                                         can be of known or indeterminate length.
 :doc:`Selection </reference/api/widgets/selection>`                     A widget to select a single option from a list of alternatives.
 :doc:`Slider </reference/api/widgets/slider>`                           A widget for selecting a value within a range. The range is shown as a
                                                                         horizontal line, and the selected value is shown as a draggable marker.
 :doc:`Switch </reference/api/widgets/switch>`                           A clickable button with two stable states: True (on, checked); and
                                                                         False (off, unchecked). The button has a text label.
 :doc:`Table </reference/api/widgets/table>`                             A widget for displaying columns of tabular data.
 :doc:`TextInput </reference/api/widgets/textinput>`                     A widget for the display and editing of a single line of text.
 :doc:`TimeInput </reference/api/widgets/timeinput>`                     A widget to select a clock time
 :doc:`Tree </reference/api/widgets/tree>`                               A widget for displaying a hierarchical tree of tabular data.
 :doc:`WebView </reference/api/widgets/webview>`                         An embedded web browser.
 :doc:`Widget </reference/api/widgets/widget>`                           The abstract base class of all widgets. This class should not be be
                                                                         instantiated directly.
======================================================================= ========================================================================

Layout widgets
--------------

==================================================================== ========================================================================
 Usage                                                                Description
==================================================================== ========================================================================
 :doc:`Box </reference/api/containers/box>`                           A generic container for other widgets. Used to construct layouts.
 :doc:`ScrollContainer </reference/api/containers/scrollcontainer>`   A container that can display a layout larger that the area of
                                                                      the container, with overflow controlled by scroll bars.
 :doc:`SplitContainer </reference/api/containers/splitcontainer>`     A container that divides an area into two panels with a movable
                                                                      border.
 :doc:`OptionContainer </reference/api/containers/optioncontainer>`   A container that can display multiple labeled tabs of content.
==================================================================== ========================================================================

Resources
---------

==================================================================== ========================================================================
 Component                                                            Description
==================================================================== ========================================================================
 :doc:`App Paths </reference/api/resources/app_paths>`                A mechanism for obtaining platform-appropriate file system locations
                                                                      for an application.
 :doc:`Command </reference/api/resources/command>`                    A representation of app functionality that the user can invoke from
                                                                      menus or toolbars.
 :doc:`Dialogs </reference/api/resources/dialogs>`                    A short-lived window asking the user for input.
 :doc:`Document </reference/api/resources/document>`                  A representation of a file on disk that will be displayed in one or
                                                                      more windows
 :doc:`Font </reference/api/resources/fonts>`                         A representation of a Font
 :doc:`Icon </reference/api/resources/icons>`                         An icon for buttons, menus, etc
 :doc:`Image </reference/api/resources/images>`                       An image
 :doc:`Source </reference/api/resources/sources/source>`              A base class for data source implementations.
 :doc:`Status Icons </reference/api/resources/statusicons>`           Icons that appear in the system tray for representing app status
                                                                      while the app isn't visible.
 :doc:`ListSource </reference/api/resources/sources/list_source>`     A data source describing an ordered list of data.
 :doc:`TreeSource </reference/api/resources/sources/tree_source>`     A data source describing an ordered hierarchical tree of data.
 :doc:`ValueSource </reference/api/resources/sources/value_source>`   A data source describing a single value.
 :doc:`Validators </reference/api/resources/validators>`              A mechanism for validating that input meets a given set of criteria.
==================================================================== ========================================================================

Hardware
--------

==================================================================== ========================================================================
 Usage                                                                Description
==================================================================== ========================================================================
 :doc:`Camera </reference/api/hardware/camera>`                       A sensor that can capture photos and/or video.
 :doc:`Location </reference/api/hardware/location>`                   A sensor that can capture the geographical location of the device.
 :doc:`Screen </reference/api/hardware/screens>`                      A representation of a screen attached to a device.
==================================================================== ========================================================================

Other
-----

============================================== ========================================================================
 Component                                      Description
============================================== ========================================================================
 :doc:`Constants </reference/api/constants>`    Symbolic constants used by various APIs.
 :doc:`Keys </reference/api/keys>`              Symbolic representation of keys used for keyboard shortcuts.
 :doc:`Types </reference/api/types>`            Utility data structures used by Toga APIs.
============================================== ========================================================================

.. toctree::
   :hidden:

   app
   window
   mainwindow
   documentwindow
   containers/index
   hardware/index
   resources/index
   widgets/index
   constants
   keys
   types
