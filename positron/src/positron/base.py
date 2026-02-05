from __future__ import annotations

import shutil
from pathlib import Path

from briefcase.bootstraps import TogaGuiBootstrap


class BasePositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    def validate_url_path(self, value: str) -> bool:
        """Validate that the value is a valid path."""
        if not value.startswith("/"):
            raise ValueError("Path must start with a /")
        return True

    def validate_content_path(self, value: str) -> bool:
        """Validate that the value is a directory."""
        if value:
            if value.startswith("https://"):
                raise ValueError("Positron can't scrape existing web sites (...yet!)")
            elif not Path(value).resolve().is_dir():
                raise ValueError(f"Path {Path(value).resolve()} does not exist")
        return True

    def templated_content(self, template_path, **context):
        """Render the template at the provided path.

        If a {template_path}.tmpl exists, it will be expanded with the provided
        context. Otherwise, the content will be used as-is.
        """
        full_template_path = template_path.with_suffix(template_path.suffix + ".tmpl")
        if full_template_path.exists():
            template = full_template_path.read_text(encoding="utf-8")
            return template.format(**context)
        else:
            return template_path.read_text(encoding="utf-8")

    def templated_file(self, template_path, output_path, **context):
        """Render the template at the provided path with the provided context, saving
        the result in `output_path`.
        """
        self.console.debug(f"Writing {template_path.name}")
        (output_path / template_path.name).write_text(
            self.templated_content(template_path, **context),
            encoding="utf-8",
        )

    def select_content_path(self, override_content_path):
        """Ask the user for a path to existing web content to use in the app."""
        self.content_path = self.console.text_question(
            intro=(
                "Where can Briefcase find the web content for the Positron app?\n"
                "\n"
                "The value should be a path to a directory; the contents of that "
                "directory will be copied into the Positron app, and form the root "
                "folder of the served content. If you don't provide a path, default "
                "content will be provided."
            ),
            description="Path to web content",
            default="",
            validator=self.validate_content_path,
            override_value=override_content_path,
        )

    def install_static_content(self, web_root_path):
        if self.content_path.startswith(("http://", "https://")):
            raise RuntimeError("Can't clone web content (...yet!)")
        elif self.content_path:
            # Copy an existing content path
            with self.console.wait_bar("Copying web content..."):
                shutil.copytree(
                    Path(self.content_path).resolve(),
                    web_root_path,
                    dirs_exist_ok=True,
                )

    def pyproject_table_web(self):
        return """\
supported = false
"""
