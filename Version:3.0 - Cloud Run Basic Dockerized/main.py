from flask import Flask, request, jsonify, send_from_directory
import ModuleGetDailyQuotes
import ModulePoemGenerator
import ModuleImageGenerator
import ModulePelicanController
import os
from datetime import datetime
import logging
import json
import time
import shutil
from logging.handlers import RotatingFileHandler
import markdown
import subprocess

import dotenv
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

# Set up log rotation
handler = RotatingFileHandler(
    'logs/all_generated_runs.log',
    maxBytes=10 * 1024 * 1024,  # 10 MB max file size
    backupCount=7,  # Keep 7 backup files
)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

app = Flask(__name__)


@app.route('/')
def index():
    # Display the hosted output
    return send_from_directory('/app/_site/output', 'index.html')

# Catch-all route for other HTML files
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('/app/_site/output', path)
    
# Protect the '/generate' route with authentication
    
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def authenticate(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    return False

@app.route('/generate', methods=['POST'])
def generate_content():
    # Check if authentication is provided
    auth = request.authorization
    logging.info(request.authorization)
    if not authenticate(auth.username, auth.password):
        logging.info("Auth Failed")
        return jsonify({"Response" : "Unauthorized","message": "Authentication required"}), 401
    logging.info("Auth Done")

    data = request.get_json()  # Parse the JSON data
    QS = data.get("quote_source")
    PS = data.get("poem_source")
    IS = data.get("image_source")
    print(QS,PS,IS)
    
    logging.info(f"QouteS: {QS}, PoemS: {PS}, ImageS: {IS}")
    # Validate the sources (optional, but recommended)
    if not all([QS, PS, IS]):
        return jsonify({f"message": "Please provide all sources (quote_source, poem_source, image_source), Received {QS} {PS} {IS}"}), 400
    allowed_quote_sources = ['QuotablesIO', 'ZenQuotesIO', 'LocalQuoteIO']
    allowed_poem_sources = ['Gemini', 'OpenAI', 'PerplexityAI']
    allowed_image_sources = ['LimewireImage', 'StabilityAIImage', 'ImagenImage']

    if QS not in allowed_quote_sources:
        return jsonify({"message": f"Invalid quote source: {QS}"}), 400

    if PS not in allowed_poem_sources:
        return jsonify({"message": f"Invalid poem source: {PS}"}), 400

    if IS not in allowed_image_sources:
        return jsonify({"message": f"Invalid image source: {IS}"}), 400
    # Log the request details

    logging.info(f"Request received from {request.remote_addr}")
    logging.info(f"Request data: quote_source={QS}, poem_source={PS}, image_source={IS}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Current Directory: {current_dir}")
    user_home_directory = subprocess.check_output("echo ~", shell=True).decode("utf-8").strip()
    logging.info(f"User Home Directory: {user_home_directory}")
    pelican_content_dir = os.path.join(current_dir, "_site", "content")
    logging.info(f"pelican_content_dir: {pelican_content_dir}")
    media_dir = os.path.join(pelican_content_dir, "media")
    logging.info(f"media_dir: {media_dir}")
    pelican_deployer_dir = os.path.join(current_dir, "_site")
    logging.info(f"pelican_deployer_dir: {pelican_deployer_dir}")
    output_media_dir = os.path.join(pelican_deployer_dir,"output","media")
    os.makedirs(output_media_dir, exist_ok=True)
    os.makedirs(pelican_content_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(pelican_deployer_dir, exist_ok=True)    

    try:
        # Fetch daily quote
        logging.info("Sending Request to Fetch Quote")
        quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(QS)
        logging.info(f"Quote fetched: {quote_data}")
        quote = quote_data.get("quote", "")
        author = quote_data.get("author", "")
        quote_from = quote_data.get("source", "")

        # Generate poem
        try:
            logging.info("Sending Request to Fetch Poem")
            poem = ModulePoemGenerator.generate_poem_from_source(quote + " by "  + author, PS)
            logging.info(f"Poem generated: {poem}")
        except Exception as e:
            logging.error(f"Error generating poem: {e}")
            poem = None  # Set poem to None if there's an error

        # Generate image
        try:
            logging.info("Sending Request to Fetch Image")
            image_file_name = ModuleImageGenerator.generate_image_from_source(quote + " by " + author, IS, media_dir)
            logging.info(f"Image generated: {image_file_name}")
        except Exception as e:
            logging.error(f"Error generating image: {e}")
            image_file_name = None  # Set image_file_name to None if there's an error

        # Generate markdown content
        try:
            markdown_content = ModulePelicanController.generate_combined_markdown(
                quote,
                author,
                poem,
                image_file_name,
                QS,
                PS,
                IS,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            logging.info(f"Markdown generated: {markdown_content}")
        except Exception as e:
            logging.error(f"Error generating markdown: {e}")
            markdown_content = None  # Set markdown_content to None if there's an error

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        markdown_file_path = os.path.join(pelican_content_dir, f"{timestamp}.md")
        with open(markdown_file_path, "w") as f:
            f.write(markdown_content)
        logging.info(f"Markdown file created at: {markdown_file_path}")

        logging.info("Running Pelican to generate HTML output.")
        ModulePelicanController.pelican_MDmedia_to_output()
        print("Blog Post Generation Complete!")
        pelican_output_dir = os.path.join(pelican_deployer_dir, "output")
        logging.info(f"Static HTML Files for hosting will be present in {pelican_output_dir}")
        logging.info("-" * 30)

        logging.info("Copying generated images from content/media to output/media")
        output_media_dir = os.path.join(pelican_output_dir, "media")
        shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)
        logging.info(f"Media files copied to: {output_media_dir}")

        # Save last run details to JSON
        last_run_data = {
            "timestamp": datetime.now().isoformat(),
            "remote_addr": request.remote_addr,
            "quote_source": QS,
            "poem_source": PS,
            "image_source": IS,
            "quote_data": quote_data,
            "poem": poem,
            "image_file_name": image_file_name,
            "markdown_content": markdown_content
        }
        with open('logs/last_run.json', 'w') as f:
            json.dump(last_run_data, f)

        return jsonify({"Response Code" : 200,"message": "Content generated successfully!", "quote_data": quote_data,"poem": poem, "image_file_name": image_file_name, }), 200  # Success response

    except Exception as e:
        logging.error(f"Error during content generation: {e}")
        return jsonify({"Response Status" : "Error", "message": f"Error generating content: {e}",
                        "quote_data": quote_data if 'quote_data' in locals() else None,
                        "poem": poem if 'poem' in locals() else None,
                        "image_file_name": image_file_name if 'image_file_name' in locals() else None}), 500  # Error response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
