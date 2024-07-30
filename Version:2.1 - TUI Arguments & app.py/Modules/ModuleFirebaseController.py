# GeminiBlog/Modules/ModuleFirebaseController.py
# @arjunraghunandanan 2024

import subprocess
import os
import logging
from dotenv import load_dotenv
load_dotenv()
# Configure logging
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')


def deploy_to_firebase(output_dir: str, firebase_project_id) -> None:
    """Deploys the Pelican output to Firebase."""
    # Construct the Firebase deploy command
    firebase_command = f"firebase deploy --project {firebase_project_id}"
    logging.info(f"Running Firebase command: {firebase_command} in directory: {output_dir}")

    # Run the Firebase deploy command in the specified output directory
    subprocess.run(firebase_command, cwd=output_dir, shell=True)
    logging.info("Firebase command executed successfully.")

    return 0
