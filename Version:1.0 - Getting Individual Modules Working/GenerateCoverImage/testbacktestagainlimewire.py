import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
LimeWire_Key = os.getenv("LimeWire_API_KEY")
Auth = "Bearer "+LimeWire_Key
print(Auth)

url = "https://api.limewire.com/api/image/generation"

payload = {
  "prompt": "Generate a cover image that can go along with this quote : Death is nothing, but to live defeated and inglorious is to die daily. No Text. Must be an Inspirational Image",
  "aspect_ratio": "16:9"
}

headers = {
  "Content-Type": "application/json",
  "X-Api-Version": "v1",
  "Accept": "application/json",
  "Authorization": Auth  # Replace with your actual Limewire API key
}

response = requests.post(url, json=payload, headers=headers)
print(response)
# # Check for successful response
# if response.status_code == 200:
#   try:
#     data = response.json()

#     # Save the JSON response
#     with open("response.json", "w") as outfile:
#       json.dump(data, outfile, indent=4)

#     # Access and process the image data
#     image_data = data["data"][0]  # Assuming one image is returned
#     image_url = image_data["asset_url"]

#     # Download the image
#     image_response = requests.get(image_url, stream=True)

#     if image_response.status_code == 200:
#       # Extract filename
#       filename = image_url.split("/")[-1]

#       # Save the image
#       with open(filename, "wb") as outfile:
#         for chunk in image_response.iter_content(1024):
#           outfile.write(chunk)

#       print(f"Image downloaded successfully: {filename}")
#     else:
#       print(f"Error downloading image: {image_response.status_code}")

#   except (KeyError, IndexError):
#     # Handle potential errors in JSON structure
#     print("Error parsing JSON response: Unexpected data format.")
#   except Exception as e:
#     # Catch unexpected errors
#     print(f"An unexpected error occurred: {e}")

# else:
#   # Handle API errors based on status code
#   error_message = ""
#   if response.status_code == 400:
#     error_message = "Bad request. Please check your prompt or parameters."
#   elif response.status_code == 401:
#     error_message = "Unauthorized. Please check your API key."
#   elif response.status_code == 429:
#     error_message = "Rate limit exceeded. Please try again later."
#   elif response.status_code == 500:
#     error_message = "Internal server error. Please try again later."
#   else:
#     error_message = f"Unknown API error: {response.status_code}"

#   print(f"Error generating image: {error_message}")
