# File management

In order to read and write files in a Python project, you need to be able to specify the location of the file you want to use. However, when you're deploying Python code as a packaged app, specifying that location is more complex than it would be when running Python code through the interpreter, or at an interactive Python prompt. Toga's app paths feature is designed to provide a way to reliably locate files, regardless of how an app is deployed.

For this guide, we're going to use Briefcase to package our application. However, the same path-related issues outlined here exist regardless of what tool you use to deploy your code, whether that is Setuptools, `py2app`, PyInstaller, or something else.

## File access

If you've worked with accessing files in Python, you're probably used to being able to read from a file in the same directory as your Python script using something like the following:

```python
with open("file.txt") as f:
    f.read()
```

This is an example of a *relative path*, meaning Python is expecting `file.txt` to be in a location relative to the Python program itself. Python defaults to looking in the *current working directory* - that is, the directory from which the program is being run. You are able to use relative paths to point to a file based on that location. However, this means the same relative path will point to a different location if the program is run from a different directory.

Relative paths might work with simple Toga scripts. However, when you package Python code as a full application, things change. When you double-click on an icon to run an app, what directory is considered the current working directory? Is it the directory containing the app bundle? Is it the directory in the app bundle that holds the executable? There isn't a reliable answer, so we can't rely on the current working directory to construct relative paths. So - what *can* we use? We need to use *absolute paths*.

## Absolute paths

Absolute paths are the full path to a location, constructed using the root directory of the file system as the anchor (`/` on macOS and Linux; `C:\` or similar on Windows). They do not rely on the location of the Python program or app, and they are valid from anywhere in the file system. At runtime, a relative path is resolved to an absolute path, constructed using the current working directory as an anchor.

There are multiple ways to construct absolute paths in Python.

The most basic method is to spell out the entire path. For example, on macOS or Unix, to access `file.txt` in a directory called `file_directory` in your home directory, you could use `~/file_directory/file.txt`.

The `pathlib` module, from the Python standard library, provides the `Path` class to describe paths. It also provides several methods that return absolute paths, including `Path.cwd()`, which returns a `Path` object referring to the current working directory; and `Path.home()`, which returns a `Path` object referring to your home directory. You can then use these anchors as starting points to build an absolute path.

Python also provides some tools to build absolute paths based on properties of the running Python code. In any Python file, `__file__` resolves to the absolute path to the location of file being executed, provided as a string. We can use this to construct paths; for example, `Path(__file__).parent` would be the directory containing the currently running Python file.

Let's take a look at an example of reading file contents from a file using the basic method to construct an absolute path.

Create a new Briefcase project (for a refresher on how to do this, see [the BeeWare tutorial](https://tutorial.beeware.org/en/latest/tutorial/tutorial-1)). In this example, we've used a formal name of `Config File Creator`. Once the project is created, update `app.py` in the project to contain the following:

```python
from pathlib import Path

import toga
from toga.style.pack import COLUMN


class ConfigFileCreator(toga.App):
    def startup(self):
        self.text_input = toga.MultilineTextInput()
        self.config_path_output = toga.TextInput(readonly=True)

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
            children=[
                self.text_input,
                self.config_path_output,
                load_button,
                save_button
            ],
        )
        self.main_window = toga.MainWindow(content=main_box)
        self.main_window.show()

    def load_button_pressed(self, button, **kwargs):
        path = Path("/Users/brutus/config-file-creator/initial_config.toml")
        self.text_input.value = path.read_text(encoding="utf-8")

    def save_button_pressed(self, button, **kwargs):
        self.config_path_output.value = "Save not implemented."


def main():
    return ConfigFileCreator()
```

This creates a multi-line text input with a button that loads the contents of an `initial_config.toml` file into the text input. The file content is read from the file using `pathlib.Path().read_text()`, with a hard-coded *absolute* file path.

Now, if we run `briefcase dev`, the app will run; however, it will fail when you click the "Load initial configuration" button, resulting in a `FileNotFoundError`. This version worked great on Brutus' computer. However, the moment we try to start the app on a different machine, the path is no longer valid, and it will fail to run when it can't find the file.

Using a hard-coded absolute path won't work, so lets try a relative path instead. We'll start by trying to replicate what Brutus was doing on their machine. Create an `initial_config.toml` file containing the following content, and place it in the same directory as your `pyproject.toml` file:

```toml
# Update the following to match your configuration
PROJECT_NAME = "Name"
PROJECT_VERSION = "v0.0.0"
AUTHOR_NAME = "Your Name"
```

Update the `load_button_pressed` handler to the following:

```python
def load_button_pressed(self, button, **kwargs):
  path = Path("initial_config.toml")
  self.text_input.value = path.read_text(encoding="utf-8")
```

If we run `briefcase dev` again, we get the same `FileNotFoundError` when we press the button. As this is a relative path, it is turned into an absolute path using the current working directory. You might think this would be the directory where Briefcase was executed - but clearly, it isn't.

At this point, you might think that the current working directory will be the location of the application code. Let's examine this as a possibility. Here is a summary of the directory structure of our project at this point:

```console
configfilecreator/
├── pyproject.toml
├── initial_config.toml
└── src/
    └── configfilecreator/
        ├── app.py
        └── resources/
```

Move the `initial_config.toml` file into the `src/configfilecreator/resources` folder, and update the `load_button_pressed` handler to the following:

```python
def load_button_pressed(self, button, **kwargs):
  path = Path("resources/initial_config.toml")
  self.text_input.value = path.read_text(encoding="utf-8")
```

Run the app, and press the button to load the file contents. Once again, the app will fail in the same way - a `FileNotFoundError`. The current working directory isn't the location of the app, either. We know using a path relative to the app file won't work, even when the file content is packaged with the app.

So - lets build an absolute path, using an anchor that we *do* know - the `__file__` attribute of the running code. Update the `load_button_pressed` handler to the following:

```python
def load_button_pressed(self, button, **kwargs):
    path = Path(__file__).parent / "resources/initial_config.toml"
    self.text_input.value = path.read_text(encoding="utf-8")
```

Now when you run the app, it will start, and the button will successfully load the contents of the file into the multi-line text input.

In this situation we have only one app file, so `__file__` is a useful location. However, in a more complex application with multiple levels of modules, or when calling a library that is independent of the app, to use `Path(__file__)` we would need to know where the file that is reading the code is in the code checkout relative to the `resources` directory.

So, how do we get the benefits of absolute paths, but ensure that the file can be found regardless of where the app is being run? This is where Toga can help.

## App paths

Toga includes an [app paths](/reference/api/data-representation/paths.md) feature that provides a selection of known locations on the user's computer. Provided as `pathlib.Path` objects, they are known-safe locations for reading and writing files, that are specific to each operating system. Each user running an application will have their own unique app paths.

The read-only path location, `paths.app`, provides an anchor from the location of the app file.[^1] It can therefore be used to construct absolute paths based on the app file location within the package.

Let's build on the previous example to use the `paths.app` to locate the file.

Update `load_button_pressed` handler to the following:

```python
def load_button_pressed(self, button, **kwargs):
    path = self.paths.app /  "resources/initial_config.toml"
    self.text_input.value = path.read_text(encoding="utf-8")
```

The path to the file is being constructed from the `self.paths.app` `Path` object, instead of a hard-coded absolute path, or a path based on the location of a specific Python file. If you have a more complex application, or a library that isn't part of your app code, and you can pass in a reference to the app (or access the `toga.App.app` singleton), you can refer to the location of the folder containing the app code.

When we run the app, it starts successfully. We can click the button, and we'll see the contents of the file loaded into the text input. This will also work when using `briefcase run`, or with any mode of deployment, including desktop or mobile platforms, because `paths.app` will adapt to local conditions.

We've successfully read from a file packaged within our app. What about writing a file? This gets more complicated. Let's explore how to use app paths to write files to the file system.

## Writing Files

So far, we've used `paths.app`, which should be considered a *read-only* location. Toga won't stop you from writing to the app directory, and in testing, it will almost always work. However, once you ship your packaged app in production, writing to the app will almost certainly fail. The reason varies depending on your operating system.

- On Windows, you can install an app as a user, or for all users. Installing for all users requires admin privileges; however when you run the app as a user, you are no longer running it as an admin, and you will not be permitted to write to that location.
- On macOS, the contents of an app are contained within the app bundle. The contents of that app bundle have been signed and notarized, which cryptographically seals the bundle; if you try to write to it, you will break that seal which can cause problems running the app in the future.
- On Unix, if `sudo` is used to install the app into `/usr` (or a similar location), it installs to a directory that the user does not have permissions to write to.
- On iOS and Android, the app is a signed bundle that cannot be modified at runtime.

So - you can read from `paths.app`, but you shouldn't write to it.

But what do you do if you want to save a file? Toga provides four writable paths available for storing files associated with an app:

- `paths.data`: The location for storing user data.
- `paths.config`: The location for storing user configuration data.
- `paths.cache`: The location for storing cache files. This should be used only for easily regenerated files as the operating system may purge the contents of this directory without warning.
- `paths.logs`: The location for storing log files.

These paths are different on every operating system. They will be subdirectories found in `~/Library` on macOS; XDG-compliant dotfiles in `~` on Linux; the user's `AppData` directory on Windows; iOS and Android provide similar locations that aren't generally visible to end-users. These paths are guaranteed to be writable; and they will be user specific *and* application specific, so they won't collide with any other content on the user's computer.

Let's build on the current application to generate a configuration file from the contents of the `initial_config.toml` file.

Update the `save_button_pressed` handler in `app.py` to the following:

```python
def save_button_pressed(self, button, **kwargs):
   path = self.paths.config / "config.toml"
   path.write_text(self.text_input.value, encoding="utf-8")
   self.config_path_output.value = path
```

This change implements the save button, that when pressed, saves the current content of the text input to a `config.toml` file in an app-specific subdirectory of the operating-system appropriate configuration directory, and displays the path to the file below the input.

Run the app and click the "Load initial configuration" button to load the file contents into the text input. Update the variables to whatever you like. Click the save button to generate the file. In your file explorer or terminal, you can use the path displayed below the input to find and view your new configuration file directly.

## Updating an existing file

Now that the user's configuration file has been generated and saved, you may want to update it. The current app will always load `initial_config.toml` - so any user-supplied modifications will be lost. So - lets modify the app to check for an existing user-saved configuration file, and load the contents of that if it exists.

Update the `load_button_pressed` handler in `app.py` to the following:

```python
def load_button_pressed(self, button, **kwargs):
    path = self.paths.config / "config.toml"
    if not path.exists():
        path = self.paths.app / "resources/initial_config.toml"
    self.text_input.value = path.read_text(encoding="utf-8")
```

This updates the handler to first try to load content from an existing `config.toml` file in the configuration directory, and then, if the file does not exist, loads the `initial_config.toml` file contents instead.

### Footnotes

[^1]: More precisely, `paths.app` is the path of the directory that     contains the Python file that defines the class that is being     executed as the app, specifically the Python file that includes the     app class definition (i.e., `class MyApp(toga.App)`). This is     essentially the same as `Path(__file__).parent` inside `app.py`; but     in more complex applications, `__file__` will refer to the current     file, whereas `paths.app` will return the same location no matter     where it is used.
