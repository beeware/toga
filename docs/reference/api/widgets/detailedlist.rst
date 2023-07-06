DetailedList
============

An ordered list of content where each item has an icon, a main heading, and a line of
supplementary text.

.. figure:: /reference/images/DetailedList.png
   :width: 300px
   :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(DetailedList|Component))'}

Usage
-----

A DetailedList uses a :class:`~toga.sources.ListSource` to manage the data being
displayed. options. If ``data`` is not specified as a ListSource, it will be converted
into a ListSource at runtime. Each item in the data source is required to provide 3
values - an icon, a title, and a subtitle.

The simplest instantiation of a DetailedList is to use a list of dictionaries, with
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

If you want to customize the data keys used to provide data, you can do this by
providing an ``accessors`` argument to the DetailedList when it is constructed.
``accessors`` is a tuple, containing the attribute that will be used to provide the
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

If the value provided by the accessor for title or subtitle is :any:`None`, or the
accessor isn't defined, the value of ``missing_value`` provided when constructing the
DetailedList will be used to populate the title and subtitle. Any other value will be
converted into a string.

If the value provided by the accessor for icon is :any:`None`, or the accessor isn't
defined, a no icon will be displayed, but space for the icon will remain the the layout.

Items in a DetailedList can respond to a primary and secondary action. On platforms that
support swipe interactions, the primary action will be associated with "swipe left"; the
secondary action will be associated with "swipe right". However, a platform may
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
implemented as a "pull down to refresh" action, such as you might see on a social media
timeline. If a DetailedList widget provides an ``on_refresh`` handler, the DetailedList
will respond to the refresh UI action, and the ``on_refresh`` handler will be invoked.
If no ``on_refresh`` handler is provided, the DetailedList will behave as a static list,
and will *not* respond to the refresh UI action.

Notes
-----

* The iOS Human Interface Guidelines differentiate between "Normal" and "Destructive"
  actions on a row. Toga will interpret any action with a name of "Delete" or "Remove"
  as destructive, and will render the action appropriately.

Reference
---------

.. autoclass:: toga.DetailedList
   :members:
   :undoc-members:
