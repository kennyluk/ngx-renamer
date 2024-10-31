#!/usr/bin/env python3

import os
import logging

from dotenv import load_dotenv
from modules.paperless_ai_titles import PaperlessAITitles

load_dotenv()

logging.getLogger().setLevel(logging.DEBUG)
logging.debug("Starting Paperless AI Titles")

paperless_url = os.getenv("PAPERLESS_NGX_URL")
paperless_api_key = os.getenv("PAPERLESS_NGX_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

with_date = os.getenv("PAPERLESS_NGX_RENAME_WITH_DATE")
with_date = with_date.lower().strip() == "true" or False

logging.debug(f"Paperless URL: {paperless_url}")

ai = PaperlessAITitles(openai_api_key, paperless_url, paperless_api_key)

def main():
        document_id = os.environ.get("DOCUMENT_ID")
        logging.debug(f"Document ID: {document_id}")

        ai.generate_and_update_title(document_id, with_date)
        
if __name__ == "__main__":
    main()