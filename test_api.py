#!/usr/bin/env python3

import os
import argparse
import requests

# from dotenv import load_dotenv

# load_dotenv()

paperless_url = "http://ip:port/api"
paperless_api_key = "apikey"

def main():
    parser = argparse.ArgumentParser(description="Get some data document")
    parser.add_argument("document_id", type=int)
    args = parser.parse_args()

    document_id = args.document_id
    print(f"Document ID: {document_id}")
    print(f"Paperless URL: {paperless_url}")
    print(f"Paperless API Key: {paperless_api_key}")

    headers = {
        "Authorization": f"Token {paperless_api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{paperless_url}/documents/{document_id}/", headers=headers
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error getting document details: {e}")
        return

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")  # Print the response content for debugging

    if response.status_code == 200:
        try:
            print(response.json())
        except ValueError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(
            f"Failed to get document details from paperless-ngx. Status code: {response.status_code}"
        )
        print(response.text)

if __name__ == "__main__":
    main()
