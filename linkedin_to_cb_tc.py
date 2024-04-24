import re
import requests
from bs4 import BeautifulSoup
import random
import os
import json
from dotenv import load_dotenv
from linkedin.linkedin_scraper import ProfileDataModule, UserCommentsModule, PostsModule, EmailFinderModule, DataExtractor
from apify_client import ApifyClient
from techcrunch.techcrunch_scraper import search_and_scrape_articles, summarize_text
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load environment variables from .env file
load_dotenv()

def search_google(company_name):
    url = f"https://www.google.com/search?q={company_name}+site:crunchbase.com"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    ]
    headers = {"User-Agent": random.choice(user_agents)}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve search results with status code {response.status_code}.")
        return None

def extract_crunchbase_username(company_name):
    search_results = search_google(company_name)
    if search_results:
        soup = BeautifulSoup(search_results, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if 'crunchbase.com/organization/' in href:
                match = re.search(r'/organization/([^&/?]+)', href)
                if match:
                    return match.group(1)
    return None

def scrape_linkedin(username, api_key, api_host, email_api_key):
    base_directory = "Data/Linkedin"  # Improved consistency with path
    linkedin_directory = os.path.join(base_directory, username)
    os.makedirs(linkedin_directory, exist_ok=True)

    profile_module = ProfileDataModule(api_key, api_host)
    comments_module = UserCommentsModule(api_key, api_host)
    posts_module = PostsModule(api_key, api_host)
    email_module = EmailFinderModule(email_api_key)

    profile_data = profile_module.get_profile_data(username)
    if profile_data:
        profile_data_path = os.path.join(linkedin_directory, f"{username}_profile_data.json")
        profile_module.save_data_to_file(profile_data, profile_data_path)
        comments = comments_module.get_user_comments(username)
        comments_module.save_data_to_file(comments, os.path.join(linkedin_directory, f"{username}_comments.json"))
        posts = posts_module.get_profile_posts(username)
        posts_module.save_data_to_file(posts, os.path.join(linkedin_directory, f"{username}_posts.json"))
        email_data = email_module.find_email(f"https://www.linkedin.com/in/{username}/")
        if email_data:
            email_module.save_data_to_file(email_data, os.path.join(linkedin_directory, f"{username}_email.json"))
        return linkedin_directory  # Important to return the path
    else:
        print(f"No data received for user: {username}")
        return None

def scrape_crunchbase_organization(company_username):

    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        print("APIFY_API_TOKEN not found in environment variables.")
        return
    client = ApifyClient(api_token)
    
    # Construct the full Crunchbase URL for the organization
    company_url = f"https://www.crunchbase.com/organization/{company_username}"

    # Prepare the Actor input
    run_input = {
        "urls": [{"url": company_url}],
        "cleanedData": True,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("qF73sh5AdGdFBxetv").call(run_input=run_input)

    # Fetch Actor results from the run's dataset
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    # Define your JSON file name
    filename = f"{company_username}_cb_data.json"

    # Save the data to the file
    crunchbase_directory = os.path.join("Data", "Crunchbase")
    os.makedirs(crunchbase_directory, exist_ok=True)
    filepath = os.path.join(crunchbase_directory, filename)
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(items, outfile, indent=4)

    print(f"Data saved to {filepath}")

def scrape_and_summarize_techcrunch(username, company_name):
    search_url = "https://techcrunch.com/search/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles_df = search_and_scrape_articles(search_url, company_name, headers)
    if not articles_df.empty:
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        articles_df['Summary'] = articles_df['Text'].apply(lambda text: summarize_text(text, tokenizer, model))
        techcrunch_directory = os.path.join("Data", "Techcrunch")
        os.makedirs(techcrunch_directory, exist_ok=True)
        output_filename = os.path.join(techcrunch_directory, f"{company_name.replace(' ', '_')}_techcrunch_summaries.csv")
        articles_df.to_csv(output_filename, index=False)
