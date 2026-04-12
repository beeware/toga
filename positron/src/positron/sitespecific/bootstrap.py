from __future__ import annotations

from pathlib import Path
from typing import Any

from briefcase.config import validate_url

from ..base import BasePositronBootstrap

TEMPLATE_PATH = Path(__file__).parent / "templates"


class SiteSpecificPositronBootstrap(BasePositronBootstrap):
    @property
    def template_path(self):
        return Path(__file__).parent / "templates"

    def app_source(self):
        return self.templated_content(TEMPLATE_PATH / "app.py", site_url=self.site_url)

    def extra_context(self, project_overrides: dict[str, str]) -> dict[str, Any] | None:
        """Runs prior to other plugin hooks to provide additional context.

        This can be used to prompt the user with additional questions or run arbitrary
        logic to supplement the context provided to cookiecutter.

        :param project_overrides: Any overrides provided by the user as -Q options that
            haven't been consumed by the standard bootstrap wizard questions.
        """
        self.site_url = self.console.text_question(
            intro="What website would you like to make a site-specific browser for?",
            description="Site URL",
            default="",
            validator=validate_url,
            override_value=project_overrides.pop("site_url", None),
        )

        return {}
