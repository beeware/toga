.. _layout:

===========================
Understanding widget layout
===========================

One of the major tasks of a GUI framework is to determine where each widget will be displayed within the application window. This determination must be made when a window is initially displayed, and every time the window changes size (or, on mobile devices, changes orientation).

Layout in Toga is performed using style engine. Toga provides a :doc:`built-in style engine called Pack </reference/style/pack>`; however, other style engines can be used. Every widget keeps a style object, and it is this style object that is used to perform layout operations.

Each widget can also report an "intrinsic" size - this is the size of the widget, as reported by the underlying GUI library. The intrinsic size is a width and height; each dimension can be fixed, or specified as a minimum. For example, a button may have a fixed intrinsic height, but a minimum intrinsic width (indicating that there is a minimum size the button can be, but it can stretch to assume any larger size). This intrinsic size is computed when the widget is first displayed; if fundamental properties of the widget ever change (e.g., changing the text or font size on a button), the widget needs to be rehinted, which re-calculates the intrinsic size, and invalidates any layout.

Widgets are constructed in a tree structure. The widget at the root of the tree is called the *container* widget. Every widget keeps a reference to the container at the root of its widget tree.

When a widget is added to a window, a *Viewport* is created. This viewport connects the widget to the available space provided by the window.

When a window needs to perform a layout, the layout engine asks the style object for the container to lay out its contents with the space that the viewport has available. This will perform whatever calculations are required and apply any position information to the widgets in the widget tree.

Every window has a container and viewport, representing the total viewable area of the window. However, some widgets (called Container widgets) establish sub-containers. When a refresh is requested on a container, any sub-containers will also be refreshed.
