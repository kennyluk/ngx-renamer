import requests
from modules.openai_titles import OpenAITitles

class PaperlessAITitles:
    def __init__(self, openai_api_key, paperless_url, paperless_api_key):
        self.openai_api_key = openai_api_key
        self.paperless_url = paperless_url
        self.paperless_api_key = paperless_api_key

        self.ai = OpenAITitles(self.openai_api_key)


    def __get_document_details(self, document_id):
        headers = {
            "Authorization": f"Token {self.paperless_api_key}",
            "Content-Type": "application/json"
        }

        response = requests.get(f"{self.paperless_url}/documents/{document_id}/", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get document details from paperless-ngx. Status code: {response.status_code}")
            print(response.text)
            return None


    def __update_document_title(self, document_id, new_title):
        payload = {
            "title": new_title
        }
        
        headers = {
            "Authorization": f"Token {self.paperless_api_key}",
            "Content-Type": "application/json"
        }

        response = requests.patch(f"{self.paperless_url}/documents/{document_id}/", json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"Title of {document_id} successfully updated in paperless-ngx to {new_title}.")
        else:
            print(f"Failed to update title in paperless-ngx. Status code: {response.status_code}")
            print(response.text)


    def generate_and_update_title(self, document_id, with_date=False):
        document_details = self.__get_document_details(document_id)
        if document_details:
            print(f"Current Document Title: {document_details['title']}")
            
            content = document_details.get('content', '')
            
            new_title = self.ai.generate_title_from_text(content, with_date)
            
            if new_title:
                print(f"Generated Document Title: {new_title}")
                
                self.__update_document_title(document_id, new_title)
            else:
                print("Failed to generate the document title.")
        else:
            print("Failed to retrieve document details.")