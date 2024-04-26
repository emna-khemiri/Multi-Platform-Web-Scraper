# linkedin_scraper.py

import logging
import os
import tempfile
import requests
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class APIHandler:
    def __init__(self, api_key, api_host):
        self.api_key = api_key
        self.api_host = api_host
        self.base_url = "https://linkedin-api8.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

    def send_request(self, endpoint, querystring=None):
        if querystring is None:
            querystring = {}
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=querystring)
        return response


class UserCommentsModule(APIHandler):
    def get_user_comments(self, username):
        endpoint = "/get-profile-comments"
        querystring = {"username": username}
        response = self.send_request(endpoint, querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"

    def save_data_to_file(self, data, filename="user_comments.json"):
        with open(filename, "w", encoding="utf-8") as file:
            # Adjust the saving logic if the data structure needs different handling
            json.dump(data, file, ensure_ascii=False, indent=4)


class PostsModule(APIHandler):
    def get_profile_posts(self, username):
        endpoint = "/get-profile-posts"
        querystring = {"username": username}
        response = self.send_request(endpoint, querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"

    def save_data_to_file(self, data, filename="posts.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class ProfileDataModule(APIHandler):
    def get_profile_data(self, username):
        endpoint = "/data-connection-count"
        querystring = {"username": username}
        response = self.send_request(endpoint, querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"

    def save_data_to_file(self, data, filename="profile_data.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            

class CompanyDetailsModule(APIHandler):
    def get_company_details(self, company_username):
        endpoint = "/get-company-details"
        querystring = {"username": company_username}
        response = self.send_request(endpoint, querystring)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error fetching company details: {response.status_code}")
            return None

    def save_data_to_file(self, data, company_username):
        base_directory = os.path.join("Data", "LinkedIn")
        company_directory = os.path.join(base_directory, company_username)
        os.makedirs(company_directory, exist_ok=True)
        filename = f"{company_username}_linkedin_details.json"
        file_path = os.path.join(company_directory, filename)
        
        if data:
            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info(f"Company details saved to {file_path}")
        else:
            logging.error("No data to save for company details.")







class EmailFinderModule:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.prospeo.io/linkedin-email-finder"
        self.headers = {
            'Content-Type': 'application/json',
            'X-KEY': self.api_key
        }

    def find_email(self, linkedin_url):
        data = {'url': linkedin_url}
        response = requests.post(self.url, json=data, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
            return None

    def save_data_to_file(self, data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)





class DataExtractor:
    def __init__(self, profile_data_file):
        self.profile_data_file = profile_data_file

    def get_company_name(self):
        try:
            with open(self.profile_data_file, 'r') as input_file:
                data = json.load(input_file)
            # Directly navigate through the nested dictionary
            positions = data.get('data', {}).get('position', [])
            if positions:
                return positions[0].get('companyName', 'Company Name not specified')
            return "No positions found."
        except Exception as e:
            logging.error(f"Failed to extract company name: {e}")
            return None

    def get_company_username(self):
        try:
            with open(self.profile_data_file, 'r') as input_file:
                data = json.load(input_file)
            # Directly navigate through the nested dictionary
            positions = data.get('data', {}).get('position', [])
            if positions:
                return positions[0].get('companyUsername', 'Company username not specified')
            return "No positions found."
        except Exception as e:
            logging.error(f"Failed to extract company username: {e}")
            return None

    def get_current_position(self):
        try:
            with open(self.profile_data_file, 'r') as input_file:
                data = json.load(input_file)
            positions = data.get('data', {}).get('position', [])
            if positions:
                return positions[0].get('title', 'Current position not specified')
            return None
        except Exception as e:
            logging.error(f"Failed to extract current position: {e}")
            return None

