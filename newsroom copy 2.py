from engine.ai_news import get_top_stories
from engine.story_selector import select_top_story
from engine.local_story_selector import select_local_story
from engine.homepage_ranker import rank_homepage
from engine.editor import should_publish
from engine.ai_writer import write_article
from engine.image_selector import get_featured_image
from engine.wordpress import publish_post
from engine.story_consolidator import analyze_story_duplicates
from engine.trailer_enricher import enrich_article
from engine.link_enricher import enrich_links

from engine.pending_story import (
    save_pending_story,
    load_pending_story,
    clear_pending_story,
)

from engine.top_story_manager import (
    should_replace_top_story,
    retire_previous_top_stories,
)


def main():

    print("\n==============================")
    print("   SHOWBIZ AI NEWSROOM")
    print("==============================\n")

    pending_story = load_pending_story()
    is_pending_story = pending_story is not None

    if is_pending_story:

        print("Pending Top Story found.")
        print("Retrying previous article generation.\n")

        story = pending_story

    else:

        print("STEP 1: Fetching live entertainment news...")

        stories = get_top_stories()

        stories = analyze_story_duplicates(stories)

        if not stories:
            print("No stories found.")
            return

        print(f"✓ {len(stories)} stories downloaded.\n")

        print("STEP 2: Ranking homepage stories...")

        try:

            ranked = rank_homepage(stories)

            if not ranked:
                raise ValueError("Homepage Ranker returned no stories.")

            print("✓ Homepage Ranker completed.\n")

            print("Top Homepage Rankings:")

            for story in ranked[:11]:
                print(
                    f"#{story['homepage_rank']:>2} "
                    f"[{story.get('category', 'Unknown')}] "
                    f"{story.get('headline', '')}"
                )

            print()

            story = ranked[0]

        except Exception as e:

            print(f"⚠ Homepage Ranker failed: {e}")

            try:

                print("⚠ Falling back to AI Story Selector.\n")

                story = select_top_story(stories)

            except Exception as e:

                print(f"⚠ AI Story Selector failed: {e}")
                print("⚠ Falling back to Local Story Selector.\n")

                story = select_local_story(stories)

                if story is None:
                    print("No valid stories available.")
                    return

    print(f"Top Story: {story['headline']}")
    print(f"Category: {story['category']}\n")

    print("STEP 3: Editorial review...")

    if not is_pending_story:

        if not should_publish(story):

            print("\nCurrent Top Story remains the best story.")
            print("Nothing will be published.\n")
            return

        print("✓ Editorial approval granted.\n")

        if not should_replace_top_story(story):

            print("\nCurrent published Top Story remains the best story.")
            print("Publishing skipped.\n")
            return

        print("✓ Top Story Manager approved replacement.\n")

    else:

        print("✓ Pending story already approved. Continuing publication retry.\n")

    print("STEP 4: Writing article...")

    article = write_article(story)

    if article is not None:
        article = enrich_article(article, story)
        article["content"] = enrich_links(article["content"])

    if article is None:

        save_pending_story(story)

        print("\n========================================")
        print("NEWSROOM")
        print("========================================")
        print("Article generation failed.")
        print("Top Story saved for retry.")
        print("Publishing skipped.\n")

        return

    print("✓ Article complete.\n")

    print("STEP 5: Finding featured image...")

    article["image"] = get_featured_image(story)

    if not article["image"]:

        print("\nNo approved featured image found.")
        print("Generating AI editorial image...\n")

        from engine.image_generator import generate_image

        article["image"] = generate_image(story)

    if not article["image"]:

        save_pending_story(story)

        print("\n========================================")
        print("NEWSROOM")
        print("========================================")
        print("TOP STORY NOT PUBLISHED")
        print(f"Headline: {story['headline']}")
        print(f"Category: {story['category']}")
        print("Reason: AI image generation failed.")
        print("The article has been saved for retry.")
        print("Publishing skipped.\n")

        raise RuntimeError(
            f"Top Story aborted: AI image generation failed for '{story['headline']}'"
        )

    print("✓ Featured image ready.\n")

    print("STEP 6: Publishing to WordPress...")

    post = publish_post(article)

    if not post:

        print("\nPublishing failed.\n")
        return

    retire_previous_top_stories(post["id"])

    clear_pending_story()

    print("\n==============================")
    print("      SUCCESS")
    print("==============================")
    print(f"Post ID : {post['id']}")
    print(f"Title   : {post['title']['rendered']}")
    print(f"URL     : {post['link']}")
    print("==============================\n")


if __name__ == "__main__":
    main()