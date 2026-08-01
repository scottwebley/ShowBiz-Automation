"""
ShowBiz Guide Preview

Creates a standalone preview HTML page for local review before
publishing to WordPress.
"""

from pathlib import Path
from string import Template
import subprocess


class Preview:
    """Generate and open a local HTML preview."""

    def __init__(self):

        self.base = Path(__file__).parent

        self.templates = self.base / "templates"

        self.css_file = self.base / "showbiz.css"

    def load_css(self) -> str:

        return self.css_file.read_text(
            encoding="utf-8"
        )

    def load_template(
        self,
        filename: str,
    ) -> Template:

        path = self.templates / filename

        return Template(
            path.read_text(
                encoding="utf-8"
            )
        )

    def build(
        self,
        title: str,
        body_html: str,
    ) -> str:

        template = self.load_template(
            "page.html"
        )

        return template.safe_substitute(
            title=title,
            css=self.load_css(),
            cards=body_html,
        )

    def save(
        self,
        html: str,
        filename: str = "test_movies.html",
    ) -> Path:

        output = Path.cwd() / filename

        output.write_text(
            html,
            encoding="utf-8",
        )

        return output

    def open(
        self,
        html_file: Path,
    ) -> None:

        subprocess.run(
            [
                "open",
                "-a",
                "Safari",
                str(html_file),
            ],
            check=False,
        )

    def preview(
        self,
        title: str,
        body_html: str,
        filename: str = "test_movies.html",
    ) -> Path:

        html = self.build(
            title,
            body_html,
        )

        output = self.save(
            html,
            filename,
        )

        self.open(output)

        return output