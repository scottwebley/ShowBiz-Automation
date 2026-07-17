def build_movie_card(
    title: str,
    poster: str,
    content: str,
    trailer: str = "",
    platform: str = "",
    platform_logo: str = "",
    trailer_url: str = "",
    watch_url: str = "",
) -> str:
    """
    Build a single ShowBiz guide card.
    """

    platform_html = ""

    if platform:

        if platform_logo:

            platform_html = f"""
        <div class="showbiz-streaming-platform">

            <img
                src="{platform_logo}"
                alt="{platform}"
                class="showbiz-streaming-platform-logo">

            <span>{platform}</span>

        </div>
"""

        else:

            platform_html = f"""
        <div class="showbiz-streaming-platform">

            <strong>Streaming on:</strong> {platform}

        </div>
"""

    links_html = ""

    if trailer_url or watch_url:

        links_html = """
        <div class="showbiz-guide-links">
"""

        if trailer_url:

            links_html += f"""
            <a
                href="{trailer_url}"
                target="_blank"
                rel="noopener noreferrer"
                class="showbiz-guide-button">
                🎬 Official Trailer
            </a>
"""

        if watch_url:

            links_html += f"""
            <a
                href="{watch_url}"
                target="_blank"
                rel="noopener noreferrer"
                class="showbiz-guide-button">
                📺 Where to Watch
            </a>
"""

        links_html += """
        </div>
"""

    return f"""
<div class="showbiz-movie-card">

    <div class="showbiz-movie-poster">

        {poster}

    </div>

    <div class="showbiz-movie-info">

        <h3>{title}</h3>

{platform_html}

        <div class="showbiz-movie-content">

            {content}

        </div>

        <div class="showbiz-movie-trailer">

            {trailer}

        </div>

{links_html}

        <br>
        <br>

    </div>

</div>

<div class="showbiz-movie-divider"></div>
"""