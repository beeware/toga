from importlib import import_module

from ..conftest import skip_if_unbundled_app, skip_on_platforms


def list_probes(hardware, skip_platforms=(), skip_unbundled=False):
    """Retrieve the probe classes for the hardware."""
    skip_on_platforms(*skip_platforms, allow_module_level=True)
    if skip_unbundled:
        skip_if_unbundled_app(allow_module_level=True)

    module = import_module(f"tests_backend.hardware.{hardware.lower()}")

    explicit_probes = getattr(module, "PROBES", None)
    if explicit_probes:
        return explicit_probes

    return [getattr(module, f"{hardware.title()}Probe")]
