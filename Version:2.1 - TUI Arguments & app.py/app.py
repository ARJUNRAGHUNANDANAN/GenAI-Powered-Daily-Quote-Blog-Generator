# @arjunraghunandanan 2024

import argparse
import os
import json
import requests
import sys
import shutil
import subprocess
import logging
from typing import Dict, Any
from datetime import datetime
import dotenv
from dotenv import load_dotenv

# remove time after doing dummy run.
# import time

#Importing My Modules
import Modules.ModuleGetDailyQuotes as ModuleGetDailyQuotes
import Modules.ModulePoemGenerator as ModulePoemGenerator
import Modules.ModuleImageGenerator as ModuleImageGenerator
import Modules.ModulePelicanController as ModulePelicanController
import Modules.ModuleFirebaseController as ModuleFirebaseController

# Configure logging to reduce headaches when code break
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

# Commeting Out Temporarily to Parameterize Code
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Commented out to replace with parameterised code
#GCP_PROJECT_ID = 'yourprojectid'
#GCP_PROJECT_ID will be also used as firebase_project_id
#GCP_LOCATION = 'location'
#poem_source = 'Gemini'
# 'Gemini', 'OpenAI', 'Perplexity' - Only Gemini Works at the Moment.
#image_source = 'LimewireImage' 
# 'LimewireImage', 'StabilityAIImage', 'ImagenImage' - Only LimewireImage & ImagenImage Works at the Moment.
#quote_source = 'ZenQuotesIO'
#'QuotablesIO', 'LocalQuoteIO', 'ZenQuotesIO - All Are Functional

def main(GCP_PROJECT_ID: str, quote_source: str, poem_source: str, image_source: str) -> None:
    """Main function to run the blog generation process."""
    print(GCP_PROJECT_ID, quote_source, poem_source, image_source)
    start_time = datetime.now()
    logging.info(f"Application Run Attempt Started at {start_time}")
    print(f"Application Run Attempt Started at {start_time}")
    logging.info("Setting Up Directory")
    print("-" * 30)
    print("Setting Up Directory")
    print("-" * 30)
    #Enable Vertex AI API
    if image_source == 'Gemini':
        print("Enabling Vertex AI API")
        #time.sleep(5)
    subprocess.run(f"gcloud services enable aiplatform.googleapis.com", shell=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_home_directory = subprocess.check_output("echo ~", shell=True).decode("utf-8").strip()
    pelican_content_dir = os.path.join(current_dir, "pelican-CMS", "_site", "content")
    media_dir = os.path.join(pelican_content_dir, "media")
    pelican_deployer_dir = os.path.join(current_dir, "pelican-CMS", "_site")
    logging.info(f"Setting User Home Directory: {user_home_directory}")
    logging.info(f"Setting Pelican Content Directory: {pelican_content_dir}")
    logging.info(f"Setting Pelican Attached Media Directory: {media_dir}")
    logging.info(f"Setting Pelican Deployer  Directory: {pelican_deployer_dir}")
    print(f"Setting User Home Deployer Directory: {user_home_directory}")
    print(f"Setting Pelican Content Directory: {pelican_content_dir}")
    print(f"Setting Pelican Attached Media Directory: {media_dir}")
    print(f"Setting Pelican Deployer Directory: {pelican_deployer_dir}")

    # Create directories if they don't exist
    os.makedirs(pelican_content_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(pelican_deployer_dir, exist_ok=True)

    old_path = os.environ["PATH"]
    logging.info(f"PATH before adding local/bin {old_path}")
    print("Adding /.local/bin to PATH if not already present")
    local_bin_path = os.path.join(user_home_directory, ".local", "bin")
    if local_bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"] + f":{local_bin_path}"
        logging.info(f"Local Bin was not present, appending {local_bin_path}")
    modified_path = os.environ["PATH"]
    logging.info(f"PATH after adding local/bin{modified_path}")
    
    logging.info("Fetching Daily Quote")
    print("-" * 30)
    print("Fetching Daily Quote")
    print("-" * 30)
    #time.sleep(5)
    quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(quote_source)  # ed
    quote = quote_data.get("quote", "")
    author = quote_data.get("author", "")
    quote_from = quote_data.get("source", "")
    logging.info(f"Quote: {quote}")
    logging.info(f"Author: {author}")

    #time.sleep(5)
    logging.info("Generating Poem")
    print("-" * 30)
    print("Generating Poem")
    print("-" * 30)
    poem = ModulePoemGenerator.generate_poem_from_source(quote+ "by" + author, poem_source)
    logging.info(f"Poem: {poem}")
    # print(poem)

    #time.sleep(5)
    logging.info("Generating Image")
    print("-" * 30)
    print("Generating Image")
    print("-" * 30)
    # Generate image
    image_file_name = ModuleImageGenerator.generate_image_from_source(quote, image_source, media_dir)  # Pass the correct media directory
    logging.info(f"Image file name: {image_file_name}")
    # print(image_file_name)
    #sys.exit("Things were working well till now")

    if image_file_name and poem and quote_data:
    #if True:
        print("Combining Blog Post")
        print("-" * 30)

        # Generate markdown content
        markdown_content = ModulePelicanController.generate_combined_markdown(quote, author,  poem, image_file_name, quote_source, poem_source, image_source , datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Create the markdown file directly in the pelican_content_dir
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        markdown_file_path = os.path.join(pelican_content_dir, f"{timestamp}.md")
        with open(markdown_file_path, "w") as f:
            f.write(markdown_content)
        logging.info(f"Markdown file created at: {markdown_file_path}")
        # console.print(f"Markdown file created at: {markdown_file_path}")

        logging.info("Running Pelican to generate HTML output.")
        print("-" * 30)
        ModulePelicanController.pelican_MDmedia_to_output()
        # Pelican's "make html" step to generate final html in pelican_deployer_dir/output from pelican_deployer_dir/content
        #time.sleep(5)
        
        print("Blog Post Generation Complete!")
        pelican_output_dir = os.path.join(pelican_deployer_dir, "output")
        logging.info("Static HTML Files for hosting will be present in", pelican_output_dir)
        logging.info("-" * 30)

        logging.info("copying generated images from content/media to output/media")
        # Copy media files to the output directory
        output_media_dir = os.path.join(pelican_output_dir, "media")
        shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)
        logging.info(f"Media files copied to: {output_media_dir}")
        #print(f"Media files copied to: {output_media_dir}")

        #sys.exit("Good till Now")
        # Deploy blog post
        print("-" * 30)
        print("Deploying Pelican output to Firebase.")
        logging.info("Deploying Pelican output to Firebase.")
        print("-" * 30)
        #time.sleep(5)

        ModuleFirebaseController.deploy_to_firebase(pelican_deployer_dir, GCP_PROJECT_ID)
        logging.info("Blog post should be generated and deployed successfully!")
        print("Blog post should be generated and deployed successfully!")
        print("-" * 30)
    else:
        # logging.error("Blog Post Generation Failed.")
        print("-" * 30)
        print("Blog Post Generation Failed.")
        print("-" * 30)
        
    end_time = datetime.now()
    logging.info(f"Application Run Attempt Ended at {end_time}")
    logging.info(f"Total Time Taken: {end_time - start_time}")
    print("-" * 30)
    print(f"Application Run Attempt Ended at {end_time}")
    print(f"Total Time Taken: {end_time - start_time}")
    print("-" * 30)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blog generation script with configurable parameters.")
    parser.add_argument("--GCP_PROJECT_ID", required=True, help="GCP project for Firebase deployment.")
    parser.add_argument("--quote", required=True, help="Quote Fetching Source (e.g., ZenQuotesIO,QuotableIO, LocalQuotesIO).")
    parser.add_argument("--poem", required=True, help="Poem Generator Source (e.g., Gemini, OpenAI, Perplexity).")
    parser.add_argument("--image", required=True, help="Image Generator Source (e.g., LimewireImage, ImagenImage, StabilityAIImage).")
    args = parser.parse_args()

    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        parser.print_help()
    else:
        main(args.GCP_PROJECT_ID, args.quote, args.poem, args.image)