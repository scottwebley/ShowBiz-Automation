"""
===========================================
ShowBiz Movie Card Builder
Version 1.1
===========================================

Purpose:
    Build the HTML structure for individual
    movie guide cards.

Does NOT:
    - Fetch data
    - Call APIs
    - Publish content
    - Apply CSS

Author:
    ShowBiz Automation
"""


def build_movie_card(
    title: str,
    poster: str,
    content: str,
    trailer: str = "",
) -> str:
    """
    Build a single movie card.
    """

    return f"""
<div class="showbiz-movie-card">

    <div class="showbiz-movie-poster">

        {poster}

    </div>


    <div class="showbiz-movie-info">

        <h3>{title}</h3>

        <div class="showbiz-movie-content">

            {content}

        </div>


        <div class="showbiz-movie-trailer">

            {trailer}

        </div>

    </div>

</div>


<div class="showbiz-movie-divider"></div>
"""


if __name__ == "__main__":

    print(
        build_movie_card(
            title="Superman",
            poster="<img src='poster.jpg'>",
            content="<p>Action adventure.</p>",
            trailer="<a>Trailer</a>",
        )
    )