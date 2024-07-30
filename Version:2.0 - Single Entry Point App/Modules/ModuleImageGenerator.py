# GeminiBlog-Version:2.0/Modules/ModuleImageGenerator.py
import os
import requests
import json
import logging
import vertexai
from vertexai.preview import vision_models
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

# Configure logging
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')


# # Function to generate an image Only Limewire works since GoogleImaGen API is closed now. DallE needs Licnese
def generate_image_from_source( quote: str, image_source : str, media_dir: str) -> str:  # Add quote as an argument
    if image_source == 'LimewireImage':
        return Limewire_Image_Generator(quote, media_dir)
    elif image_source == 'StabilityAIImage':
        return StableDiffusionImageGenerator(quote, media_dir)
    elif image_source == 'ImagenImage':
        return Google_Imagen_Generator(quote, media_dir)
    else:
        logging.error(f"Invalid image source: {image_source}")
        print(f"Invalid image source: {image_source}")
        return "https://placehold.co/600x400/png"  # Default placeholder image URL

def Limewire_Image_Generator(quote: str, media_dir: str) -> str:
    LimeWire_Key = os.getenv("LimeWire_API_KEY")
    url = "https://api.limewire.com/api/image/generation"
    payload = {
        "prompt": f"Generate a cover image that can go along with this quote : {quote}. There should be no text.  Inspirational. Astrictic",
        "aspect_ratio": "3:2"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": "Bearer " + LimeWire_Key
    }
    logging.info(f"Sending image generation request to Limewire API with payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if data and data['status'] == "COMPLETED" and 'asset_url' in data['data'][0]:
        logging.info("Image Generation - Success!")
        logging.info(f"You have {data['credits_remaining']} credits remaining.")
        print("Image Generation - Success!")
        print(f"You have {data['credits_remaining']} credits remaining.")
        image_url = data['data'][0]['asset_url']
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Construct the image file path
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            image_file_path = os.path.join(media_dir, f"{timestamp}.png")  # Use a unique filename

            # Save the image to the media directory
            with open(image_file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            logging.info(f"Image downloaded and saved to: {image_file_path}")
            print(f"Image downloaded and saved to: {image_file_path}")
            return os.path.basename(image_file_path)  # Return the filename
        else:
            logging.error(f"Error downloading image: {response.status_code}")
            print(f"Error downloading image: {response.status_code}")
            return "https://placehold.co/600x400/png"  # Default placeholder image URL
    else:
        logging.error("Image Generation - Failed.")
        logging.error(response.text)
        logging.error("Please check if you exceeded you Limewire Daily Free Credit")
        logging.error("Image Generation - Failed. Defaulting to placeholder image.")
        print(response.text)
        print("Please check if you exceeded you Limewire Daily Free Credit")
        print("Image Generation - Failed. Defaulting to placeholder image.")
        return "https://placehold.co/600x400/png"  # Default placeholder image URL

def StableDiffusionImageGenerator(quote: str, media_dir: str) -> str:
    # Implement logic for Stable Diffusion image generation
    # ...
    # Return the image URL
    return "https://placehold.co/600x400/png"  # Placeholder for now


# Code used from https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/generative_ai/imagen
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def Google_Imagen_Generator(quote: str, media_dir: str) -> str:
    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel
    project_id = os.getenv("GCP_PROJECT_ID")
    #output_file = "temp.png"  # Remove this line
    vertexai.init(project=project_id, location="us-central1")
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    images = model.generate_images(
        prompt=f"Generate a artistic cover image that conveys s beautiful image that can convery this message : {quote}. There should be no text.  Inspirational. Astrictic. Incase any words violate Google's Responsible AI practices, respond with something acceptable to general audience.",
        number_of_images=1,
        aspect_ratio="4:3",  # 4:3 aspect ratio
        safety_filter_level="block_some",  # No blocking
        person_generation="dont_allow"  # Don't allow person generation
    )
    
    # Assign a value to image_file_path before using it
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_file_path = os.path.join(media_dir, f"{timestamp}.png")  # Use a unique filename

    images[0].save(location=image_file_path, include_generation_parameters=False)  # Use image_file_path here
    # Download the image
    with open(image_file_path, 'rb') as f:
        response = f.read()
    if response:
        # Save the image to the media directory
        with open(image_file_path, 'wb') as f:
            f.write(response)
        logging.info(f"Image downloaded and saved to: {image_file_path}")
        print(f"Image downloaded and saved to: {image_file_path}")
        return os.path.basename(image_file_path)  # Return the filename
    else:
        logging.error(f"Error downloading image: {response.status_code}")
        print(f"Error downloading image: {response.status_code}")
        return "https://placehold.co/600x400/png"  # Default placeholder image URL

# if __name__ == "__main__":
#     quote = "The mind is everything. What you think you become. - Buddha"
#     image_url = generate_image_from_source(quote, 'ImagenImage', '/tmp')
#     print("Generated Image URL: ", image_url)
