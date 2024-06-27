.. _dialogs:

Dialogs
=======

A short-lived window asking the user for input.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :include: {0: '^Dialogs$'}

Usage
-----

A dialog is a short-lived window that requires the user to provide acknowledgement,
respond to a question, or provide information to the application.

A dialog can be presented relative to a specific window (a window-modal dialog), and
relative to the entire app (an app-modal dialog). When presented as a window-modal
dialog, the user will *not* be able to interact with anything in the window until the
dialog is dismissed. When presented as an app-modal dialog, the user will be restricted
from interacting with the rest of the app (there are some platform-specific variations
in this behavior; see the :ref:`platform notes <dialog-notes>` for details).

When a dialog is presented, the app's event loop will continue to run, and the content
of the app windows will redraw if requested by the event loop. For this reason, dialogs
are implemented *asynchronously* - that is, they must be ``await``-ed in the context
of an ``async`` method. The value returned by the ``await`` is the response of the
dialog; the return type will vary depending on the type of dialog being displayed.

To display a dialog, create an instance of the dialog type you want to display, and
``await`` the ``dialog()`` method in the context that you want to display the dialog
(either :meth:`toga.Window.dialog` or :meth:`toga.App.dialog`). In the following
example, ``my_handler`` is an asynchronous method defined on an :class:`~toga.App`
subclass that would be installed as an event handler (e.g., as an
:meth:`~toga.Button.on_press` handler on a :class:`~toga.Button`). The dialog is
displayed as window-modal against the app's main window; the dialog returns ``True`` or
``False`` depending on the user's response:

.. code-block:: python

    async def my_handler(self, widget, **kwargs):
        ask_a_question = toga.QuestionDialog("Hello!", "Is this OK!")

        if await self.main_window.dialog(ask_a_question):
            print("The user said yes!")
        else:
            print("The user said no.")

When this handler is triggered, the dialog will be displayed, but a ``print`` statement
will not be executed until the user's response has been received. To convert this
example into an app-modal dialog, you would use ``self.dialog(ask_a_question)``, instead
of ``self.main_window.dialog(ask_a_question)``.

If you need to display a dialog in a synchronous context (i.e., in a normal,
non-``async`` event handler), you must create a :any:`asyncio.Task` for the dialog, and
install a callback that will be invoked when the dialog is dismissed:

.. code-block:: python

    def my_sync_handler(self, widget, **kwargs):
        ask_a_question = toga.QuestionDialog("Hello!", "Is this OK!")

        task = asyncio.create_task(self.main_window.dialog(ask_a_question))
        task.add_done_callback(self.dialog_dismissed)
        print("Dialog has been created")

    def dialog_dismissed(self, task):
        if task.result():
            print("The user said yes!")
        else:
            print("The user said no.")


In this example, when ``my_sync_handler`` is triggered, a dialog will be created, the
display of that dialog will be scheduled as an asynchronous task, and a message will be
logged saying the dialog has been created. When the user responds, the
``dialog_dismissed`` callback will be invoked, with the dialog task provided as an
argument. The result of the task can then be interrogated to handle the response.

.. _dialog-notes:

Notes
-----

* On macOS, app-modal dialogs will *not* prevent the user from interacting with the rest
  of the app.

Reference
---------

.. autoclass:: toga.InfoDialog

.. autoclass:: toga.QuestionDialog

.. autoclass:: toga.ConfirmDialog

.. autoclass:: toga.ErrorDialog

.. autoclass:: toga.StackTraceDialog

.. autoclass:: toga.SaveFileDialog

.. autoclass:: toga.OpenFileDialog

.. autoclass:: toga.SelectFolderDialog
