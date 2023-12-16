OptionContainer
===============

A container that can display multiple labeled tabs of content.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/optioncontainer-cocoa.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/optioncontainer-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows

    .. figure:: /reference/images/optioncontainer-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android |no|

    Not supported

  .. group-tab:: iOS

    .. figure:: /reference/images/optioncontainer-iOS.png
       :align: center
       :width: 450px

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

The content of an OptionContainer is a list of widgets that will form discrete tabs in
the display. Each tab can be identified by a label, and, optionally, an icon. This list
of content can be modified after initial construction:

.. code-block:: python

    import toga

    pizza = toga.Box()
    pasta = toga.Box()

    # Create 2 initial tabs; one with an icon, and one without.
    container = toga.OptionContainer(
        content=[("Pizza", pizza), ("Pasta", pasta, toga.Icon("pasta"))]
    )

    # Add another tab of content, without an icon.
    salad = toga.Box()
    container.content.append("Salad", salad)

    # Add another tab of content, with an icon
    icecream = toga.Box()
    container.content.append("Ice Cream", icecream, toga.Icon("icecream"))

OptionContainer content can also be specified by using :any:`OptionItem` instances
instead of tuples. This enables you to be explicit when setting an icon or enabled
status; it also allows you to set the initial enabled status *without* setting an icon:

.. code-block:: python

    import toga

    pizza = toga.Box()
    pasta = toga.Box()

    # Create 2 initial tabs; one with an icon, and one without.
    container = toga.OptionContainer(
        content=[
          toga.OptionItem("Pizza", pizza),
          toga.OptionItem("Pasta", pasta, icon=toga.Icon("pasta"))
        ]
    )

    # Add another tab of content, initially disabled, without an icon.
    salad = toga.Box()
    container.content.append(toga.OptionItem("Salad", salad, enabled=False))


When retrieving or deleting items, or when specifying the currently selected
item, you can specify an item using:

* The index of the item in the list of content:

  .. code-block:: python

      # Insert a new second tab
      container.content.insert(1, "Soup", toga.Box())
      # Make the third tab the currently active tab
      container.current_tab = 2
      # Delete the second tab
      del container.content[1]

* The string label of the tab:

  .. code-block:: python

      # Insert a tab at the index currently occupied by a tab labeled "Pasta"
      container.content.insert("Pasta", "Soup", toga.Box())
      # Make the tab labeled "Pasta" the currently active tab
      container.current_tab = "Pasta"
      # Delete tab labeled "Pasta"
      del container.content["Pasta"]

* A reference to an :any:`OptionItem`:

  .. code-block:: python

      # Get a reference to the "Pasta" tab
      pasta_tab = container.content["Pasta"]
      # Insert content at the index currently occupied by the pasta tab
      container.content.insert(pasta_tab, "Soup", toga.Box())
      # Make the pasta tab the currently active tab
      container.current_tab = pasta_tab
      # Delete the pasta tab
      del container.content[pasta_tab]

Notes
-----

* The use of icons on tabs varies between platforms. If the platform requires icons, and
  no icon is provided, a default icon will be used. If the platform does not support
  icons, any icon provided will be ignored, and requests to retrieve the icon will
  return ``None``.

* The behavior of disabled tabs varies between platforms. Some platforms will display
  the tab, but put it in an unselectable state; some will hide the tab. A hidden tab can
  still be referenced by index - the tab index refers to the logical order, not the
  visible order.

* iOS can only display 5 tabs. If there are more than 5 visible tabs in an
  OptionContainer, the last item will be converted into a "More" option that will allow
  the user to select the additional items. While the "More" menu is displayed, the
  current tab will return as ``None``.

* iOS allows the user to rearrange icons on an OptionContainer. When referring to tabs
  by index, user re-ordering is ignored; the logical order as configured in Toga itself
  is used to identify tabs.

* Icons for iOS OptionContainer tabs should be 25x25px alpha masks.

Reference
---------

.. c:type:: OptionContainerContent

    An item of :any:`OptionContainer` content can be:

    * a 2-tuple, containing the title for the tab, and the content widget;
    * a 3-tuple, containing the title, content widget, and :any:`icon <IconContent>`
      for the tab;
    * a 4-tuple, containing the title, content widget, :any:`icon <IconContent>` for
      the tab, and enabled status; or
    * an :any:`OptionItem` instance.

.. autoclass:: toga.OptionContainer
   :exclude-members: app, window

.. autoclass:: toga.OptionItem

.. autoclass:: toga.widgets.optioncontainer.OptionList
    :special-members: __getitem__, __delitem__

.. autoprotocol:: toga.widgets.optioncontainer.OnSelectHandler
