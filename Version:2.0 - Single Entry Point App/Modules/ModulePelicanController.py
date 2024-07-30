# GeminiBlog-Version:2.0/ModulePelicanController.py
import os
import subprocess
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

def generate_combined_markdown(quote: str, author: str, quote_source: str, poem: str, image: str) -> str:
    """Generates a combined markdown file content.
        quote: The fetched quote.
        author: The author of the quote.
        quote_source: The source of the quote.
        poem: The generated poem.
        image: The generated image file location.
    Returns A string representing the markdown content.
    """
    # Get today's date
    today = datetime.now().strftime("%d%B%Y%H%M%S")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construct the markdown content
    markdown_content = f"""---
title: Quote for {today} - {author}
date: {date_str}
category: Inspirational Quote
tags: quote, inspiration, poetry, AI, {author}
slug: quote-{today}
authors: Gemini AI
summary: A daily dose of inspiration with a quote, poem, and image generated by AI.
---

# {today}
date: {date_str}
category: Inspirational Quote

# Quote of the Day
## {quote}
by **{author}**

Quote Source : {quote_source}

![pic_A1](media/{image})


> {poem}


### Disclaimer
'All Images, Poem and other content are fetched and modified by a Generative AI Application and should not be used as factual information. Use with Caution. Quotes and Author detail are taken from above cited sources '
    """

    logging.info(f"Markdown content generated: {markdown_content}")
    return markdown_content
def pelican_MDmedia_to_output():
    """Runs Pelican to generate HTML output from markdown and media files."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pelican_deployer_dir = os.path.join(current_dir, "..", "pelican-CMS", "_site")
    print(f"Pelican Deployer Directory: {pelican_deployer_dir}")

    # Print the PATH environment variable before running 'make'
    #print("PATH before running 'make':")
    #subprocess.run("echo $PATH", shell=True, cwd=pelican_deployer_dir)

    # Append to PATH if it doesn't exist
    user_home_directory = subprocess.check_output("echo ~", shell=True).decode("utf-8").strip()
    local_bin_path = os.path.join(user_home_directory, ".local", "bin")
    if local_bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"] + f":{local_bin_path}"
        print(f"Appended {local_bin_path} to PATH in SubProcess for MakeFile")

    # Print the PATH environment variable again
    #subprocess.run("echo $PATH", shell=True, cwd=pelican_deployer_dir)
    
    print("Running Pelican MakeFile")
    # Run the Pelican command
    pelican_command = "make clean html"
    logging.info(f"Running Pelican command: {pelican_command} in directory: {pelican_deployer_dir}")
    subprocess.run(pelican_command, cwd=pelican_deployer_dir, shell=True)
    logging.info("Pelican command executed successfully.")


if __name__ == "__main__":
    pelican_MDmedia_to_output()
