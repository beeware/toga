from importlib import import_module

from pytest import fixture


@fixture
async def widget(main_box, new_widget):
    main_box.add(new_widget)
    yield new_widget
    main_box.remove(new_widget)


@fixture
async def probe(main_box, widget):
    name = type(widget).__name__
    module = import_module(f"test_probes.widgets.probe_{name.lower()}")
    return getattr(module, f"{name}Probe")(main_box, widget)
