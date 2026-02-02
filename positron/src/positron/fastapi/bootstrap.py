from __future__ import annotations

from pathlib import Path
from typing import Any

from briefcase.bootstraps import TogaGuiBootstrap

from ..common import templated_content, templated_file, validate_path

TEMPLATE_PATH = Path(__file__).parent / "templates"


class FastAPIPositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    def app_source(self):
        return templated_content(
            TEMPLATE_PATH,
            "app.py",
            initial_path=self.initial_path,
        )

    def pyproject_table_briefcase_app_extra_content(self):
        return """
requires = [
    "fastAPI == 0.128.0",
    "uvicorn == 0.40.0",
]
test_requires = [
{% if cookiecutter.test_framework == "pytest" %}
    "pytest",
{% endif %}
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
            validator=validate_path,
            override_value=project_overrides.pop("initial_path", None),
        )

        return {}

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        # App files
        for template_name in ["site.py"]:
            self.console.debug(f"Writing {template_name}")
            templated_file(
                TEMPLATE_PATH,
                template_name,
                app_path,
                module_name=self.context["module_name"],
            )
