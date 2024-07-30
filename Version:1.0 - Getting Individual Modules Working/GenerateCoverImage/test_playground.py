import requests
import json
import random
import os
from dotenv import load_dotenv

url = "https://api.limewire.com/api/image/generation"
load_dotenv()
LimeWire_Key = os.getenv("LimeWire_API_KEY")
Auth = "Bearer "+LimeWire_Key

with open("Quotes.json", "r") as f:
    quotes_data = json.load(f)
random_quote = random.choice(quotes_data)

prompt = f"""Generate an artistic cover image that can go along with this quote: 
"{random_quote["quote"]}" by {random_quote["author"]}.
The image should be visually appealing and evoke a sense of motivation or upliftment. 
The image should be acceptable and non harmful. Do not respond with null. 
You must provide an image output to comply with further workflow"""

payload = {
  "prompt": prompt,
  "aspect_ratio": "1:1"
}

headers = {
  "Content-Type": "application/json",
  "X-Api-Version": "v1",
  "Accept": "application/json",
  "Authorization": Auth  
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

def extract_image_url(response):
  """
  Extracts the image URL from a Limewire API response (dictionary).

  Args:
      response: A dictionary containing the API response data.

  Returns:
      The image URL as a string, or None if the status is not 200 or there's no image data.
  """
  # Check if the status is 200 (success)
  if response.get("status") == 200:
    # Get the data list
    data = response.get("data")

    # Check if data exists and is a list
    if data and isinstance(data, list):
      # Assuming the first element in the data list contains the image information
      image_data = data[0]

      # Extract the image URL
      image_url = image_data.get("asset_url")
      return image_url
  else:
    # Handle non-200 status codes (e.g., print an error message)
    print(f"Error: API request failed with status {response.get('status')}")
    return None

image_url = extract_image_url(data)

if image_url:
  print("Image URL:", image_url)
else:
  print("No image URL found.")