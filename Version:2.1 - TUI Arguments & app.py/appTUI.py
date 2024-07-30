import os
import json
import requests
import sys
import shutil
import subprocess
import logging
from typing import Dict, Any
from datetime import datetime
from rich.progress import track
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
load_dotenv()

#Importing My Modules
import Modules.ModuleGetDailyQuotes as ModuleGetDailyQuotes
import Modules.ModulePoemGenerator as ModulePoemGenerator
import Modules.ModuleImageGenerator as ModuleImageGenerator
import Modules.ModulePelicanController as ModulePelicanController
import Modules.ModuleFirebaseController as ModuleFirebaseController


# Configure logging to reduce headaches when code break
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
#GCP_PROJECT_ID will be also used as firebase_project_id

GCP_LOCATION = os.getenv("GCP_LOCATION")

def main() -> None:
    """Main function to run the blog generation process."""
    console = Console()
    start_time = datetime.now()
    logging.info(f"Application Run Attempt Started at {start_time}")

    # Option Selection Loop
    while True:  # Outer loop to keep the program running
        console.print(Panel("[bold blue]Welcome to Gemini Blog Generator![/bold blue]"), justify="center")
        console.print("Set Quote, Poem, Image Generation Sources.")
        console.print("Select your Source :")

        # Flags for source selection
        quote_source_selected = False
        poem_source_selected = False
        image_source_selected = False

        # Get Quote Source
        while not quote_source_selected:
            console.print("[bold blue]Select From Available Quote Sources:[/bold blue]")
            console.print("[1] QuotablesIO [ Working ][ No API_KEY Needed]]")
            console.print("[2] LocalQuoteIO  [ Working ][ Use from 'Backup_Repository/local_quotes.json']")
            console.print("[3] ZenQuotesIO  [ Working ][ No API_KEY Needed]")

            quote_choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

            if quote_choice == "1":
                quote_source = "QuotablesIO"
                console.print(f"-- you selected {quote_source}")
                quote_source_selected = True
            elif quote_choice == "2":
                quote_source = "LocalQuoteIO"
                console.print(f"-- you selected {quote_source}")
                quote_source_selected = True
            elif quote_choice == "3":
                quote_source = "ZenQuotesIO"
                console.print(f"-- you selected {quote_source}")
                quote_source_selected = True
            else:
                console.print("[bold red]Invalid choice![/bold red]")

        # Get Poem Source
        while not poem_source_selected:
            console.print("[bold blue]Select From Available Poem Sources:[/bold blue]")
            console.print("[1] Gemini  [ Working ][Set 'GEMINI_API_KEY' in .env ]")
            console.print("[2] OpenAI  [ Not Fully Tested ][Will Require 'OPENAI_API_KEY' in .env]")
            console.print("[3] Perplexity  [ Not Fully Tested ][Will Require 'PERPLEXITY_API_KEY' in .env]")

            poem_choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

            if poem_choice == "1":
                poem_source = "Gemini"
                console.print(f"-- you selected {poem_source}")
                poem_source_selected = True
            elif poem_choice == "2":
                poem_source = "OpenAI"
                console.print(f"-- you selected {poem_source}")
                poem_source_selected = True
            elif poem_choice == "3":
                poem_source = "Perplexity"
                console.print(f"-- you selected {poem_source}")
                poem_source_selected = True
            else:
                console.print("[bold red]Invalid choice![/bold red]")

        # Get Image Source
        while not image_source_selected:
            console.print("[bold blue]Select From Available Image Sources:[/bold blue]")
            console.print("[1] LimewireImage [ Working ][Set 'LimeWire_API_KEY' in .env ]")
            console.print("[2] StabilityAIImage [ Working ][Will Require 'StabilityAI_API_KEY' in .env ]")
            console.print("[3] ImagenImage [ Working ][Set 'GOOGLE_API_KEY' in .env ][Requires VertexAI Enabled with Imagen Allowlist]")

            image_choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

            if image_choice == "1":
                image_source = "LimewireImage"
                console.print(f"-- you selected {image_source}")
                image_source_selected = True
            elif image_choice == "2":
                image_source = "StabilityAIImage"
                console.print(f"-- you selected {image_source}")
                image_source_selected = True
            elif image_choice == "3":
                image_source = "ImagenImage"
                console.print(f"-- you selected {image_source}")
                image_source_selected = True
            else:
                console.print("[bold red]Invalid choice![/bold red]")

        # Proceed to Fetch from Sources?
        console.print("[bold green]Proceed to Fetch from Sources?[/bold green]")
        console.print("[1] Yes")
        console.print("[2] No. Exit Program")
        console.print("[3]. No. Start Selection Again.")

        proceed_choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

        if proceed_choice == "2":
            console.print("[bold yellow]Exiting...[/bold yellow]")
            sys.exit(0)
        elif proceed_choice == "3":
            console.print("[bold yellow]Starting Selection Again...[/bold yellow]")
            continue  # Restart the source selection loop
        elif proceed_choice == "1":
            break  # Exit the outer loop and proceed with generation

    #Enable Vertex AI API
    if image_source == "ImagenImage":
        console.print("You have selected Google Imagen which requires Vertex AI API")
        console.print("Currently, running Imagen is not possible unless you are in Imagen Allowlist")
        console.print("Enabling Vertex AI API")
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
    console.print(f"Setting User Home Deployer Directory: {user_home_directory}")
    console.print(f"Setting Pelican Content Directory: {pelican_content_dir}")
    console.print(f"Setting Pelican Attached Media Directory: {media_dir}")
    console.print(f"Setting Pelican Deployer Directory: {pelican_deployer_dir}")

    # Create directories if they don't exist
    os.makedirs(pelican_content_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(pelican_deployer_dir, exist_ok=True)

    #print(os.environ["PATH"])
    console.print("Adding /.local/bin to PATH if not already present")
    local_bin_path = os.path.join(user_home_directory, ".local", "bin")
    if local_bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"] + f":{local_bin_path}"
        console.print(f"Local Bin was not present, appending {local_bin_path}")
    #print(os.environ["PATH"])

    console.print("[bold green]Fetching Daily Quote[/bold green]")
    console.print("-" * 30)
    quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(quote_source)  # ed
    quote = quote_data.get("quote", "")
    author = quote_data.get("author", "")
    quote_from = quote_data.get("source", "")
    console.print(f"Quote: {quote}")
    console.print(f"Author: {author}")

    console.print("[bold green]Generating Poem[/bold green]")
    console.print("-" * 30)
    poem = ModulePoemGenerator.generate_poem_from_source(quote+ "by" + author, poem_source)
    logging.info(f"Poem: {poem}")
    console.print(poem)

    console.print("[bold green]Generating Image[/bold green]")
    console.print("-" * 30)
    # Generate image
    image_file_name = ModuleImageGenerator.generate_image_from_source(quote, image_source, media_dir)  # Pass the correct media directory
    logging.info(f"Image file name: {image_file_name}")
    console.print(image_file_name)

    if image_file_name and poem and quote_data:
        console.print("[bold green]Combining Blog Post[/bold green]")
        console.print("-" * 30)

        # Generate markdown content
        markdown_content = ModulePelicanController.generate_combined_markdown(quote, author,  poem, image_file_name, quote_source, poem_source, image_source , datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Create the markdown file directly in the pelican_content_dir
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        markdown_file_path = os.path.join(pelican_content_dir, f"{timestamp}.md")
        with open(markdown_file_path, "w") as f:
            f.write(markdown_content)
        logging.info(f"Markdown file created at: {markdown_file_path}")
        console.print(f"Markdown file created at: {markdown_file_path}")

        #--------------------------------------------------------------------------------------------------------------

        console.print("[bold green]Running Pelican to generate HTML output.[/bold green]")
        console.print("-" * 30)
        console.print("[bold green]Do you want to generate the HTML output using Pelican?[/bold green]")
        console.print("[1] Yes")
        console.print("[2] No")

        pelican_choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

        if pelican_choice == "1":
            pelican_output_dir = os.path.join(pelican_deployer_dir, "output")
            os.makedirs(pelican_output_dir, exist_ok=True)
            ModulePelicanController.pelican_MDmedia_to_output()
            console.print("Blog Post Generation Complete!")
            console.print("Static HTML Files for hosting will be present in", pelican_output_dir)
            console.print("-" * 30)

            # Now define the variables if pelican_choice is 1
            output_media_dir = os.path.join(pelican_output_dir, "media")
            shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)
            logging.info(f"Media files copied to: {output_media_dir}")
            console.print(f"Media files copied to: {output_media_dir}")

            console.print("[bold green]Do you want to deploy the Pelican output to Firebase?[/bold green]")
            console.print("[1] Yes")
            console.print("[2] No")

            firebase_choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

            if firebase_choice == "1":
                console.print("[bold green]Deploying Pelican output to Firebase.[/bold green]")
                ModuleFirebaseController.deploy_to_firebase(pelican_deployer_dir, GCP_PROJECT_ID)
                console.print("Blog post should be generated and deployed successfully!")
            else:
                console.print("[bold yellow]Skipping Firebase deployment...[/bold yellow]")

        elif pelican_choice == "2":
            console.print("[bold yellow]Skipping Pelican HTML generation and Firebase deployment...[/bold yellow]")

        #--------------------------------------------------------------------------------------------------------------

        end_time = datetime.now()
        logging.info(f"Application Run Attempt Ended at {end_time}")
        logging.info(f"Total Time Taken: {end_time - start_time}")
        console.print("-" * 30)
        console.print(f"Application Run Attempt Ended at {end_time}")
        console.print(f"Total Time Taken: {end_time - start_time}")
        console.print("-" * 30)

if __name__ == "__main__":
    main()
