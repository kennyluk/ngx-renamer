from datetime import datetime
import requests
import yaml

class OllamaTitles:
    def __init__(self, ollama_server_url, paperless_url, paperless_api_key, settings_file="settings.yaml") -> None:
        self.ollama_server_url = ollama_server_url
        self.paperless_url = paperless_url
        self.paperless_api_key = paperless_api_key
        self.settings = self.__load_settings(settings_file)
        print(f"Loaded settings: {self.settings}")  # Debugging line

    def __load_settings(self, settings_file):
        try:
            with open(settings_file, 'r') as f:
                settings = yaml.safe_load(f)
                print(f"Settings loaded: {settings}")  # Debugging line
                return settings
        except Exception as e:
            print(f"Error loading settings file: {e}")
            return None

    def __truncate_text(self, text, max_tokens=500):
        words = text.split()
        if len(words) > max_tokens:
            return ' '.join(words[:max_tokens])
        return text

    def __ask_ollama(self, content):
        try:
            url = f"{self.ollama_server_url}/api/generate"
            print(f"Requesting URL: {url}")
            response = requests.post(
                url,
                json={
                    "model": self.settings.get("ollama_model", "llama3.2"),
                    "prompt": content,
                    "stream": False  # Ensuring a single response
                }
            )
            response.raise_for_status()
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error generating title from Ollama: {e}")
            return None

    def generate_title_from_text(self, text):
        truncated_text = self.__truncate_text(text, max_tokens=500)
        with_date = self.settings.get("with_date", False)
        setting_prompt = self.settings.get("prompt", None)
        if setting_prompt:
            prompt = setting_prompt.get("main", "")

            if with_date:
                current_date = datetime.today().strftime("%Y-%m-%d")
                with_date_prompt = setting_prompt.get("with_date", "")
                with_date_prompt = with_date_prompt.replace("{current_date}", current_date)
                prompt += with_date_prompt
            else:
                prompt += setting_prompt.get("no_date", "")

            prompt += setting_prompt.get("pre_content", "") + truncated_text
            prompt += setting_prompt.get("post_content", "")

            print(f"Constructed Prompt: {prompt}")  # Debugging line to see the prompt

            result = self.__ask_ollama(prompt)
            if result and 'response' in result:
                return result['response']
            else:
                print("Failed to get a valid response from Ollama.")
                return None
        else:
            print("Prompt settings not found.")
            return None

    def __get_document_details(self, document_id):
        headers = {
            "Authorization": f"Token {self.paperless_api_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            f"{self.paperless_url}/documents/{document_id}/", headers=headers
        )

        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print(
                f"Failed to get document details from paperless-ngx. Status code: {response.status_code}"
            )
            print(response.text)
            return None

    def __update_document_title(self, document_id, new_title):
        payload = {"title": new_title}

        headers = {
            "Authorization": f"Token {self.paperless_api_key}",
            "Content-Type": "application/json",
        }

        response = requests.patch(
            f"{self.paperless_url}/documents/{document_id}/",
            json=payload,
            headers=headers,
        )

        if response.status_code == 200:
            print(
                f"Title of {document_id} successfully updated in paperless-ngx to {new_title}."
            )
        else:
            print(
                f"Failed to update title in paperless-ngx. Status code: {response.status_code}"
            )
            print(response.text)

    def generate_and_update_title(self, document_id):
        document_details = self.__get_document_details(document_id)
        if document_details:
            print(f"Current Document Title: {document_details['title']}")

            content = document_details.get("content", "")

            new_title = self.generate_title_from_text(content)

            if new_title:
                print(f"Generated Document Title: {new_title}")

                self.__update_document_title(document_id, new_title)
            else:
                print("Failed to generate the document title.")
        else:
            print("Failed to retrieve document details.")
