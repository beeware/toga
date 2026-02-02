from __future__ import annotations

from pathlib import Path

from briefcase.bootstraps import TogaGuiBootstrap


class BasePositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    @property
    def template_path(self):
        return Path(__file__).parent / "templates"

    def validate_path(self, value: str) -> bool:
        """Validate that the value is a valid path."""
        if not value.startswith("/"):
            raise ValueError("Path must start with a /")
        return True

    def templated_content(self, template_name, **context):
        """Render a template for `template.name` with the provided context."""
        template = (self.template_path / f"{template_name}.tmpl").read_text(
            encoding="utf-8"
        )
        return template.format(**context)

    def templated_file(self, template_name, output_path, **context):
        """Render a template for `template.name` with the provided context, saving the
        result in `output_path`."""
        (output_path / template_name).write_text(
            self.templated_content(template_name, **context), encoding="utf-8"
        )

    def pyproject_table_web(self):
        return """\
supported = false
"""
