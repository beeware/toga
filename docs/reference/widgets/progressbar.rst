:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Progress Bar
============

The progress bar is a simple widget for showing a percentage progress for task completion.

Usage
-----

.. code-block:: Python

    import toga

    progress = toga.ProgressBar(max=100, value=1)

    # Update progress
    progress.value = 10

A progress bar can be in one of four visual states, determined by its ``max`` properties, and with the ``start()`` and ``stop()`` methods.
Calling the ``start()`` method will make the progress bar enter running mode, and calling ``stop()`` will exit running mode.
See the table below:

======= ============== ===================================
``max`` ``is_running`` Behavior
======= ============== ===================================
None    False          disabled
None    True           indeterminate (continuous animation)
number  False          show percentage
number  True           show percentage and busy animation
======= ============== ===================================

If a progress bar is indeterminate, it is communicating that it has no exact percentage to report, but that work is still begin done. It may communicate this by continuously pulsing back and forth, for example.

A second type of animation occurs when a percentage is displayed and the application wants to signal that progress is still "busy". Such an animation might involve gradually altering a lighting gradient on the progress bar.

**Note**: Not every platform may support these animations.

ProgressBar state examples:

.. code-block:: Python

    # use indeterminate mode
    progress.max = None
    print(progress.is_determinate) #  => False
    progress.start()
    print(progress.is_running) #  => True

    # show percentage and busy animation (if supported)
    progress.max = 100
    print(progress.is_determinate) #  => True

    # signal that no work is begin done with the disabled state
    progress.max = None
    print(progress.is_determinate) #  => False
    progress.stop()
    print(progress.is_running) #  => False


Supported Platforms
-------------------

.. include:: ../supported_platforms/ProgressBar.rst

Reference
---------

.. autoclass:: toga.widgets.progressbar.ProgressBar
   :members:
   :undoc-members:
   :inherited-members:
