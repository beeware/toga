PasswordInput
=============

A widget to allow the entry of a password. Any value typed by the user will be
obscured, allowing the user to see the number of characters they have typed, but
not the actual characters.

.. figure:: /reference/images/PasswordInput.png
   :align: center
   :width: 300

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(PasswordInput|Component)$)'}


Usage
-----

The ``PasswordInput`` is functionally identical to a
:class:`~toga.widgets.textinput.TextInput`, except for how the text is
displayed. All features supported by :class:`~toga.widgets.textinput.TextInput`
are also supported by PasswordInput.

.. code-block:: python

    import toga

    password = toga.PasswordInput()


Reference
---------

.. autoclass:: toga.widgets.passwordinput.PasswordInput
   :members:
   :undoc-members:
