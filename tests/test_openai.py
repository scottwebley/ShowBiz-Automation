from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.responses.create(
    model="gpt-5.5",
    input="Give me 5 entertainment headlines."
)

print(response.output_text)
