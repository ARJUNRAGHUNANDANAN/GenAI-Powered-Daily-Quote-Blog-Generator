import os
import json
import requests
import sys
import shutil
import subprocess
import logging
from typing import Dict, Any
from datetime import datetime
#Importing My Modules
import Modules.ModuleGetDailyQuotes as ModuleGetDailyQuotes
import Modules.ModulePoemGenerator as ModulePoemGenerator
import Modules.ModuleImageGenerator as ModuleImageGenerator
import Modules.ModulePelicanController as ModulePelicanController
import Modules.ModuleFirebaseController as ModuleFirebaseController

# Configure logging to reduce headaches when code break
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

GCP_PROJECT_ID =  os.getenv("GCP_PROJECT_ID")
#GCP_PROJECT_ID will be also used as firebase_project_id

GCP_LOCATION = os.getenv("GCP_LOCATION")
poem_source = 'Gemini'
# 'Gemini', 'OpenAI', 'Perplexity' - Only Gemini Works at the Moment.

image_source = 'ImagenImage' 

# 'LimewireImage', 'StabilityAIImage', 'ImagenImage' - Only LimewireImage Works at the Moment.

quote_source = 'QuotablesIO'
#'QuotablesIO', 'LocalQuoteIO', 'ZenQuotesIO - All Are Functional

def main() -> None:
    """Main function to run the blog generation process."""
    start_time = datetime.now()
    logging.info(f"Application Run Attempt Started at {start_time}")
    logging.info("Setting Up Directory")
    print("-" * 30)
    print("Setting Up Directory")
    print("-" * 30)
    #Enable Vertex AI API
    print("Enabling Vertex AI API")
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

    #print(os.environ["PATH"])
    print("Adding /.local/bin to PATH if not already present")
    local_bin_path = os.path.join(user_home_directory, ".local", "bin")
    if local_bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"] + f":{local_bin_path}"
        print(f"Local Bin was not present, appending {local_bin_path}")
    #print(os.environ["PATH"])

    logging.info("Fetching Daily Quote")
    print("-" * 30)
    print("Fetching Daily Quote")
    print("-" * 30)
    quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(quote_source)  # ed
    quote = quote_data.get("quote", "")
    author = quote_data.get("author", "")
    quote_from = quote_data.get("source", "")
    print(f"Quote: {quote}")
    print(f"Author: {author}")

    logging.info("Generating Poem")
    print("-" * 30)
    print("Generating Poem")
    print("-" * 30)
    poem = ModulePoemGenerator.generate_poem_from_source(quote+ "by" + author, poem_source)
    logging.info(f"Poem: {poem}")
    print(poem)

    logging.info("Generating Image")
    print("-" * 30)
    print("Generating Image")
    print("-" * 30)
    # Generate image
    image_file_name = ModuleImageGenerator.generate_image_from_source(quote, image_source, media_dir)  # Pass the correct media directory
    logging.info(f"Image file name: {image_file_name}")
    print(image_file_name)
    #sys.exit("Things were working well till now")

    if image_file_name and poem and quote_data:
        logging.info("Combining Blog Post")
        print("-" * 30)
        print("Combining Blog Post")
        print("-" * 30)


        # Generate markdown content
        markdown_content = ModulePelicanController.generate_combined_markdown(quote, author, quote_from, poem, image_file_name)

        # Create the markdown file directly in the pelican_content_dir
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        markdown_file_path = os.path.join(pelican_content_dir, f"{timestamp}.md")
        with open(markdown_file_path, "w") as f:
            f.write(markdown_content)
        logging.info(f"Markdown file created at: {markdown_file_path}")
        print(f"Markdown file created at: {markdown_file_path}")

        logging.info("Running Pelican to generate HTML output.")
        print("-" * 30)
        ModulePelicanController.pelican_MDmedia_to_output()
        # Pelican's "make publish" step to generate final html in pelican_deployer_dir/output from pelican_deployer_dir/content pending
        print("Blog Post Generation Complete!")
        pelican_output_dir = os.path.join(pelican_deployer_dir, "output")
        print("Static HTML Files for hosting will be present in", pelican_output_dir)
        print("-" * 30)

        logging.info("copying generated images from content/media to output/media")
        # Copy media files to the output directory
        output_media_dir = os.path.join(pelican_output_dir, "media")
        shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)
        logging.info(f"Media files copied to: {output_media_dir}")
        print(f"Media files copied to: {output_media_dir}")

        #sys.exit("Good till Now")
        # Deploy blog post
        logging.info("Deploying Pelican output to Firebase.")
        ModuleFirebaseController.deploy_to_firebase(pelican_deployer_dir, GCP_PROJECT_ID)
        print("Blog post should be generated and deployed successfully!")
    else:
        logging.error("Blog Post Generation Failed.")
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
    main()
