from __future__ import annotations

from typing import Any

from briefcase.bootstraps import TogaGuiBootstrap
from briefcase.config import validate_url


class SiteSpecificPositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    def app_source(self):
        return f"""\
import toga


class {{{{ cookiecutter.class_name }}}}(toga.App):

    def startup(self):
        self.web_view = toga.WebView()
        self.web_view.url = f"{self.site_url}"

        self.main_window = toga.MainWindow()
        self.main_window.content = self.web_view
        self.main_window.show()


def main():
    return {{{{ cookiecutter.class_name }}}}()
"""

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
