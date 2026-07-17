"""
engine/featured_entertainer_pipeline.py

PART 1 OF 2
"""

from engine.featured_entertainer import (
    generate_featured_entertainer,
)

from engine.featured_entertainer_profile import (
    generate_featured_entertainer_profile,
)

from engine.featured_entertainer_writer_v3 import (
    write_featured_entertainer,
)

from engine.image_selector import (
    get_featured_image,
)

from engine.wordpress import (
    publish_post,
)


CATEGORY_ID = 63


def build_featured_package(stories):
    """
    Select this week's Featured Entertainer,
    build the profile, and generate the HTML.
    """

    print(
        "STEP 2: AI editorial analysis..."
    )

    report = generate_featured_entertainer(
        stories
    )

    if report is None:

        print(
            "\nFeatured Entertainer "
            "generation failed.\n"
        )

        return None

    profile = (
        generate_featured_entertainer_profile(
            report
        )
    )

    if profile is None:

        print(
            "\nFeatured profile "
            "generation failed.\n"
        )

        return None

    print(
        "✓ Featured Entertainer selected.\n"
    )

    print(
        "STEP 3: Writing HTML article..."
    )

    article = write_featured_entertainer(
        profile
    )

    print(
        "✓ HTML article created.\n"
    )

    return {
        "report": report,
        "profile": profile,
        "article": article,
    }


def attach_featured_image(
    package,
    stories,
):
    """
    Select the featured image and attach
    it to the article.
    """

    report = package["report"]
    article = package["article"]

    image_story = report.get(
        "source_story"
    )

    if image_story is None:
        image_story = stories[0]

    print(
        "STEP 4: Selecting featured image..."
    )

    image = get_featured_image(
        image_story
    )

    if image:

        article["image"] = image

        print(
            "✓ Featured image selected.\n"
        )

    else:

        print(
            "⚠ No featured image available."
        )

    return package


def publish_featured_package(
    package,
):
    """
    Publish the completed article.
    """

    article = package["article"]

    article["category_id"] = (
        CATEGORY_ID
    )

    print(
        "STEP 5: Publishing article..."
    )

    post = publish_post(
        article
    )

    if not post:

        print(
            "\nPublication failed.\n"
        )

        return None

    package["post"] = post

    return package
def finish_featured_package(
    package,
    save_featured_entertainer,
    archive_featured_entertainer,
    current_editorial_week,
):
    """
    Save homepage data, archive the article,
    and display the publication summary.
    """

    report = package["report"]
    profile = package["profile"]
    article = package["article"]
    post = package["post"]

    save_featured_entertainer(
        report=report,
        post=post,
        week=current_editorial_week(),
    )

    archive_featured_entertainer(
        profile,
        article,
    )

    print("\n==============================")
    print(" FEATURED ENTERTAINER PUBLISHED")
    print("==============================")
    print(f"Post ID : {post['id']}")
    print(
        f"Title   : "
        f"{post['title']['rendered']}"
    )
    print(
        f"URL     : "
        f"{post['link']}"
    )
    print("==============================\n")

    return post


def run_featured_pipeline(
    stories,
    save_featured_entertainer,
    archive_featured_entertainer,
    current_editorial_week,
):
    """
    Execute the complete Featured
    Entertainer publishing pipeline.
    """

    package = build_featured_package(
        stories
    )

    if package is None:
        return None

    package = attach_featured_image(
        package,
        stories,
    )

    package = publish_featured_package(
        package,
    )

    if package is None:
        return None

    finish_featured_package(
        package,
        save_featured_entertainer,
        archive_featured_entertainer,
        current_editorial_week,
    )

    return package["post"]