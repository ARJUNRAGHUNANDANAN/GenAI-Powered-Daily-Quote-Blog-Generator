import os
from dotenv import load_dotenv
from openai import OpenAI

# Load credentials
load_dotenv()
API_KEY = os.getenv("OpenAI_KEY")
client = OpenAI(api_key=API_KEY)
if not API_KEY:
    raise ValueError("OpenAI API key not found. Ensure it's set in the environment variables.")

#Setting Prompt
quote = "The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart. - Helen Keller"
prompt_statement = f"An inspirational cover image in low resolution (320x180) for the quote: '{quote}'. " \
                   f"The image should be visually appealing and evoke a sense of motivation or upliftment."

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt_statement,
  size="1024x1024",
  quality="standard",
  n=1,
)
# Extract and print the image URL
# image_url = response.data[0].url
# print(image_url)
print(response.data[0].message())