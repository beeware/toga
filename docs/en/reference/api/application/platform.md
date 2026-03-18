{{ component_header("Platform") }}

## Usage

Although Toga is a cross-platform framework, and in theory *shouldn't* require any special platform-specific handling, in practice you will. If you wish to apply platform-specific modifications to your user interface, or modify business logic on a per-platform basis, you may need to know the currently active backend, or the platform on which your application is running. This can be achieved by using [`toga.backend`][] and [`toga.platform.current_platform`][].

For example:
```python
import toga

if toga.backend == `toga_gtk`:
    # ... perform GTK-specific logic

if toga.platform.current_platform == 'android':
    # ... perform Android-specific business logic
```

### Selecting a specific backend

In general, a Python environment should only have a single Toga backend installed. However, if you need to install multiple backends, you can tell Toga which backend to use by setting the `TOGA_BACKEND` environment variable to match the name of the Python module for the backend you wish to use (e.g., `toga_gtk`).

### Getting an implementation factory

Developers who want to implement new platform-dependent functionality, or produce a new backend, need a way to access the implementation classes for the current backend. The [`get_factory`][toga.platform.get_factory] function provides a standard way to do this, returning an object whose attributes are lazily-loaded implementation classes.

See the topic guide on [Extending Toga](../../../topics/extending-toga.md) for more information.

## Reference

::: toga.backend

::: toga.platform.current_platform

::: toga.platform.get_factory
