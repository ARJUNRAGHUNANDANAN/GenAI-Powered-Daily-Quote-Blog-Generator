#GeminiBlog/Modules/ModuleImageGenerator.py
# @arjunraghunandanan 2024

# Vertex AI's logging and Python's Logging causes issues with each other which misses up some logs. Currently I have resorted to just leaving both loggers running so some log lines will be duplicated.  

# Reference Content URLS
# https://docs.limewire.com/#operation/generateImage
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/imagen-api
# https://platform.stability.ai/docs/api-reference#tag/Generate/paths

import os
import requests
import json
import shutil
import logging
import subprocess
import vertexai
#from absl import logging as absl_logging
#absl_logging.set_verbosity(absl_logging.ERROR)
from vertexai.preview import vision_models
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

# Configure logging
logging.basicConfig(filename='logs/all_generated_runs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

# Placeholder image URL
PLACEHOLDER_IMAGE_URL = "https://placehold.co/600x400/png"

# Download and save placeholder image
def download_placeholder_image(media_dir: str) -> str:
    response = requests.get(PLACEHOLDER_IMAGE_URL, stream=True)
    if response.status_code == 200:
        logging.info(f"Received Placeholder image. Status Code: {response.status_code}")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_file_path = os.path.join(media_dir, f"{timestamp}_placeholder.png")
        with open(image_file_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        logging.info(f"Placeholder image downloaded and saved to: {image_file_path}")
        return image_file_path
    else:
        logging.error(f"Error downloading placeholder image: {response.status_code}")
        return None
    return image_file_path

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
        # Download and return placeholder image file path
        placeholder_image_path = download_placeholder_image(media_dir)
        print(placeholder_image_path)
        if placeholder_image_path:
            print(os.path.basename(placeholder_image_path))
            return os.path.basename(placeholder_image_path)
        else:
            return None  # Default placeholder image URL

def Limewire_Image_Generator(quote: str, media_dir: str) -> str:
    LimeWire_Key = os.getenv("LimeWire_API_KEY")
    url = "https://api.limewire.com/api/image/generation"
    payload = {
        "prompt": f"Generate a captivating, visually striking image that embodies the essence of the following quote: {quote}. The image should evoke the core theme of the quote in a visually compelling way. Utilize a cinematic composition, rich colors, and attention to detail. Consider incorporating symbolic elements or metaphors to enhance the image's impact.",
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
            # Download and return placeholder image file path
            placeholder_image_path = download_placeholder_image(media_dir)
            if placeholder_image_path:
                return os.path.basename(placeholder_image_path)
            else:
                return PLACEHOLDER_IMAGE_URL  # Default placeholder image URL
    else:
        logging.error("Image Generation - Failed.")
        logging.error(response.text)
        logging.error("Please check if you exceeded you Limewire Daily Free Credit")
        logging.error("Image Generation - Failed. Defaulting to placeholder image.")
        print(response.text)
        print("Please check if you exceeded you Limewire Daily Free Credit")
        print("Image Generation - Failed. Defaulting to placeholder image.")
        # Download and return placeholder image file path
        placeholder_image_path = download_placeholder_image(media_dir)
        if placeholder_image_path:
            return os.path.basename(placeholder_image_path)
        else:
            return PLACEHOLDER_IMAGE_URL  # Default placeholder image URL

# Created based on Official StabilityAI Documentation. 
# https://platform.stability.ai/docs/api-reference#tag/Generate/paths/~1v2beta~1stable-image~1generate~1core/post
def StableDiffusionImageGenerator(quote: str, media_dir: str) -> str:
    Stability_Key = os.getenv("StabilityAI_API_KEY")
    if not Stability_Key:
        logging.error("StabilityAI_API_KEY not set in environment variables.")
        return ""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_file_path = os.path.join(media_dir, f"{timestamp}.png")
    
    logging.info("Sending request to Stability AI API...")
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
        "Authorization": "Bearer "+ Stability_Key,
        "Accept": "image/*"
    }   ,
        files={"none": (None, '')},  # Ensure the request is multipart/form-data
        data={
        "prompt": "Generate a captivating, visually striking image that embodies the essence of the following quote: {quote}. The image should evoke the core theme of the quote in a visually compelling way. Utilize a cinematic composition, rich colors, and attention to detail. Consider incorporating symbolic elements or metaphors to enhance the image's impact.",
        "output_format": "png","aspect_ratio": "3:2",
        }
    )
    logging.info("Received response with status code: {response.status_code}")
    logging.debug("Response content: {response.content}")
    
    if response.status_code == 200:
        with open(image_file_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"Image downloaded and saved to: {image_file_path}")
        return os.path.basename(image_file_path)
    else:
        logging.error(f"Error generating image: {response.status_code}")
        logging.error(response.text)
        raise Exception(response.json())

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
    #import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel
    project_id = os.getenv("GCP_PROJECT_ID")
    #output_file = "temp.png"  # Remove this line
    vertexai.init(project=project_id, location="us-central1")
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    images = model.generate_images(
        prompt=f"Generate a captivating, visually striking image that embodies the essence of the following quote: {quote}. The image should evoke the core theme of the quote in a visually compelling way. Utilize a cinematic composition, rich colors, and attention to detail. Consider incorporating symbolic elements or metaphors to enhance the image's impact.",
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
        # Download and return placeholder image file path
        placeholder_image_path = download_placeholder_image(media_dir)
        if placeholder_image_path:
            return os.path.basename(placeholder_image_path)
        else:
            return PLACEHOLDER_IMAGE_URL  # Default placeholder image URL

if __name__ == "__main__":
    quote = "The mind is everything. What you think you become. - Buddha"
    image_url = generate_image_from_source(quote, 'LimewireImage', '/home/{cloudusername}}/GeminiBlog-Run/_site/content')
    print("Generated Image URL: ", image_url)

