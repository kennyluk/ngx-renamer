#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from modules.ollama_titles import OllamaTitles

def main():
    document_id = os.environ.get('DOCUMENT_ID')
    run_dir = os.environ.get('RUN_DIR')

    load_dotenv()

    paperless_url = os.getenv("PAPERLESS_NGX_URL")
    paperless_api_key = os.getenv("PAPERLESS_NGX_API_KEY")
    ollama_server_url = os.getenv("OLLAMA_SERVER_URL")

    print("Starting Paperless AI Titles")
    print(f"Paperless Document ID: {document_id}")
    print(f"Directory where script runs in container: {run_dir}")

    ai = OllamaTitles(ollama_server_url, paperless_url, paperless_api_key, f"{run_dir}/settings.yaml")
    ai.generate_and_update_title(document_id)

if __name__ == "__main__":
    main()
