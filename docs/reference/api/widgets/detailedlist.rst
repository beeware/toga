DetailedList
============


.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/detailedlist-cocoa.png
       :align: center
       :width: 450px

  .. group-tab:: Linux

    .. figure:: /reference/images/detailedlist-gtk.png
       :align: center
       :width: 450px

  .. group-tab:: Windows |beta|

    .. figure:: /reference/images/detailedlist-winforms.png
       :align: center
       :width: 450px

  .. group-tab:: Android

    .. figure:: /reference/images/detailedlist-android.png
       :align: center
       :width: 450px

  .. group-tab:: iOS

    .. figure:: /reference/images/detailedlist-iOS.png
       :align: center
       :width: 450px

  .. group-tab:: Web |no|

    Not supported

  .. group-tab:: Textual |no|

    Not supported

Usage
-----

The simplest way to create a DetailedList is to pass a list of dictionaries, with
each dictionary containing three keys: ``icon``, ``title``, and ``subtitle``:

.. code-block:: python

    import toga

    table = toga.DetailedList(
        data=[
            {
               "icon": toga.Icon("icons/arthur"),
               "title": "Arthur Dent",
               "subtitle": "Where's the tea?"
            },
            {
               "icon": toga.Icon("icons/ford"),
               "title": "Ford Prefect",
               "subtitle": "Do you know where my towel is?"
            },
            {
               "icon": toga.Icon("icons/tricia"),
               "title": "Tricia McMillan",
               "subtitle": "What planet are you from?"
            },
        ]
    )

If you want to customize the keys used in the dictionary, you can do this by
providing an ``accessors`` argument to the DetailedList when it is constructed.
``accessors`` is a tuple containing the attributes that will be used to provide the
icon, title, and subtitle, respectively:

.. code-block:: python

    import toga

    table = toga.DetailedList(
        accessors=("picture", "name", "quote"),
        data=[
            {
               "picture": toga.Icon("icons/arthur"),
               "name": "Arthur Dent",
               "quote": "Where's the tea?"
            },
            {
               "picture": toga.Icon("icons/ford"),
               "name": "Ford Prefect",
               "quote": "Do you know where my towel is?"
            },
            {
               "picture": toga.Icon("icons/tricia"),
               "name": "Tricia McMillan",
               "quote": "What planet are you from?"
            },
        ]
    )

If the value provided by the title or subtitle accessor is ``None``, or the accessor
isn't defined, the ``missing_value`` will be displayed. Any other value will be
converted into a string.

The icon accessor should return an :any:`Icon`. If it returns ``None``, or the
accessor isn't defined, then no icon will be displayed, but space for the icon will
remain in the layout.

Items in a DetailedList can respond to a primary and secondary action. On platforms that
use swipe interactions, the primary action will be associated with "swipe left", and the
secondary action will be associated with "swipe right". Other platforms may
implement the primary and secondary actions using a different UI interaction (e.g., a
right-click context menu). The primary and secondary actions will only be enabled in
the DetailedList UI if a handler has been provided.

By default, the primary and secondary action will be labeled as "Delete" and "Action",
respectively. These names can be overridden by providing a ``primary_action`` and
``secondary_action`` argument when constructing the DetailedList. Although the primary
action is labeled "Delete" by default, the DetailedList will not perform any data
deletion as part of the UI interaction. It is the responsibility of the application to
implement any data deletion behavior as part of the ``on_primary_action`` handler.

The DetailedList as a whole can also respond to a refresh UI action. This is usually
implemented as a "pull down" action, such as you might see on a social media timeline.
This action will only be enabled in the UI if an ``on_refresh`` handler has been
provided.

Notes
-----

* The iOS Human Interface Guidelines differentiate between "Normal" and "Destructive"
  actions on a row. Toga will interpret any action with a name of "Delete" or "Remove"
  as destructive, and will render the action appropriately.

* The WinForms implementation currently uses a column layout similar to :any:`Table`,
  and does not support the primary, secondary or refresh actions.

Reference
---------

.. autoclass:: toga.DetailedList
