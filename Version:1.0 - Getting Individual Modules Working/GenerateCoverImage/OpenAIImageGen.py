import os
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()

# Configure OpenAI API key (replace with your actual key)
load_dotenv()
API_KEY  = os.getenv("OpenAI_API_KEY")

def generate_cover_image(quote, width=320, height=180):

  # Ensure aspect ratio is 16:9
  if width / height != 16 / 9:
    print(" Warning : Image dimensions must maintain a 16:9 aspect ratio.")

  # Craft a clear and concise prompt that incorporates design elements
  prompt = f"An inspirational cover image in low resolution (320x180) for the quote: '{quote}'. " \
          f"The image should be visually appealing and evoke a sense of motivation or upliftment."

  # Use a smaller response size for low-resolution images and avoid exceeding API limits
  response = client.images.generate(prompt=prompt,
  n=1,
  size=f"{width}x{height}",
  response_format="url")
  print(response.json.data[0].url)
#   # Handle potential errors and return the image URL if successful
#   if response.status_code == 200:
#     return response.json["data"][0]["url"]
#   else:
#     print(f"Error generating image: {response.status_code} - {response.json['error']['message']}")
#     return None

# # Example usage (replace with your inspirational quote)
quote = "The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart. - Helen Keller"
image_url = generate_cover_image(quote)

# if image_url:
#   # Extract filename from URL (assuming a common naming convention)
#   filename = image_url.split("/")[-1]

#   try:
#     # Download the image using an appropriate library (e.g., requests)
#     # Replace the following line with your preferred image download method
#     # response = requests.get(image_url, stream=True)
#     # response.raw.decode_content = True
#     # with open(filename, 'wb') as f:
#     #   for chunk in response.iter_content(1024):
#     #     f.write(chunk)
#     print(f"Image successfully generated: {filename}")
#   except Exception as e:
#     print(f"Error downloading image: {e}")
# else:
#   print("Failed to generate image.")


