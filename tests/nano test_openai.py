from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.responses.create(
    model="gpt-5",
    input="Give me 5 entertainment headlines."
)

print(response.output_text)