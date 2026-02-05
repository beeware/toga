from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):  # pragma: no-cover-if-lt-py311
    import tomllib
else:  # pragma: no-cover-if-gte-py311
    import tomli as tomllib

from ..base import BasePositronBootstrap


class FastAPIPositronBootstrap(BasePositronBootstrap):
    display_name_annotation = "does not support Web deployment"

    @property
    def template_path(self):
        return Path(__file__).parent / "templates"

    def app_start_source(self):
        return self.templated_content("__main__.py", initial_path=self.initial_path)

    def app_source(self):
        return self.templated_content("app.py", initial_path=self.initial_path)

    def pyproject_table_briefcase_app_extra_content(self):
        return """
requires = [
    # 0.125.0 is the last version of FastAPI that supports Pydantic < 2.0
    # This is a blocker on iOS/Android until wheels for pydantic-core are available.
    "fastAPI == 0.125.0",
    "uvicorn == 0.40.0",
]
test_requires = [
{% if cookiecutter.test_framework == "pytest" %}
    "pytest",
{% endif %}
]
"""

    def pyproject_table_iOS(self):
        iOS_table = tomllib.loads(super().pyproject_table_iOS())
        base_requires = "\n".join(f'    "{req}",' for req in iOS_table["requires"])
        return f"""\
requires = [
{base_requires}
    "pydantic < 2",
]
"""

    def pyproject_table_android(self):
        android_table = tomllib.loads(super().pyproject_table_android())
        base_requires = "\n".join(f'    "{req}",' for req in android_table["requires"])
        return f"""\
requires = [
{base_requires}
    "pydantic < 2",
]

base_theme = "Theme.MaterialComponents.Light.DarkActionBar"

build_gradle_dependencies = [
    "com.google.android.material:material:1.13.0",
]
"""

    def extra_context(self, project_overrides: dict[str, str]) -> dict[str, Any] | None:
        """Runs prior to other plugin hooks to provide additional context.

        This can be used to prompt the user with additional questions or run arbitrary
        logic to supplement the context provided to cookiecutter.

        :param project_overrides: Any overrides provided by the user as -Q options that
            haven't been consumed by the standard bootstrap wizard questions.
        """
        self.initial_path = self.console.text_question(
            intro=(
                "What path do you want to use as the initial URL for the app's "
                "webview?\n"
                "\n"
                "The value should start with a '/', but can be any path that your "
                "FastAPI site will serve."
            ),
            description="Initial path",
            default="/",
            validator=self.validate_path,
            override_value=project_overrides.pop("initial_path", None),
        )

        return {}

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        # App files
        for template_name in ["server.py"]:
            self.console.debug(f"Writing {template_name}")
            self.templated_file(
                template_name,
                app_path,
                module_name=self.context["module_name"],
            )
