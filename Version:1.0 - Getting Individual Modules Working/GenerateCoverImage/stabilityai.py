import os
import requests
from datetime import datetime
Stability_Key  = os.getenv("Stability_Key")
# Created based on Official StabilityAI Documentation. 
# https://platform.stability.ai/docs/api-reference#tag/Generate/paths/~1v2beta~1stable-image~1generate~1core/post
def StableDiffusionImageGenerator(quote: str, media_dir: str) -> str:
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "Authorization": f"Bearer {Stability_Key}",
        "Accept": "image/*",
    }
    data = {
        "prompt": quote,
        "output_format": "png"
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        image_file_path = os.path.join(media_dir, f"{timestamp}.png")
        with open(image_file_path, 'wb') as file:
            file.write(response.content)
        return os.path.basename(image_file_path)
    else:
        None

if __name__ == "__main__":
    quote = "The mind is everything. What you think you become. - Buddha"
    image_url = StableDiffusionImageGenerator(quote, '/Dev')
    print("Generated Image URL: ", image_url)

