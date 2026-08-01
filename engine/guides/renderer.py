"""
ShowBiz Renderer

Standalone HTML renderer for previewing guides locally before publishing.
"""

from pathlib import Path
from string import Template
import subprocess


class Renderer:
    """Render ShowBiz guide previews."""

    def __init__(self):

        self.base = Path(__file__).parent

        self.templates = self.base / "templates"

        self.css_file = self.base / "showbiz.css"

    def load_css(self) -> str:

        if not self.css_file.exists():
            raise FileNotFoundError(self.css_file)

        return self.css_file.read_text(encoding="utf-8")

    def load_template(self, filename: str) -> Template:

        path = self.templates / filename

        if not path.exists():
            raise FileNotFoundError(path)

        return Template(
            path.read_text(encoding="utf-8")
        )

    def render_movie_card(self, movie: dict) -> str:

        template = self.load_template("movie_card.html")

        return template.safe_substitute(movie)

    def render_page(self, movies: list[dict]) -> str:

        cards = []

        for movie in movies:
            cards.append(
                self.render_movie_card(movie)
            )

        template = self.load_template("page.html")

        return template.safe_substitute(
            css=self.load_css(),
            cards="\n".join(cards),
        )

    def save_preview(
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

    def open_preview(self, html_file: Path):

        subprocess.run(
            [
                "open",
                "-a",
                "Safari",
                str(html_file),
            ],
            check=False,
        )