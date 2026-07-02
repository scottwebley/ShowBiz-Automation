from engine.ai_news import get_top_stories
from engine.story_selector import select_top_story
from engine.local_story_selector import select_local_story
from engine.homepage_ranker import rank_homepage
from engine.editor import should_publish
from engine.ai_writer import write_article
from engine.image_selector import get_featured_image
from engine.wordpress import publish_post


def main():

    print("\n==============================")
    print("   SHOWBIZ AI NEWSROOM")
    print("==============================\n")

    # -------------------------------------------------
    # STEP 1
    # -------------------------------------------------

    print("STEP 1: Fetching live entertainment news...")

    stories = get_top_stories()

    if not stories:
        print("No stories found.")
        return

    print(f"✓ {len(stories)} stories downloaded.\n")

    # -------------------------------------------------
    # STEP 2
    # -------------------------------------------------

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

    # -------------------------------------------------
    # STEP 3
    # -------------------------------------------------

    print("STEP 3: Editorial review...")

    if not should_publish(story):

        print("\nCurrent Top Story remains the best story.")
        print("Nothing will be published.\n")

        return

    print("✓ Editorial approval granted.\n")

    # -------------------------------------------------
    # STEP 4
    # -------------------------------------------------

    print("STEP 4: Writing article...")

    article = write_article(story)

    if article is None:

        print("\n========================================")
        print("NEWSROOM")
        print("========================================")
        print("Article generation failed.")
        print("Publishing skipped.\n")

        return

    print("✓ Article complete.\n")
        # -------------------------------------------------
    # STEP 5
    # -------------------------------------------------

    print("STEP 5: Generating featured image...")

    article["image"] = get_featured_image(story)

    print("✓ Featured image generated.\n")

    # -------------------------------------------------
    # STEP 6
    # -------------------------------------------------

    print("STEP 6: Publishing to WordPress...")

    post = publish_post(article)

    if not post:

        print("\nPublishing failed.\n")

        return

    # -------------------------------------------------
    # DONE
    # -------------------------------------------------

    print("\n==============================")
    print("      SUCCESS")
    print("==============================")
    print(f"Post ID : {post['id']}")
    print(f"Title   : {post['title']['rendered']}")
    print(f"URL     : {post['link']}")
    print("==============================\n")


if __name__ == "__main__":
    main()