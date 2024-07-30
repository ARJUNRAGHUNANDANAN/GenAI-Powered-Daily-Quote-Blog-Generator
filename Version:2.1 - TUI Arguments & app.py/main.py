# main.py
# @arjunraghunandanan 2024

import argparse
import os
import sys
import logging
from datetime import datetime
import dotenv
from dotenv import load_dotenv
load_dotenv()
from rich.console import Console
from rich.panel import Panel
import subprocess
import shutil
from typing import Dict, Any

# Importing My Modules
import Modules.ModuleGetDailyQuotes as ModuleGetDailyQuotes
import Modules.ModulePoemGenerator as ModulePoemGenerator
import Modules.ModuleImageGenerator as ModuleImageGenerator
import Modules.ModulePelicanController as ModulePelicanController
import Modules.ModuleFirebaseController as ModuleFirebaseController

# Configure logging to reduce headaches when code break
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

def script_mode(quote_source: str, poem_source: str, image_source: str) -> None:
    logging.info("Running the blog generation process in script mode.")
    print("Arguments Detected with main.py Running the blog generation process in script mode.")

    if image_source == 'Gemini':
        print("Enabling Vertex AI API")
        subprocess.run(f"gcloud services enable aiplatform.googleapis.com", shell=True)

    logging.info("Fetching Daily Quote")
    print("-" * 30)
    print("Fetching Daily Quote")
    quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(quote_source)
    quote = quote_data.get("quote", "")
    author = quote_data.get("author", "")
    quote_from = quote_data.get("source", "")
 
    logging.info("Generating Poem")
    print("-" * 30)
    print("Generating Poem")
    poem = ModulePoemGenerator.generate_poem_from_source(quote + " by " + author, poem_source)
    logging.info(f"Poem: {poem}")

    logging.info("Generating Image")
    print("-" * 30)
    print("Generating Image")
    image_file_name = ModuleImageGenerator.generate_image_from_source(quote, image_source, media_dir)
    logging.info(f"Image file name: {image_file_name}")

    if image_file_name and poem and quote_data:
        logging.info("All 3 requirements met : Quote, Image, Poem. Generating MD File")
        print("-" * 30)
        print("Generateing Markdown File")
        markdown_content = ModulePelicanController.generate_combined_markdown(quote, author, poem, image_file_name, quote_source, poem_source, image_source, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        markdown_file_path = os.path.join(pelican_content_dir, f"{timestamp}.md")
        with open(markdown_file_path, "w") as f:
            f.write(markdown_content)
        logging.info(f"Markdown file created at: {markdown_file_path}")

        logging.info("Running Pelican to generate HTML output.")
        print("-" * 30)
        ModulePelicanController.pelican_MDmedia_to_output()
        print("Blog Post Generation Complete!")
        pelican_output_dir = os.path.join(pelican_deployer_dir, "output")
        logging.info(f"Static HTML Files for hosting will be present in {pelican_output_dir}")
        logging.info("-" * 30)

        logging.info("Copying generated images from content/media to output/media")
        output_media_dir = os.path.join(pelican_output_dir, "media")
        shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)
        logging.info(f"Media files copied to: {output_media_dir}")

        print("-" * 30)
        print("Deploy Pelican output to Firebase.")
        logging.info("Deploy Pelican output to Firebase.")
        ModuleFirebaseController.deploy_to_firebase(pelican_deployer_dir, GCP_PROJECT_ID)
        logging.info("Blog post should be generated and deployed successfully!")
        print("Blog post should be generated and deployed successfully!")
        print("-" * 30)
    else:
        print("-" * 30)
        print("Blog Post has failed Generation Failed. Stopping Program")
        print("-" * 30)

def tui_mode() -> None:
    logging.info("Running the blog generation process in TUI mode.")
    print("No Parameters Detected. Running the blog generation process in TUI mode.")

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
            console.print("[2] StabilityAIImage [ Not Ready ][Will Require 'StabilityAI_API_KEY' in .env ]")
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
        console.print("-" * 30)
        console.print("You have selected Google Imagen which requires Vertex AI API")
        console.print("Currently, running Imagen is not possible unless you are in Imagen Allowlist")
        console.print("Enabling Vertex AI API")
        subprocess.run(f"gcloud services enable aiplatform.googleapis.com", shell=True)

    # Generate Quote
    console.print("-" * 30)
    console.print("[bold green]Fetching Daily Quote[/bold green]")
    quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(quote_source)  
    logging.info(f"quote_data: {quote_data}")
    quote = quote_data.get("quote", "")
    author = quote_data.get("author", "")
    quote_from = quote_data.get("source", "")
    console.print(f"Quote: {quote}")
    console.print(f"Author: {author}")

    # Generate Poem
    console.print("-" * 30)
    console.print("[bold green]Generating Poem[/bold green]")
    poem = ModulePoemGenerator.generate_poem_from_source(quote+ "by" + author, poem_source)
    logging.info(f"Poem: {poem}")
    console.print(poem)

    # Generate Image
    console.print("-" * 30)
    console.print("[bold green]Generating Image[/bold green]")
    image_file_name = ModuleImageGenerator.generate_image_from_source(quote, image_source, media_dir)  # Pass the correct media directory
    console.print(f"Generated image stores at {os.path.basename(image_file_name)}")
    logging.info(f"Image file name: {image_file_name}")
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
        console.print("-" * 30)
        console.print("[bold green]Running Pelican to generate HTML output.[/bold green]")
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

if __name__ == "__main__":
    console = Console()
    start_time = datetime.now()
    print("-" * 30)
    logging.info(f"Application Run Attempt Started at {start_time}")
    print(f"Application Run Attempt Started at {start_time}")

    parser = argparse.ArgumentParser(description="Gemini Blog Generator")
    parser.add_argument("--quote_source", type=str, choices=["QuotablesIO", "LocalQuoteIO", "ZenQuotesIO"], help="Source for fetching quotes")
    parser.add_argument("--poem_source", type=str, choices=["Gemini", "OpenAI", "Perplexity"], help="Source for generating poems")
    parser.add_argument("--image_source", type=str, choices=["ImagenImage", "StabilityAIImage", "LimewireImage"], help="Source for generating images")
    args = parser.parse_args()
    if len(sys.argv) == 1 or len(sys.argv) == 7:
        logging.info("Setting Up Directory")
        print("Setting Up Directory")
        print("-" * 30)
        # Create directories if they don't exist

        current_dir = os.path.dirname(os.path.abspath(__file__))
        user_home_directory = subprocess.check_output("echo ~", shell=True).decode("utf-8").strip()
        pelican_content_dir = os.path.join(current_dir, "pelican-CMS", "_site", "content")
        media_dir = os.path.join(pelican_content_dir, "media")
        pelican_deployer_dir = os.path.join(current_dir, "pelican-CMS", "_site")

        os.makedirs(pelican_content_dir, exist_ok=True)
        os.makedirs(media_dir, exist_ok=True)
        os.makedirs(pelican_deployer_dir, exist_ok=True)
        
        logging.info(f"Setting User Home Directory: {user_home_directory}")
        logging.info(f"Setting Pelican Content Directory: {pelican_content_dir}")
        logging.info(f"Setting Pelican Attached Media Directory: {media_dir}")
        logging.info(f"Setting Pelican Deployer  Directory: {pelican_deployer_dir}")
        console.print(f"Setting User Home Directory: {user_home_directory}")
        console.print(f"Setting Pelican Content Directory: {pelican_content_dir}")
        console.print(f"Setting Pelican Attached Media Directory: {media_dir}")
        console.print(f"Setting Pelican Deployer Directory: {pelican_deployer_dir}")

        old_path = os.environ["PATH"]
        logging.info(f"PATH before adding local/bin {old_path}")
        print("Adding /.local/bin to PATH if not already present")
        local_bin_path = os.path.join(user_home_directory, ".local", "bin")
        if local_bin_path not in os.environ["PATH"]:
            os.environ["PATH"] = os.environ["PATH"] + f":{local_bin_path}"
            logging.info(f"Local Bin was not present, appending {local_bin_path}")
        modified_path = os.environ["PATH"]
        logging.info(f"PATH after adding local/bin{modified_path}")
    
        if len(sys.argv) == 1:
            tui_mode()
        elif len(sys.argv) == 7:
            script_mode(args.quote_source, args.poem_source, args.image_source)
    else:
        print("Incorrect number of arguments. Please use the following format:")
        print("python main.py --quote_source <quote_source> --poem_source <poem_source> --image_source <image_source>")
        print("Example: python main.py --quote_source ZenQuotesIO --poem_source Gemini --image_source Gemini")

    end_time = datetime.now()
    logging.info(f"Application Run Attempt Ended at {end_time}")
    logging.info(f"Total Time Taken: {end_time - start_time}")
    console.print("-" * 30)
    console.print(f"Application Run Attempt Ended at {end_time}")
    console.print(f"Total Time Taken: {end_time - start_time}")
    console.print("-" * 30)