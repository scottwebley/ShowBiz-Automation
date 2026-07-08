"""
===========================================
ShowBiz Homepage Validator
Version 1.0
===========================================

Purpose:
    Validate the AI homepage ranking
    response returned by GPT.

Author:
    ShowBiz Automation
"""

import json


def validate_homepage_ranking(result, story_count):
    """
    Validate the AI response and return
    the homepage ranking list.

    Args:
        result (str): Raw AI response.
        story_count (int): Number of stories.

    Returns:
        list[int]
    """

    result = result.strip()

    #
    # Remove markdown fences.
    #

    if result.startswith("```"):

        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]

    data = json.loads(result)

    if "homepage_ranking" not in data:

        raise ValueError(
            "AI response missing 'homepage_ranking'"
        )

    ranking = data["homepage_ranking"]

    if not isinstance(ranking, list):

        raise ValueError(
            "'homepage_ranking' must be a list."
        )

    if len(ranking) != story_count:

        raise ValueError(
            f"Expected {story_count} ranked stories, "
            f"received {len(ranking)}."
        )

    seen = set()

    for index in ranking:

        if not isinstance(index, int):

            raise ValueError(
                f"Invalid index type: {index}"
            )

        if index < 0 or index >= story_count:

            raise ValueError(
                f"Invalid story index: {index}"
            )

        if index in seen:

            raise ValueError(
                f"Duplicate story index: {index}"
            )

        seen.add(index)

    expected = set(range(story_count))

    missing = expected - seen

    if missing:

        raise ValueError(
            f"Missing story indices: "
            f"{sorted(missing)}"
        )

    return ranking