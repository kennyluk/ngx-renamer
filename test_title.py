#!/usr/bin/env python3

import os
import logging

from dotenv import load_dotenv

from modules.openai_titles import OpenAITitles

load_dotenv()

logging.getLogger().setLevel(logging.DEBUG)

openai_api_key = os.getenv("OPENAI_API_KEY")

with_date = os.getenv("PAPERLESS_NGX_RENAME_WITH_DATE")
with_date = with_date.lower().strip() == "true" or False


ai = OpenAITitles(openai_api_key)

def main():
        text = """
(1) Zweck der Abmarkung ist, die Grenzen der Grundstücke durch Marken (Grenzzeichen) örtlich erkennbar zu bezeichnen.
(2) Zur Abmarkung nach dem in diesem Gesetz geregelten Verfahren zählen insbesondere das Anbringen von Grenzzeichen, das Verbringen von Grenzzeichen in die richtige Lage, das Erneuern sowie das Entfernen von Grenzzeichen.
(3) Das Ergebnis der Abmarkung ist im Liegenschaftskataster nachzuweisen.
(4) Stimmt eine nach den Vorschriften dieses Gesetzes oder nach früheren Vorschriften abgemarkte Grundstücksgrenze mit dem Nachweis des Liegenschaftskatasters überein, so wird, abgesehen von dem Fall des Art. 7 Abs. 2, vermutet, daß die abgemarkte Grenze die richtige ist. 2Die Vermutung der Richtigkeit gilt auch für eine Grundstücksgrenze, die festgestellt (Art. 2 Abs. 1), aber aus den in Art. 6 Nrn. 4 und 5 genannten Gründen nicht abgemarkt worden ist.
"""

        new_title = ai.generate_title_from_text(text, with_date)

        print(f"Generated Title: {new_title}")

if __name__ == "__main__":
    main()