from __future__ import annotations

from pathlib import Path
from typing import Any

from briefcase.bootstraps import TogaGuiBootstrap


def validate_path(value: str) -> bool:
    """Validate that the value is a valid path."""
    if not value.startswith("/"):
        raise ValueError("Path must start with a /")
    return True


def templated_content(template_name, **context):
    """Render a template for `template.name` with the provided context."""
    template = (
        Path(__file__).parent / f"django_templates/{template_name}.tmpl"
    ).read_text(encoding="utf-8")
    return template.format(**context)


def templated_file(template_name, output_path, **context):
    """Render a template for `template.name` with the provided context, saving the
    result in `output_path`."""
    (output_path / template_name).write_text(
        templated_content(template_name, **context), encoding="utf-8"
    )


class DjangoPositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    def app_source(self):
        return templated_content("app.py", initial_path=self.initial_path)

    def pyproject_table_briefcase_app_extra_content(self):
        return """
requires = [
    "django~=5.1",
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
                "Django site will serve."
            ),
            description="Initial path",
            default="/admin/",
            validator=validate_path,
            override_value=project_overrides.pop("initial_path", None),
        )

        return {}

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        # Top level files
        self.console.debug("Writing manage.py")
        templated_file(
            "manage.py",
            app_path.parent,
            module_name=self.context["module_name"],
        )
        # App files
        for template_name in ["settings.py", "urls.py", "wsgi.py"]:
            self.console.debug(f"Writing {template_name}")
            templated_file(
                template_name,
                app_path,
                module_name=self.context["module_name"],
            )
