===============
File Management
===============

TODO: Intro needs work

If you've worked with files in Python, you're probably used to being able to access a file in the same directory as your Python script using ``with open(file.txt) as f:``. Python defaults to looking in the current working directory (the directory from which the script is being run), and all path access from this is implicit. You are able to use relative paths to point to a location. This might even work with simple Toga scripts. However, when you get into packaging applications, things change.

A packaged app can be run from anywhere on a computer, and there's no guarantee you can write a file to the location from which the app is being run. You can package file content into an app, but there's still no guarantee of the location it will be installed or run. Further, you may run into permissions issues attempting to write to the app location.

For this guide, we're going to use Briefcase for packaging your application, however the same path-related issues outlined here exist regardless of what tool you use, including Setuptools, py2app, PyInstaller, and so on.

TODO: More

So, if relative paths won't work in this situation, what can we do? We need to use absolute paths.

Absolute paths
==============

In any Python file, ``__file__`` is the full path to current working directory, i.e. the location of file being executed, provided as a string. You can use this to construct paths; for example, ``Path(__file__).parent`` is the parent directory of the currently running Python program.

The ``pathlib`` module, from the Python standard library, provides several absolute path options including ``Path.cwd()``, which is a path to the current working directory, and ``Path.home()``, which is a path to your home directory.

TODO: More

Let's take a look at an example of reading file contents from a file using an absolute path.

Create a `new Briefcase project <https://docs.beeware.org/en/latest/tutorial/tutorial-1.html>`__. Update ``app.py`` in your project to the following:

.. code-block:: python

    import pathlib

    import toga
    from toga.style.pack import COLUMN


    class ConfigFileCreator(toga.App):
        def startup(self):
            file_content = pathlib.Path(
                "/Users/brutus/configfilecreator/src/configfilecreator/resources/initial_config.toml"
            ).read_text(encoding="utf-8")

            self.text_input = toga.MultilineTextInput(value=file_content)

            main_box = toga.Box(
                direction=COLUMN,
                children=[self.text_input],
            )
            self.main_window = toga.MainWindow(content=main_box)
            self.main_window.show()


    def main():
        return ConfigFileCreator()

This creates a multiline text input and automatically loads the contents of an ``initial_config.toml`` file into the text input. The file content is read from the file using ``pathlib.Path().read_text()`` with a hardcoded file path.

Now, if we run ``briefcase dev``, the app will fail to start, resulting in a ``FileNotFoundError``. This version worked great on Brutus' computer. However, the moment we try to start the app on a different machine, the path is no longer valid, and it will fail to run when it can't find the file.

You might be thinking: the issue is that the file is not located in the application. Let's examine this as a possibility. Here is a the basic structure of a Briefcase project:

.. code-block:: console

    helloworld/
    └── src/
        └── helloworld/
            ├── app.py
            └── resources/

One possible option is in the top level ``helloworld/`` directory, as that's the location from which you actually run the app. While you could point your code to this location as an absolute path, you will still run into the problem when running your app from anywhere else but your computer.

A second possible option might be to put the file in ``helloworld/src/helloworld`` because that's where the ``app.py`` file is. After all, Python bases file access on the current working directory. This second option does ensure Briefcase packages the file with your app. However, apps can be run from anywhere on a computer, so it still doesn't guarantee a consistent path.

To avoid the possibility of either of the above happening accidentally, Briefcase sets the current working directory to elsewhere so you aren't caught by this issue.

So, how do we get the benefits of absolute paths, but ensure that the file can be found and read regardless of where the app is being run? This is where Toga can help.

App paths
=========

Toga includes an :doc:`app paths </reference/api/resources/app_paths>` feature that provides a selection of known locations on the user's computer. Provided as a ``pathlib.Path`` object, they are known-safe locations for reading and writing files, that are specific to each operating system. They are unique to each application, and guaranteed to be isolated to the specific app. There are four writeable paths available for storing files associated with an app:

- ``data``: The location for storing user data.
- ``config``: The location for storing user configuration data.
- ``cache``: The location for storing cache files. This should be used only for easily regenerated files as the operating system may purge the contents of this directory without warning.
- ``logs``: The location for storing log files.

Toga also provides a read-only path location, ``app``, that provides an anchor from the location of the app file, or more specifically, the path of the directory that contains the Python file that defines the class that is being executed as the app. It is essentially returning ``Path(__file__).parent``, however ``app`` will return the same location no matter where you are. It can therefore be used to construct absolute paths based on the app file location within the package.

These paths are different on every operating system, and Toga guarantees the correct paths will be provided. The paths will be subdirectories found in ``~/Library`` on macOS, XDG-compliant dotfiles in ``~`` on Linux, and ``AppData/`` on Windows.

Let's build on the previous example to use app paths to locate the file.

Create a ``initial_config.toml`` file containing the following content, and place it in the ``resources/`` directory within your Briefcase project:

.. code-block:: toml

    # Update the following to match your configuration
    PROJECT_NAME = "Name"
    PROJECT_VERSION = "v0.0.0"
    AUTHOR_NAME = "Your Name"

Update ``app.py`` to the following:

.. code-block:: python

    import toga
    from toga.style.pack import COLUMN


    class ConfigFileCreator(toga.App):
        def startup(self):
            self.text_input = toga.MultilineTextInput()

            load_button = toga.Button(
                text="Load initial config",
                on_press=self.load_button_pressed,
                margin=20,
            )

            main_box = toga.Box(
                direction=COLUMN,
                children=[self.text_input, load_button],
            )
            self.main_window = toga.MainWindow(content=main_box)
            self.main_window.show()

        def load_button_pressed(self, button, **kwargs):
            path = self.paths.app / "resources/initial_config.toml"
            self.text_input.value = path.read_text(encoding="utf-8")


    def main():
        return ConfigFileCreator()

This updates the app to add a button that loads the file contents into the text input, instead of loading them automatically.

The most important change is found in the ``load_button_pressed`` handler:

.. code-block:: python

        def load_button_pressed(self, button, **kwargs):
            path = self.paths.app / "resources/initial_config.toml"
            self.text_input.value = path.read_text(encoding="utf-8")

The path to the file is being constructed from the ``self.paths.app`` ``Path`` object, instead of a hardcoded path. This means that no matter where the app is being run from, it always knows where to find the file within the package.
