from __future__ import annotations

from pathlib import Path
from typing import Any

from ..fastapi.bootstrap import FastAPIPositronBootstrap

TEMPLATE_PATH = Path(__file__).parent / "templates"
STATIC_TEMPLATE_PATH = Path(__file__).parent.parent / "static/templates"


class PyScriptPositronBootstrap(FastAPIPositronBootstrap):
    display_name_annotation = "does not support Web deployment"

    def extra_context(self, project_overrides: dict[str, str]) -> dict[str, Any] | None:
        """Runs prior to other plugin hooks to provide additional context.

        This can be used to prompt the user with additional questions or run arbitrary
        logic to supplement the context provided to cookiecutter.

        :param project_overrides: Any overrides provided by the user as -Q options that
            haven't been consumed by the standard bootstrap wizard questions.
        """
        self.initial_path = "/"
        self.select_content_path(project_overrides.pop("content_path", None))
        return {}

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]
        resource_path = app_path / "resources"

        # FastAPI server
        for template_name in ["server.py"]:
            self.templated_file(
                TEMPLATE_PATH / template_name,
                app_path,
                module_name=self.context["module_name"],
            )

        # App files
        if self.content_path:
            self.install_static_content(resource_path)
        else:
            # Write default content for a PyScript app.
            # Start with content shared with every static app
            for template_name in ["positron.css"]:
                self.templated_file(
                    STATIC_TEMPLATE_PATH / template_name,
                    resource_path,
                    **self.context,
                )

            # Then add content that is PyScript specific
            for template_name in ["index.html", "main.py", "pyscript.toml"]:
                self.templated_file(
                    TEMPLATE_PATH / template_name,
                    resource_path,
                    **self.context,
                )
