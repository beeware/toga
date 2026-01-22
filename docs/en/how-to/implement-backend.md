# Implementing a new backend


## Extensibility and unofficial backends

In order to support multiple platforms natively, Toga uses [a 3-layered architecture](/reference/internals/architecture.md), in which the widgets that are instantiated by the user belongs to the *interface* layer, which does basic bookkeeping and normalizes quirks that exists across multiple platforms.  Each interface widget instantiates an internal *implementation* layer widget, a collection of which are provided by platform-specific backends.

On an interface layer object, using ``._impl`` often gets the implementation layer object.  On the implementation layer object, using ``.interface`` often gets the interface layer object.

Toga accomplishes backend discovery by virtue of [entry points](https://packaging.python.org/en/latest/specifications/entry-points/), and specifically, the following syntax is utilized by Toga backends in their ``pyproject.toml`` files:
```
[project.entry-points."toga.backends"]
PLATFORM = "BACKEND"
```
For example, in the Qt backend:
```
[project.entry-points."toga.backends"]
linux = "toga_qt"
```
The backend should then define a ``factory`` module that imports all of its implementation layer functionalities and widgets, which will be used by the interface layer.

Toga, by virtue of being an open-source project, allows third parties to provide independently maintained unofficial backends for Toga.  These backends have the ability to wrap a native GUI toolkit currently unsupported by Toga.  If the backend is for a commonly used but unsupported platform, can work reliably with no significant blockers, and is mature enough to be maintainable, then you may consider [proposing](contribute/what/propose-feature.md) and [submitting][implement-backend] the backend officially.

However, if you do decide to maintain a backend unofficially, please release the package for your backend using a ``togax-`` prefix in its name, instead of a ``toga-`` prefix.  The latter is reserved for official BeeWare and Toga packages only.

## Research

Preliminarily determining the steps in order to perform a number of tasks in the native GUI toolkit you plan to wrap is helpful before starting the implementation.  This includes the following:

### ``asyncio`` integration

All modern GUI toolkits has an *event loop*, which, when approximated by way of pseudocode, amounts approximately to the following:
```
while not app.quit_requested():
   app.process_events()
   app.redraw()
```
The method names shall exist for demonstration purposes only, and are fictional.  Processing events partly consists of invoking handlers and taking into account the consequences of interactions with elements such as a button, the scrollbar, etc; redrawing will display the updated GUI stemming from these consequences.

(By virtue of the approximative nature of the above demonstration, there may also exist additional phases in toolkits such as GTK, including performing layout.)

Often, however, users would like to wait on other events in this loop, and perform tasks such as waiting for a long-standing operation to finish.  All these can be accomplished by virtue of an event loop -- Pythonically, a module named `asyncio` can orchestrate event loops quite well, and in Toga it is the solution used to provide the user with means to perform asynchronous tasks like those above.  However, native GUI event loops are often different from `asyncio`.

For various GUI toolkits, there exists packages created that can integrate their event loop into `asyncio`.  Search for those that uses the Python `asyncio` interface clearly and is fully compatible with it (e.g. QtAsyncio would not be a viable option for Qt by virtue of it reimplementing some of the `asyncio` APIs by themselves incompatibly), and research how that library can be utilized to dispatch tasks asynchronously in an application built with that native GUI toolkit.  This will often involve creating an event loop and running it in a certain way.

### Replacement of the layout system

Toga aims to be native in various ways, with the exception of layout, mostly due to the diversity of how different platforms perform this task.  The implementation of layout is better explained in [this topic guide](/topics/layout.md), but since the algorithm is cross-platform, it is implemented in the interface layer, facilitated by a library named Travertino.

Thus, for the purpose of implementing a backend, one must procure the method in order to put an arbitrary widget at any location with any size in the GUI toolkit they plan to wrap.  For a more complex system, such as GTK which has an organized way of handling layout at scale that may cause difficulties, you may wish to investigate how to integrate a custom layout system into the widget toolkit, using the layout values produced by Toga to cooperate with the native layout.

---

The above two are the major tasks, that if handled, should make the actual implementation much more straightforward.  Now we could begin.

## Implementation

The sections below encompasses what would be the most important to implement, in a recommended order.  General tips / explanations are provided, followed by expandable explanations of specific potential areas of confusion.

### ``Window`` and ``App``

Start by implementing 2 basic classes:  [`Window`][toga.Window] and [`App`][toga.App].  At this stage, it is imperative to note that the implementations need not be feature-complete, and to [avoid scope creep](contribute/how/scope-creep.md); having a window to manage its size, position, lifecycle, and visibility is often sufficient, and similarly, App need not manage current window, dialogs, cursors, and commands, but should have the correct startup and main loop sequence and be able to instantiate the GUI elements.  In the process, if an error is raised about a functionality not being available, it is acceptable to stub it with ``pass`` or returning a similar structure, such as an empty array.  In the process, ``self.interface.factory.not_implemented("brief description / function name")`` (where ``self`` is most of the classes in the implementation layer) can be used to indicate that a functionality is not implemented yet.

For understanding what should be done in the classes, you can take a look at ``toga_dummy`` for the necessary APIs that should be implemented -- however, they may not be representative of typical implementations of the functionalities.  The actual code for the other backends may also be a good reference -- but it is recommended to take a look at multiple other backends to see how things are achieved; each backend can and should have its own, slightly different shape, influenced by the differences of the public interface API and the native layer.

??? abstract "App startup handling"

    Remarks about App.interface.startup

??? abstract "Window Close Handling"

    Remarks about sWindow on close handlers

### Widgets and Layout

Containers, etc.
