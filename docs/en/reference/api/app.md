# App

The top-level representation of an application.

::: {.rst-class}
widget-support
:::

::: {.csv-filter header-rows="1" file="../data/widgets_by_platform.csv" included_cols="4,5,6,7,8,9,10" include="{0: '^Application$'}"}
Availability (`Key <api-status-key>`{.interpreted-text role="ref"})
:::

## Usage

The App class is the top level representation of all application
activity. It is a singleton object - any given process can only have a
single App. That application may manage multiple windows, but it will
generally have at least one window (called the
`~toga.App.main_window`{.interpreted-text role="attr"}).

The application is started by calling
`~toga.App.main_loop()`{.interpreted-text role="meth"}. This will invoke
the `~toga.App.startup()`{.interpreted-text role="meth"} method of the
app.

``` python
import toga

app = toga.App("Simplest App", "com.example.simplest")
app.main_loop()
```

You can populate an app's main window by passing a callable as the
`startup` argument to the `toga.App`{.interpreted-text role="class"}
constructor. This `startup` method must return the content that will be
added to the main window of the app.

``` python
import toga

def create_content(app):
    return toga.Box(children=[toga.Label("Hello!")])

app = toga.App("Simple App", "com.example.simple", startup=create_content)
app.main_loop()
```

This approach to app construction is most useful with simple apps. For
most complex apps, you should subclass `toga.App`{.interpreted-text
role="class"}, and provide an implementation of
`~toga.App.startup()`{.interpreted-text role="meth"}. This
implementation *must* assign a value to
`~toga.App.main_window`{.interpreted-text role="attr"} for the app. The
possible values are `discussed
below <assigning-main-window>`{.interpreted-text role="ref"}; most apps
will assign an instance of `toga.MainWindow`{.interpreted-text
role="any"}:

``` python
import toga

class MyApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()
        self.main_window.content = toga.Box(children=[toga.Label("Hello!")])
        self.main_window.show()

if __name__ == '__main__':
    app = MyApp("Realistic App", "org.beeware.realistic")
    app.main_loop()
```

Every app must have a formal name (a human readable name), and an app ID
(a machine-readable identifier - usually a reversed domain name). In the
examples above, these are provided as constructor arguments. However,
you can also provide these details, along with many of the other
constructor arguments, as packaging metadata in a format compatible with
`importlib.metadata`{.interpreted-text role="any"}. If you deploy your
app with [Briefcase](https://briefcase.readthedocs.io/en/stable), this
will be done automatically.

A Toga app will install a number of default commands to reflect core
application functionality (such as the Quit/Exit menu item, and the
About menu item). The IDs for these commands are defined as constants on
the `~toga.Command`{.interpreted-text role="class"} class. These
commands are automatically installed *before*
`~toga.App.startup()`{.interpreted-text role="meth"} is invoked. If you
wish to customize the menu items exposed by your app, you can add or
remove commands in your `~toga.App.startup()`{.interpreted-text
role="meth"} implementation.

## Assigning a main window {#assigning-main-window}

An app *must* assign `main_window` as part of the startup process.
However, the value that is assigned as the main window will affect the
behavior of the app.

### `~toga.Window`{.interpreted-text role="class"} {#toga.window}

Most apps will assign an instance of `toga.Window`{.interpreted-text
role="class"} (or a subclass, such as
`toga.MainWindow`{.interpreted-text role="class"}) as the main window.
This window will control the life cycle of the app. When the window
assigned as the main window is closed, the app will exit.

If you create an `App` by passing a `startup` argument to the
constructor, a `~toga.MainWindow`{.interpreted-text role="class"} will
be automatically created and assigned to `main_window`.

### `None`

If your app doesn't have a single "main" window, but instead has
multiple windows that are equally important (e.g., a document editor, or
a web browser), you can assign a value of `None` to
`~toga.App.main_window`{.interpreted-text role="attr"}. The resulting
behavior is slightly different on each platform, reflecting platform
differences.

On macOS, the app is allowed to continue running without having any open
windows. The app can open and close windows as required; the app will
keep running until explicitly exited. If you give the app focus when it
has no open windows, a file dialog will be displayed prompting you to
select a file to open. If the file is already open, the existing
representation for the document will be given focus.

On Linux and Windows, when an app closes the last window it is managing,
the app will automatically exit. Attempting to close the last window
will trigger any app-level `~toga.App.on_exit`{.interpreted-text
role="meth"} handling in addition to any window-specific
`~toga.Window.on_close`{.interpreted-text role="meth"} handling.

Mobile, web and console platforms *must* define a main window.

### `~toga.App.BACKGROUND`{.interpreted-text role="attr"} {#toga.app.background}

Assigning a value of `toga.App.BACKGROUND`{.interpreted-text
role="attr"} as the main window will allow your app to persist even if
it doesn't have any open windows. It will also hide any app-level icon
from your taskbar.

Background apps are not supported on mobile, web and console platforms.

## Life cycle of an app

Regardless of what an application does, every application goes through
the same life cycle of starting, running, and shutting down.

Application startup is handled by the
`~toga.App.startup`{.interpreted-text role="meth"} method described
above. `~toga.App.startup`{.interpreted-text role="meth"} *cannot* be an
asynchronous method, as it runs *before* the App's event loop is
started.

All other events in the life cycle of the app can be managed with event
handlers. `toga.App`{.interpreted-text role="class"} defines the
following event handlers:

- `~toga.App.on_running`{.interpreted-text role="meth"} occurs as soon
  as the app's event loop has started.
- `~toga.App.on_exit`{.interpreted-text role="meth"} occurs when the
  user tries to exit. The handler for this event must return a Boolean
  value: `True` if the app is allowed to exit; `False` otherwise. This
  allows an app to abort the exit process (for example, to prevent exit
  if there are unsaved changes).

Event handlers can be defined by subclassing
`toga.App`{.interpreted-text role="class"} and overriding the event
handler method, by assigning a value to the event handler when the app
instance is constructed, or by assigning the event handler attribute on
an existing app instance. When the event handler is set by assigning a
value to the event handler, the handler method must accept an `app`
argument. This argument is not required when subclassing, as the app
instance can be implied. Regardless of how they are defined, event
handlers *can* be defined as `async` methods.

## Managing documents

When you create an App instance, you can declare the type of documents
that your app is able to manage by providing a value for
`document_types`. When an app declares that it can manage document
types, the app will automatically create file management menu items
(such as New, Open and Save), and the app will process command line
arguments, creating a `toga.Document`{.interpreted-text role="class"}
instance for each argument matching a registered document type.

For details on how to define and register document types, refer to `the
documentation on document handling <./resources/document>`{.interpreted-text
role="doc"}.

## Notes

- On macOS, menus are tied to the app, not the window; and a menu is
  mandatory. Therefore, a macOS app will *always* have a menu with the
  default menu items, regardless of the window being used as the main
  window.
- Apps executed under Wayland on Linux environment may not show the
  app's formal name correctly. Wayland considers many aspects of app
  operation to be the domain of the windowing environment, not the app;
  as a result, some API requests will be ignored under a Wayland
  environment. Correctly displaying the app's formal name requires the
  use of a desktop metadata that Wayland can read. Packaging your app
  with [Briefcase](https://briefcase.readthedocs.io/en/stable) is one
  way to produce this metadata.

## Reference

::: {.autoclass}
toga.App
:::

::: {.autoprotocol}
toga.app.AppStartupMethod
:::

::: {.autoprotocol}
toga.app.BackgroundTask
:::

::: {.autoprotocol}
toga.app.OnRunningHandler
:::

::: {.autoprotocol}
toga.app.OnExitHandler
:::
