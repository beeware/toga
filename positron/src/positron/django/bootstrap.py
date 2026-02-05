from __future__ import annotations

from pathlib import Path
from typing import Any

from ..base import BasePositronBootstrap


class DjangoPositronBootstrap(BasePositronBootstrap):
    @property
    def template_path(self):
        return Path(__file__).parent / "templates"

    def app_source(self):
        return self.templated_content("app.py", initial_path=self.initial_path)

    def pyproject_table_briefcase_app_extra_content(self):
        return """
requires = [
    "django~=6.0",
]
test_requires = [
{% if cookiecutter.test_framework == "pytest" %}
    "pytest",
{% endif %}
]
"""

    def pyproject_table_web(self):
        return """\
supported = false
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
                "Django site will serve."
            ),
            description="Initial path",
            default="/admin/",
            validator=self.validate_url_path,
            override_value=project_overrides.pop("initial_path", None),
        )

        return {}

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        # Top level files
        self.templated_file(
            "manage.py",
            app_path.parent,
            module_name=self.context["module_name"],
        )

        # App files
        for template_name in ["settings.py", "urls.py", "wsgi.py"]:
            self.templated_file(
                template_name,
                app_path,
                module_name=self.context["module_name"],
            )
