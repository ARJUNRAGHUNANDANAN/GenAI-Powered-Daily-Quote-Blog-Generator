from flask import Flask, request, jsonify, send_from_directory, abort
import os
from datetime import datetime
from dotenv import load_dotenv
import subprocess
import shutil

# Import your modules
import Modules.ModuleGetDailyQuotes as ModuleGetDailyQuotes
import Modules.ModulePoemGenerator as ModulePoemGenerator
import Modules.ModuleImageGenerator as ModuleImageGenerator
import Modules.ModulePelicanController as ModulePelicanController
import Modules.ModuleFirebaseController as ModuleFirebaseController

app = Flask(__name__)

# Load environment variables from app.yaml
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
StabilityAI_API_KEY = os.getenv('StabilityAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
LimeWire_API_KEY = os.getenv('LimeWire_API_KEY')
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')

load_dotenv()

# Directory configurations
current_dir = os.path.dirname(os.path.abspath(__file__))
pelican_content_dir = os.path.join(current_dir, "pelican-CMS", "_site", "content")
media_dir = os.path.join(current_dir, "pelican-CMS", "media")
pelican_output_dir = os.path.join(current_dir, "pelican-CMS", "_site", "output")
pelican_deployer_dir = os.path.join(current_dir, "pelican-CMS")

# Create necessary directories
os.makedirs(media_dir, exist_ok=True)
os.makedirs(pelican_output_dir, exist_ok=True)

# Simple token-based authentication
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

def check_auth(token):
    return token == AUTH_TOKEN

@app.route('/generate', methods=['POST'])
def generate_content():
    auth_token = request.headers.get('Authorization')
    if not auth_token or not check_auth(auth_token):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    GCP_PROJECT_ID = data.get('GCP_PROJECT_ID')
    quote_source = data.get('quote_source')
    poem_source = data.get('poem_source')
    image_source = data.get('image_source')

    if not GCP_PROJECT_ID:
        GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

    if not GCP_PROJECT_ID:
        return jsonify({"error": "Please set 'GCP_PROJECT_ID' in .env or pass as argument '--GCP_PROJECT_ID'."}), 400

    if not quote_source or not poem_source or not image_source:
        return jsonify({"error": "quote_source, poem_source, and image_source are required"}), 400

    if image_source == "ImagenImage":
        subprocess.run(f"gcloud services enable aiplatform.googleapis.com", shell=True)

    quote_data = ModuleGetDailyQuotes.fetch_daily_quote_from_source(quote_source)
    quote = quote_data.get("quote", "")
    author = quote_data.get("author", "")
    quote_from = quote_data.get("source", "")

    poem = ModulePoemGenerator.generate_poem_from_source(quote + " by " + author, poem_source)
    image_file_name = ModuleImageGenerator.generate_image_from_source(quote, image_source, media_dir)

    if image_file_name and poem and quote_data:
        markdown_content = ModulePelicanController.generate_combined_markdown(
            quote, author, poem, image_file_name, quote_source, poem_source, image_source, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        markdown_file_path = os.path.join(pelican_content_dir, f"{timestamp}.md")
        with open(markdown_file_path, "w") as f:
            f.write(markdown_content)

        ModulePelicanController.pelican_MDmedia_to_output()

        output_media_dir = os.path.join(pelican_output_dir, "media")
        shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)
        #firebase no longer used. 
        #ModuleFirebaseController.deploy_to_firebase(pelican_deployer_dir, GCP_PROJECT_ID)

        return jsonify({"message": "Content generated and deployed successfully"}), 200
    else:
        return jsonify({"error": "Failed to generate content"}), 500


# Function to run on first deployment
@app.before_first_request
def initialize_pelican():
    # Run pelican to generate initial content
    subprocess.run(["pelican", "content"], cwd=pelican_deployer_dir, shell=True)
    # Copy media files to output directory
    output_media_dir = os.path.join(pelican_output_dir, "media")
    shutil.copytree(media_dir, output_media_dir, dirs_exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate():
    if request.remote_addr != '127.0.0.1':
        abort(403)  # Only allow requests from the hoster

    generate_content()
    return jsonify({"message": "Content generated successfully"}), 200

@app.route('/static/<path:path>', methods=['GET'])
def serve_static(path):
    return send_from_directory('pelican-CMS/_site/output', path)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
