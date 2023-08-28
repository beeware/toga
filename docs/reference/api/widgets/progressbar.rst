ProgressBar
===========

A horizontal bar to visualize task progress. The task being monitored can be of
known or indeterminate length.

.. tabs::

  .. group-tab:: macOS

    .. figure:: /reference/images/progressbar-macOS.png
       :align: center
       :width: 300px

  .. group-tab:: Linux

    .. figure:: /reference/images/progressbar-gtk.png
       :align: center
       :width: 300px

  .. group-tab:: Windows

    .. figure:: /reference/images/progressbar-winforms.png
       :align: center
       :width: 300px

  .. group-tab:: Android

    .. figure:: /reference/images/progressbar-android.png
       :align: center
       :width: 300px

  .. group-tab:: iOS

    .. figure:: /reference/images/progressbar-ios.png
       :align: center
       :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(ProgressBar|Component)$)'}

Usage
-----

If a progress bar has a ``max`` value, it is a *determinate* progress bar. The
value of the progress bar can be altered over time, indicating progress on a
task. The visual indicator of the progress bar will be filled indicating the
proportion of ``value`` relative to ``max``. ``max`` can be any positive
numerical value.

.. code-block:: python

    import toga

    progress = toga.ProgressBar(max=100, value=1)

    # Start progress animation
    progress.start()

    # Update progress to 10%
    progress.value = 10

    # Stop progress animation
    progress.stop()

If a progress bar does *not* have a ``max`` value (i.e., ``max == None``), it is
an *indeterminate* progress bar. Any change to the value of an indeterminate
progress bar will be ignored. When started, an indeterminate progress bar
animates as a throbbing or "ping pong" animation.

.. code-block:: python

    import toga

    progress = toga.ProgressBar(max=None)

    # Start progress animation
    progress.start()

    # Stop progress animation
    progress.stop()

Notes
-----

* The visual appearance of progress bars varies from platform to platform. Toga
  will try to provide a visual distinction between running and not-running
  determinate progress bars, but this cannot be guaranteed.

Reference
---------

.. autoclass:: toga.ProgressBar
