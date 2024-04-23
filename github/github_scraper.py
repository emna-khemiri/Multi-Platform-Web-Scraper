import os
import json
from collections import defaultdict
from urllib.parse import unquote
from dotenv import load_dotenv
import requests
import re

def load_github_data(github_username):
    """
    Fetches GitHub data for a given user and saves it to a JSON file.
    
    Args:
    - username (str): The GitHub username.
    
    Returns:
    - str: The file name where the scraped data is saved.
    """
    # Load environment variables from .env file
    load_dotenv()

    headers = {'Authorization': f'token {os.getenv("GITHUB_PAT")}'}

    # Initialize a dictionary to hold all the scraped data
    scraped_data = {}

    # Fetch user information
    user_info_url = f'https://api.github.com/users/{github_username}'
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # Attempt to include the public email, if available
    email = user_info.get('email', 'Email not public or available')

    # Extract LinkedIn username from blog URL, if present
    blog_url = user_info.get('blog', '')
    linkedin_username = extract_linkedin_username(blog_url)
    print("Extracted LinkedIn username:", linkedin_username)  # Debugging
    
    # Update the scraped data dictionary with the LinkedIn username
    scraped_data['linkedin_username'] = linkedin_username

    # Update the scraped data dictionary with the user information
    scraped_data['user_info'] = user_info

    # Fetch repositories
    repos_response = requests.get(f'https://api.github.com/users/{github_username}/repos', headers=headers)
    repos = repos_response.json()

    # Process repositories and languages
    scraped_data['repositories'] = []
    language_counts = defaultdict(int)
    for repo in repos:
        if repo['language']:
            language_counts[repo['language']] += 1
        scraped_data['repositories'].append({
            'name': repo['name'],
            'description': repo.get('description'),
            'primary_language': repo.get('language')
        })

    # Aggregate programming languages (skills)
    scraped_data['skills'] = dict(language_counts)

    # Fetch organizations
    orgs_response = requests.get(f'https://api.github.com/users/{github_username}/orgs', headers=headers)
    orgs = orgs_response.json()
    scraped_data['organizations'] = [{'name': org['login'], 'url': org['url'].replace('api.', '').replace('users/', '')} for org in orgs]

    # Fetch gists
    gists_response = requests.get(f'https://api.github.com/users/{github_username}/gists', headers=headers)
    gists = gists_response.json()
    scraped_data['gists'] = [{'id': gist['id'], 'html_url': gist['html_url'], 'description': gist.get('description')} for gist in gists]

    # Save the scraped data to a JSON file
    file_name = f'{github_username}_github_data.json'
    with open(file_name, 'w', encoding='utf-8')  as file:
        json.dump(scraped_data, file, indent=4,ensure_ascii=False)

    return file_name

def extract_linkedin_username(blog_url):
    """
    Extracts the LinkedIn username from the provided blog URL.
    
    Args:
    - blog_url (str): The blog URL provided in the GitHub user information.
    
    Returns:
    - str: The extracted LinkedIn username, or None if not found.
    """
    if "linkedin.com/in" in blog_url:
        print("Blog URL contains LinkedIn link")  # Debugging
        # Normalize the URL if it contains redundant parts
        cleaned_url = re.sub(r'^https?:\/\/(www\.)?linkedin\.com\/in\/', '', blog_url)
        # Normalize any trailing slashes or query parameters
        cleaned_url = re.sub(r'\/.*', '', cleaned_url)
        # Extract username from LinkedIn URL
        linkedin_username = cleaned_url.split("/")[-1]
        # Decode URL-encoded characters
        linkedin_username = unquote(linkedin_username)
        return linkedin_username
    else:
        return None


def extract_linkedin_username_from_github(github_data):
    """
    Extracts the LinkedIn username from the GitHub data.
    
    Args:
    - github_data (dict): The GitHub data scraped for a user.
    
    Returns:
    - str: The extracted LinkedIn username, or None if not found.
    """
    blog_url = github_data.get('user_info', {}).get('blog', '')
    if "linkedin.com/in" in blog_url:
        print("Blog URL contains LinkedIn link")  # Debugging
        # Normalize the URL if it contains redundant parts
        cleaned_url = re.sub(r'^https?:\/\/(www\.)?linkedin\.com\/in\/', '', blog_url)
        # Normalize any trailing slashes or query parameters
        cleaned_url = re.sub(r'\/.*', '', cleaned_url)
        # Extract username from LinkedIn URL
        linkedin_username = cleaned_url.split("/")[-1]
        # Decode URL-encoded characters
        linkedin_username = unquote(linkedin_username)
        return linkedin_username
    else:
        return None
    
    

