from importlib import import_module


def get_probe(monkeypatch, app_probe, name):
    module = import_module(f"tests_backend.hardware.{name.lower()}")
    return getattr(module, f"{name}Probe")(monkeypatch, app_probe)
