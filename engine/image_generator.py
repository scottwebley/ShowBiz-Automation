import re
import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, BadRequestError

load_dotenv()

client = OpenAI()

IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(exist_ok=True)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_prompt(story):
    category = story.get("category", "Entertainment Industry")

    return f"""
Create a premium editorial illustration for an entertainment news website.

Story headline:
{story["headline"]}

Story summary:
{story["summary"]}

Category:
{category}

STYLE

• Premium entertainment magazine artwork
• Cinematic lighting
• Rich blacks, blues and purples
• Modern, dramatic composition
• Wide 16:9 composition
• Professional editorial illustration

IMPORTANT

• NO text
• NO headlines
• NO logos
• NO watermarks
• NO UI elements
• NO celebrity likenesses
• NO copyrighted characters
• Focus on the atmosphere and theme of the story rather than specific people.
"""


def generate_image(story):
    """
    Generates an editorial image and saves it locally.

    Returns:
        str: Path to the saved image.
        None: If image generation fails.
    """

    prompt = build_prompt(story)

    filename = slugify(story["headline"]) + ".png"
    filepath = IMAGE_DIR / filename

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1536x1024"
        )

        image_bytes = base64.b64decode(result.data[0].b64_json)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print(f"✓ Image saved: {filepath}")

        return str(filepath)

    except BadRequestError as e:
        print("\n⚠ AI image generation blocked.")
        print(e)
        print("Continuing without a generated image.\n")
        return None

    except Exception as e:
        print("\n⚠ Image generation failed.")
        print(e)
        print("Continuing without a generated image.\n")
        return None


if __name__ == "__main__":

    story = {
        "headline": "Christopher Nolan Announces New Epic Film",
        "summary": "Award-winning filmmaker Christopher Nolan has revealed details of his next feature.",
        "category": "Movies"
    }

    image = generate_image(story)

    print(image)