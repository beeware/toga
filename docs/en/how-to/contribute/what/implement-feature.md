# Implementing a new feature

{% extends "contribute/what/implement-feature.md" %}

{% block specific_feature_ideas %}

## Feature ideas

Don't worry if you don't have an idea for a new feature, there are [plenty of features we'd love to see implemented](https://github.com/beeware/toga/issues?q=is%3Aissue%20state%3Aopen%20label%3Aenhancement) for Toga. This section outlines a number of places you can start.

### Implement a platform native widget

If the core library already specifies an interface for a widget, but the widget isn't implemented on your platform of choice, implement that interface. The [API reference table](/reference/api/index.md) table can show you the widgets that are missing on various platforms. You can also look for log messages in a running app (or the direct `factory.not_implemented()` function calls that produce those log messages). At present, Qt, the Web and Textual backends have the most missing widgets. If you have web skills, or would like to learn more about [PyScript](https://pyscript.net) and [Shoelace](https://shoelace.style), the web backend could be a good place to contribute; if you'd like to learn more about terminal applications or the [Textual](https://textual.textualize.io) API, contributing to the Textual backend could be a good place for you to contribute. If you’re interested in desktop GUI development or want to deepen your understanding of the Qt framework, contributing to the [Qt](https://www.qt.io/product/framework) backend is a great option.

Alternatively, if there's a widget that doesn't exist, propose an interface design, and implement it for at least one platform. You may find [this presentation by BeeWare emeritus team member Dan Yeaw](https://www.youtube.com/watch?v=sWt_sEZUiY8) helpful. This talk gives an architectural overview of Toga, as well as providing a guide to the process of adding new widgets.

If you implement a new widget, don't forget you'll need to write tests for the new core API. If you're extending an existing widget, you may need to [add a probe for the backend][testbed-probe].

### Contribute to the GTK4 update

Toga's GTK support is currently based on the GTK3 API. This API works, and ships with most Linux distributions, but is no longer maintained by the GTK team. We're in the process of adding GTK4 support to Toga's GTK backend. You can help with this update process.

GTK4 support can be enabled by setting the `TOGA_GTK=4` environment variable. To contribute to the update, pick a widget that currently has GTK3 support, and try updating the widget's API to support GTK4 as well. You can identify a widget that hasn't been ported by looking at the [GTK probe for the widget][testbed-probe] - widgets that aren't ported yet will have an "if GTK4, skip" block at the top of the probe definition.

The code needs to support both GTK3 and GTK4; if there are significant differences in API, you can add conditional branches based on the GTK version. See one of the widgets that *has* been ported (e.g., Label) for examples of how this can be done.

### Implement an entirely new platform backend

Toga currently has support for 8 backends - but there's room for more!

The first steps of any new platform backend are always the same:

1. Implement enough of the Toga Application and Window classes to allow  you to create an empty application window, integrated with the  Python `asyncio` event loop.
2. Work out how to use native platform APIs to position a widget at a  specific position on the window. Most widget frameworks will have  some sort of native layout scheme; we need to replace that scheme  with Toga's layout algorithm. If you can work out how to place a  button with a fixed size at a specific position on the screen,  that's usually sufficient.
3. Get Tutorial 0 working. This is the simple case of a single box that  contains a single button. To get this tutorial working, you'll need  to implement the factory class for your new backend so that Toga can  instantiate widgets on your new backend, and connect the Toga style  applicator methods on the base widget that sets the position of  widgets on the screen.

Once you have those core features in place, you can start implementing widgets and other Toga features (like fonts, images, and so on).

### Improve the testing API for application writers

The dummy backend exists to validate that Toga's internal API works as expected. However, we would like it to be a useful resource for *application* authors as well. Testing GUI applications is a difficult task; a Dummy backend would potentially allow an end user to write an application, and validate behavior by testing the properties of the Dummy. Think of it as a GUI mock - but one that is baked into Toga as a framework. See if you can write a GUI app of your own, and write a test suite that uses the Dummy backend to validate the behavior of that app.


{% endblock %}
