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

A progress bar can have 4 different visual states, and its current state is determined by its ``max`` and ``running`` properties. See the table below:

| ``max`` | ``running`` | Behavior                |
|---------|-------------|-------------------------|
| None    | False       | disabled                |
| None    | True        | indeterminate (continuous animation).     |
| number  | False       | show percentage         |
| number  | True        | show percentage and busy animation  |

Two different animations may be

If a progress bar is indeterminate, it is communicating that it has no exact percentage to report, but that work is still begin done. It may communicate this by continuously pulsing back and forth, for example.

A second type of animation occurs when a percentage is displayed and the application wants to signal that progress is still "busy". Such an animation might involve gradually altering a lighting gradient on the progress bar.

**Note**: Not every platform may support these animations.

ProgressBar state examples:

.. code-block:: Python

    # use indeterminate mode
    progess.max = None
    progress.running = True

    # show percentage and busy animation (if supported)
    progress.max = 100

    # signal that no work is begin done with the disabled state
    progress.max = None
    progress.running = False

Supported Platforms
-------------------

.. include:: ../supported_platforms/ProgressBar.rst

Reference
---------

.. autoclass:: toga.widgets.progressbar.ProgressBar
   :members:
   :undoc-members:
   :inherited-members:
