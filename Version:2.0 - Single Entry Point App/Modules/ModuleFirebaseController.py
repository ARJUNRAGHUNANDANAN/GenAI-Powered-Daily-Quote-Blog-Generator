# GeminiBlog-Version:2.0/ModuleFirebaseController.py
import subprocess
import os
import logging

# Configure logging
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')


def deploy_to_firebase(output_dir: str, firebase_project_id) -> None:
    """Deploys the Pelican output to Firebase."""
    if not firebase_project_id:
        logging.error("GCP_PROJECT_ID environment variable not set.")
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    # Construct the Firebase deploy command
    firebase_command = f"firebase deploy --project {firebase_project_id}"
    logging.info(f"Running Firebase command: {firebase_command} in directory: {output_dir}")

    # Run the Firebase deploy command in the specified output directory
    subprocess.run(firebase_command, cwd=output_dir, shell=True)
    logging.info("Firebase command executed successfully.")
    #New Code Here


    # Deploy to Firebase
    # firebase_command = f"firebase deploy --project {firebase_project_id}"
    # logging.info(f"Running Firebase command: {firebase_command}")
    # subprocess.run(firebase_command, cwd=output_dir, shell=True)
    # logging.info("Firebase command executed successfully.")
