===============
File Management
===============

In order to read and write files in a Python project, you need to be able to specify the location of the file you want to use. However, when you're deploying Python code as a packaged app, specifying that location is more complex than it would be when running Python code through the interpreter, or at an interactive Python prompt. Toga's app paths feature is designed to provide a way to reliably locate files, regardless of how an app is deployed.

For this guide, we're going to use Briefcase to package our application. However, the same path-related issues outlined here exist regardless of what tool you use to deploy your code, including Setuptools, py2app, PyInstaller, and so on.

File access
===========

If you've worked with accessing files in Python, you're probably used to being able to read from a file in the same directory as your Python script using something like the following:

.. code-block:: python

    with open("file.txt") as f:
        f.read()

This is an example of a relative path, meaning Python is expecting ``file.txt`` to be in a specific location relative to the Python program itself. Python defaults to looking in the *current working directory*, that is, the directory from which the program is being run. You are able to use relative paths to point to a file based on that location. However, this means the same relative path will point to a different location if the program is run from a different directory.

Absolute paths are the full path to a location, constructed using the root directory of the file system as the anchor (``/`` on macOS and Linux, and ``C:\`` on Windows). They do not rely on the location of the Python program or app, and they are valid from anywhere in the file system. At runtime, a relative path is resolved to an absolute path, constructed using the current working directory as the anchor.

Relative paths might work with simple Toga scripts. However, when you get into packaging applications, things change. When you double-click on an icon to run an app, what directory is considered the current working directory? Is it the directory containing the app bundle? Is it the directory in the app bundle that holds the executable? There isn't a solid answer. The question we really need to answer is, how can we reliably tell an app where to look for file content?

If we can't rely on the current working directory to construct relative paths, what *can* we use? We need to use absolute paths.

Absolute paths
==============

There are multiple ways to construct absolute paths in Python.

The most basic method is to spell out the entire path. For example, on macOS or Unix, to access ``file.txt`` in a directory called ``file_directory`` in your home directory, you could use ``~/file_directory/file.txt``.

In any Python file, ``__file__`` resolves to the absolute path to the location of file being executed, provided as a string. We can use this to construct paths; for example, ``Path(__file__).parent`` is the parent directory of the currently running Python program.

The ``pathlib`` module, from the Python standard library, provides several absolute path options including ``Path.cwd()``, which is the path to the current working directory, and ``Path.home()``, which is the path to your home directory.

Let's take a look at an example of reading file contents from a file using the basic method to construct an absolute path.

Create a new Briefcase project (for a refresher on how to do this, see `the BeeWare tutorial <https://docs.beeware.org/en/latest/tutorial/tutorial-1.html>`__). Once you've created that project, update ``app.py`` in the project to contain the following:

.. code-block:: python

    from pathlib import Path

    import toga
    from toga.style.pack import COLUMN


    class ConfigFileCreator(toga.App):
        def startup(self):
            self.text_input = toga.MultilineTextInput()
            self.config_directory = toga.TextInput(readonly=True)

            load_button = toga.Button(
                text="Load initial configuration",
                on_press=self.load_button_pressed,
                margin=20,
            )
            save_button = toga.Button(
                text="Save user configuration",
                on_press=self.save_button_pressed,
                margin=20,
            )

            main_box = toga.Box(
                direction=COLUMN,
                children=[self.text_input, self.config_directory, load_button, save_button],
            )
            self.main_window = toga.MainWindow(content=main_box)
            self.main_window.show()

        def load_button_pressed(self, button, **kwargs):
            path = Path("/Users/brutus/config-file-creator/initial_config.toml")
            self.text_input.value = path.read_text(encoding="utf-8")

        def save_button_pressed(self, button, **kwargs):
            self.config_directory.value = "Save not implemented."


    def main():
        return ConfigFileCreator()


This creates a multi-line text input with a button that loads the contents of an ``initial_config.toml`` file into the text input. The file content is read from the file using ``pathlib.Path().read_text()`` with a hard-coded *absolute* file path.

Now, if we run ``briefcase dev``, the app will fail to start, resulting in a ``FileNotFoundError``. This version worked great on Brutus' computer. However, the moment we try to start the app on a different machine, the path is no longer valid, and it will fail to run when it can't find the file.

You might be thinking, the issue is that the file is not located in the application. Let's examine this as a possibility. Here is a the basic structure of a Briefcase project:

.. code-block:: console

    configfilecreator/
    └── src/
        └── configfilecreator/
            ├── app.py
            └── resources/

One possible option is in the top level ``configfilecreator/`` directory, as that's the location from which we actually run the app. This may have been what Brutus was intending with the path they specified. While we could point our code to this location as an absolute path, we will still run into the problem when running the app from anywhere else but our own computer.

A second possible option might be to put the file in ``configfilecreator/src/configfilecreator`` because that's where the ``app.py`` file is. After all, Python bases file access on the directory from which the program is being run. While the second option does ensure Briefcase packages the file with the app, it still doesn't guarantee a consistent path.

To avoid the possibility of either of the above happening accidentally, Briefcase sets the current working directory to elsewhere so we aren't caught by this issue.

Let's take a look at an example of packaging the file content with the app, and using ``__file__`` to locate it.

Create an ``initial_config.toml`` file containing the following content, and place it in the ``resources/`` directory within the Briefcase project:

.. code-block:: toml

    # Update the following to match your configuration
    PROJECT_NAME = "Name"
    PROJECT_VERSION = "v0.0.0"
    AUTHOR_NAME = "Your Name"

Update the ``load_button_pressed`` handler to the following:

.. code-block:: python

    def load_button_pressed(self, button, **kwargs):
        path = Path(__file__).parent / "resources" / "initial_config.toml"
        self.text_input.value = path.read_text(encoding="utf-8")

Now when you run the app, it will start, and the button will successfully load the contents of the file into the multi-line text input. This works in this situation, because we have only one app file, and the standard directory structure. However, in a more complex application with multiple levels of modules, or when calling a library that is independent of the app, to use ``Path(__file__)``, we would need to know where the file that is reading the code is in the code checkout relative to the ``resources`` directory.

So, how do we get the benefits of absolute paths, but ensure that the file can be found regardless of where the app is being run? This is where Toga can help.

App paths
=========

Toga includes an :doc:`app paths <../../reference/api/resources/app_paths>` feature that provides a selection of known locations on the user's computer. Provided as ``pathlib.Path`` objects, they are known-safe locations for reading and writing files, that are specific to each operating system. Each user running an application will have their own unique app paths.

The read-only path location, ``paths.app``, provides an anchor from the location of the app file. [#f1]_ It can therefore be used to construct absolute paths based on the app file location within the package. For this to work, we need to package the file with our app. Briefcase guarantees that any file in the project directory (``configfilecreator/src/configfilecreator`` in the example project structure shown above), will be included with the packaged app, including the contents of any subdirectories. There are other ways to ensure a file is included - see the :doc:`Source <../../reference/api/resources/sources/source>` documentation for details.

Let's build on the previous example to use the ``paths.app`` to locate the file.

Update ``load_button_pressed`` handler to the following:

.. code-block:: python

    def load_button_pressed(self, button, **kwargs):
        path = self.paths.app /  "resources" / "initial_config.toml"
        self.text_input.value = path.read_text(encoding="utf-8")


The path to the file is being constructed from the ``self.paths.app`` ``Path`` object, instead of a hard-coded absolute path. This means that no matter where the app is being run from, it always knows where to find the file within the package.

When we run the app, it starts successfully. We can click the button, and we'll see the contents of the file loaded into the text input. This will also work when using ``briefcase run``, or with any mode of deployment, including desktop or mobile platforms, because ``paths.app`` will adapt to local conditions.

We've successfully read from a file packaged within our app. What about writing a file? This gets more complicated. Let's explore how to use app paths to write files to the file system.

Writing Files
=============

So far, we've used ``paths.app``, which should be considered read-only. Toga won't stop you from writing to the app directory, and in testing, it will almost always work. However, once you ship your packaged app in production, writing to the app will fail. The overall reason is permissions, but it is a bit different for each operating system.

- On Windows, you can install an app as a user or for all users. "All users" requires admin privileges, however when you run the app as a user, you are no longer running it as an admin, and you will not be permitted to write to that location.
- On macOS, the contents of an app are contained within the app bundle. It is a file in a directory, however the contents have been signed and notarized, which cryptographically seals the bundle, and if you try to write to it, you will break that seal and end up with problems running the app.
- On Unix, even if ``sudo`` is used to install the app, it installs to a directory that the user does not have permissions to write to.

You can read from ``paths.app``, but you shouldn't write to it.

So, what if you want to generate a file through your app and save it? Toga provides four writable paths available for storing files associated with an app:

- ``data``: The location for storing user data.
- ``config``: The location for storing user configuration data.
- ``cache``: The location for storing cache files. This should be used only for easily regenerated files as the operating system may purge the contents of this directory without warning.
- ``logs``: The location for storing log files.

These paths are different on every operating system, and Toga guarantees the correct paths will be provided. The paths will be subdirectories found in ``~/Library`` on macOS, XDG-compliant dotfiles in ``~`` on Linux, and the user's ``AppData`` directory on Windows.

Let's build on the current application to generate a configuration file from the contents of the ``initial_config.toml`` file.

Update the ``save_button_pressed`` handler in ``app.py`` to the following:

.. code-block:: python

     def save_button_pressed(self, button, **kwargs):
        path = self.paths.config / "config.toml"
        self.config_directory.value = path
        path.write_text(self.text_input.value, encoding="utf-8")

This change implements the save button, that when pressed, saves the contents of the text input to a ``config.toml`` file in an app-specific subdirectory of the operating-system appropriate configuration directory, and displays the path to the file below the input.

Run the app and click the "Load initial configuration" button to load the file contents into the text input. Update the variables to whatever you like. Click the save button to generate the file. In your file explorer or terminal, you can use the path displayed below the input to find and view your new configuration file directly.

Updating an existing file
=========================

Now that the configuration file is generated, you may want to update it. You could use the same app to load the contents of ``initial_config.toml`` and update that info to the new configuration, but then you may not know what the previous changes were. Instead, you can tell the app to check for an existing configuration file, and load the contents of that if it exists.

Update the ``load_button_pressed`` handler in ``app.py`` to the following:

.. code-block:: python

    def load_button_pressed(self, button, **kwargs):
        path = self.paths.config / "config.toml"
        if not path.exists():
            path = self.paths.app / "resources/initial_config.toml"
        self.text_input.value = path.read_text(encoding="utf-8")

This updates the handler to first try to load content from an existing ``config.toml`` file in the configuration directory, and then, if the file does not exist, loads the ``initial_config.toml`` file contents instead.

.. rubric:: Footnotes

.. [#f1] More precisely, ``paths.app`` is the path of the directory that contains the Python file that defines the class that is being executed as the app, specifically the Python file that includes ``class MyApp(toga.app):``. In an application containing only a single file, is essentially returning ``Path(__file__).parent``. In more complex applications, this may produce unexpected results, whereas ``paths.app`` will return the same location no matter where it is.
