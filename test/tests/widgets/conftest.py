from importlib import import_module

from pytest import fixture, skip


@fixture
async def simple_layout(main_box, widget):
    main_box.add(widget)
    yield
    main_box.remove(widget)


@fixture
async def probe(main_box, widget, simple_layout):
    name = type(widget).__name__
    try:
        module = import_module(f"test_probes.widgets.probe_{name.lower()}")
    except ImportError:
        skip(f"No probe module for {name}")
    return getattr(module, f"{name}Probe")(main_box, widget)
