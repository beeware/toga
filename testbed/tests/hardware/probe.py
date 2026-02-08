from importlib import import_module

from ..conftest import skip_if_unbundled_app, skip_on_platforms


def list_probes(
    hardware: str, skip_platforms: tuple[str] = (), skip_unbundled: bool = False
):
    """Retrieve the probe classes for the hardware.

    :param hardware: the hardware for which to list the probes,
        matching the module name for (e.g., "location", "camera")
    :param skip_platforms: platforms to skip
    :param skip_unbundled: whether to skip unbundled apps"""
    skip_on_platforms(*skip_platforms, allow_module_level=True)
    if skip_unbundled:
        skip_if_unbundled_app(allow_module_level=True)

    module = import_module(f"tests_backend.hardware.{hardware}")

    explicit_probes = getattr(module, "PROBES", None)
    if explicit_probes:
        return explicit_probes

    return [getattr(module, f"{hardware.title()}Probe")]
