#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from modules.paperless_ai_titles import PaperlessAITitles

load_dotenv()

paperless_url = os.getenv("PAPERLESS_NGX_URL")
paperless_api_key = os.getenv("PAPERLESS_NGX_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

ai = PaperlessAITitles(openai_api_key, paperless_url, paperless_api_key)


def main():
    document_id = os.environ.get("DOCUMENT_ID")
    ai.generate_and_update_title(document_id)


if __name__ == "__main__":
    main()
