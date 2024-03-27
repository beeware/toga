.. _layout:

=============
Widget layout
=============

One of the major tasks of a GUI framework is to determine where each widget will be displayed within the application window. This determination must be made when a window is initially displayed, and every time the window changes size (or, on mobile devices, changes orientation).

Layout in Toga is performed using style engine. Toga provides a :doc:`built-in style engine called Pack </reference/style/pack>`; however, other style engines can be used. Every widget keeps a style object, and it is this style object that is used to perform layout operations.

Each widget can also report an "intrinsic" size - this is the size of the widget, as reported by the underlying GUI library. The intrinsic size is a width and height; each dimension can be fixed, or specified as a minimum. For example, a button may have a fixed intrinsic height, but a minimum intrinsic width (indicating that there is a minimum size the button can be, but it can stretch to assume any larger size). This intrinsic size is computed when the widget is first displayed; if fundamental properties of the widget ever change (e.g., changing the text or font size on a button), the widget needs to be rehinted, which re-calculates the intrinsic size, and invalidates any layout.

Widgets are constructed in a tree structure. The widget at the root of the tree is called the *container* widget. Every widget keeps a reference to the container at the root of its widget tree.

When a window needs to perform a layout, the layout engine asks the style object for the
container to lay out its contents within the space that the container has available.
This will calculate a size and position for all the widgets in the tree.

Every window has a container representing the total viewable area of the window.
However, some widgets (those with "Container" in their name) establish sub-containers.
When a refresh is requested on a container, any sub-containers will also be refreshed.


.. _css-units:

Length units
============

Toga uses CSS units in its public API. Their physical size depends on the device type:

* A CSS pixel is about 1/96 of an inch (0.26 mm) on a desktop screen, and about 1/160 of
  an inch (0.16 mm) on a phone screen.

* A CSS point is 1.33 CSS pixels.

Toga only uses points to measure font sizes. All other lengths are expressed as pixels.

For a full explanation of CSS units, see `this article
<https://hacks.mozilla.org/2013/09/css-length-explained/>`__.

Implementation notes
~~~~~~~~~~~~~~~~~~~~

* On macOS and iOS, one CSS pixel equals one `"point"
  <https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Explained/Explained.html>`__,
  which is 1, 2 or 3 linear physical pixels, depending on the device.

* On Windows, one CSS pixel equals one physical pixel at `100% scale
  <https://support.microsoft.com/en-us/windows/view-display-settings-in-windows-37f0e05e-98a9-474c-317a-e85422daa8bb>`__,
  and is adjusted as necessary at higher scale factors.

* On Android, one CSS pixel equals one `dp
  <https://developer.android.com/training/multiscreen/screendensities#TaskUseDP>`__.
