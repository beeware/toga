from __future__ import annotations

from pathlib import Path
from typing import Any

from ..base import BasePositronBootstrap

TEMPLATE_PATH = Path(__file__).parent / "templates"


class StaticPositronBootstrap(BasePositronBootstrap):
    def app_source(self) -> str:
        return self.templated_content(TEMPLATE_PATH / "app.py")

    def extra_context(self, project_overrides: dict[str, str]) -> dict[str, Any] | None:
        """Runs prior to other plugin hooks to provide additional context.

        This can be used to prompt the user with additional questions or run arbitrary
        logic to supplement the context provided to cookiecutter.

        :param project_overrides: Any overrides provided by the user as -Q options that
            haven't been consumed by the standard bootstrap wizard questions.
        """
        self.select_content_path(project_overrides.pop("content_path", None))
        return {}

    def post_generate(self, base_path: Path):
        resource_path = base_path / "src" / self.context["module_name"] / "resources"

        if self.content_path:
            self.install_static_content(resource_path)
        else:
            # Write default content
            for template_name in ["index.html", "positron.css"]:
                self.templated_file(
                    TEMPLATE_PATH / template_name,
                    resource_path,
                    **self.context,
                )
