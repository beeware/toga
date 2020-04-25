Activity Indicator
==================

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(ActivityIndicator|Component)$)'}

.. |y| image:: /_static/yes.png
    :width: 16

The activity indicator is a (spinning) animation for showing progress in an indeterminate task.

Usage
-----

.. code-block:: Python

    import toga

    spinner = toga.ActivityIndicator()

    # make widget visible and start animation
    spinner.start()

By default, the activity indicator is hidden when it is not running and will become visible when calling ``start``.
This can be changed by setting the ``hide_when_stopped`` proprerty to ``False``.

Reference
---------

.. autoclass:: toga.widgets.activityindicator.ActivityIndicator
   :members:
   :undoc-members:
   :inherited-members:
