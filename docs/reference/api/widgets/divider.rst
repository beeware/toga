Divider
=======

A separator used to visually distinguish two sections of content in a layout.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/divider-cocoa.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/divider-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/divider-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/divider-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS |no|

    Not supported

  .. group-tab:: Web |beta|

    .. .. figure:: /reference/images/divider-web.png
    ..    :align: center
    ..    :width: 300px

    Screenshot not available

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

To separate two labels stacked vertically with a horizontal line:

.. code-block:: python

    import toga
    from toga.style.pack import Pack, COLUMN

    box = toga.Box(
        children=[
            toga.Label("First section"),
            toga.Divider(),
            toga.Label("Second section"),
        ],
        style=Pack(direction=COLUMN, flex=1, padding=10)
    )

The direction (horizontal or vertical) can be given as an argument. If not
specified, it will default to horizontal.

Reference
---------

.. autoclass:: toga.Divider
