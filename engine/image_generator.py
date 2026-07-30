import re
import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import BadRequestError

from engine.openai_helper import (
    client,
    generate_image as openai_generate_image,
)

load_dotenv()

IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(exist_ok=True)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_prompt(story):
    category = story.get("category", "Entertainment")

    themes = {
        "Movies": "cinematic movie production and filmmaking",
        "Television": "television production and studio lighting",
        "Music": "live music performance and concert atmosphere",
        "Awards": "red carpet awards ceremony",
        "Style": "fashion photography and luxury style",
        "Theater": "stage performance and theatrical lighting",
    }

    theme = themes.get(category, "the entertainment industry")

    return f"""
Create an original premium editorial illustration.

Theme:
{theme}

The artwork should communicate the mood of an entertainment news story
without depicting any real people, celebrities, actors, musicians,
fictional characters, superheroes, movie scenes, TV scenes,
logos, trademarks, or copyrighted material.

Style:
• Premium entertainment magazine cover art
• Cinematic lighting
• Dramatic composition
• Rich blues, blacks and gold accents
• Wide 16:9 composition
• Highly detailed digital illustration
• Modern editorial artwork

Requirements:
• No people
• No faces
• No celebrity likenesses
• No copyrighted characters
• No movie costumes
• No text
• No logos
• No watermarks
• No UI elements

The image should be symbolic and atmospheric rather than literal.
"""


def generate_image(story):
    """
    Generates an editorial image and saves it locally.

    Returns:
        str: Path to the saved image.
        None: If image generation fails.
    """

    import traceback

    prompt = build_prompt(story)

    filename = slugify(story["headline"]) + ".png"
    filepath = IMAGE_DIR / filename

    try:

        print("\n========================================")
        print("AI IMAGE GENERATOR")
        print("========================================")
        print("Headline:", story["headline"])
        print("Generating image...\n")

        result = openai_generate_image(
            model="gpt-image-1",
            prompt=prompt,
            size="1536x1024",
        )

        if not result:
            print("❌ OpenAI returned no result.")
            return None

        if not getattr(result, "data", None):
            print("❌ OpenAI returned no image data.")
            print(result)
            return None

        if not result.data[0].b64_json:
            print("❌ OpenAI returned empty image data.")
            print(result)
            return None

        image_bytes = base64.b64decode(result.data[0].b64_json)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print(f"✓ Image saved: {filepath}")

        return str(filepath)

    except BadRequestError:

        print("\n❌ OpenAI rejected the image request:\n")
        traceback.print_exc()
        return None

    except Exception:

        print("\n❌ Unexpected image generation error:\n")
        traceback.print_exc()
        return None


if __name__ == "__main__":

    story = {
        "headline": "Christopher Nolan Announces New Epic Film",
        "summary": "Award-winning filmmaker Christopher Nolan has revealed details of his next feature.",
        "category": "Movies"
    }

    image = generate_image(story)

    print(image)