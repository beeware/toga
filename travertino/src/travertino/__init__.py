def _package_version(file, name):
    try:
        # Read version from SCM metadata
        # This will only exist in a development environment
        from setuptools_scm import get_version

        # Excluded from coverage because a pure test environment (such as the one
        # used by tox in CI) won't have setuptools_scm
        return get_version(root="../../..", relative_to=file)  # pragma: no cover
    except (
        ModuleNotFoundError,
        LookupError,
    ):  # pragma: no-cover-if-missing-setuptools_scm
        # If setuptools_scm isn't in the environment, the call to import will fail.
        # If it *is* in the environment, but the code isn't a git checkout (e.g.,
        # it's been pip installed non-editable) the call to get_version() will fail.
        # If either of these occurs, read version from the installer metadata.
        import importlib.metadata

        # The Toga package names as defined in pyproject.toml all use dashes.
        package = name.replace("_", "-")
        return importlib.metadata.version(package)


__version__ = _package_version(__file__, __name__)
