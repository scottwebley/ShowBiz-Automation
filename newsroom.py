from engine.news_selector import select_story
from engine.ai_writer import write_article
from engine.wordpress import publish_post


def main():
    print("\n🎬 ShowBiz AI Newsroom\n")

    story = select_story()

    article = write_article(story)

    publish_post(article)

    print("\n✅ Today's Top Story Published")


if __name__ == "__main__":
    main()