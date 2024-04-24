import json
import logging
import os

from linkedin.linkedin_scraper import DataExtractor
from linkedin_google_search import get_first_google_search_url,find_organization_by_email
from linkedin_to_cb_tc import scrape_and_summarize_techcrunch, scrape_linkedin, scrape_crunchbase_organization, extract_crunchbase_username
import behance_to_linkedin
from github.github_scraper import load_github_data, extract_linkedin_username_from_github
from dotenv import load_dotenv

load_dotenv()

def setup_logging():
    logger = logging.getLogger(__name__)
    if not logger.handlers:  # Check if handlers are already added
        logger.setLevel(logging.INFO)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('logfile.log')
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
    return logger

def get_user_input():
    print("Please enter user information:")
    return {
        "first_name": input("First Name: ").strip(),
        "last_name": input("Last Name: ").strip(),
        "email": input("Email: ").strip(),
        "company_name": input("Company Name: ").strip(),
        "linkedin_username": input("LinkedIn Username: ").strip(),
        "behance_username": input("Behance Username: ").strip(),
        "github_username": input("GitHub Username: ").strip()
    }

def extract_username_from_alternate_sources(user_info, logger):
    if user_info.get('github_username'):
        logger.info(f"Attempting to extract LinkedIn username from GitHub for user: {user_info['github_username']}")
        github_data_file = load_github_data(user_info['github_username'])
        if os.path.exists(github_data_file):
            with open(github_data_file, 'r', encoding='utf-8') as file:
                github_data = json.load(file)
            linkedin_username = extract_linkedin_username_from_github(github_data)
            if linkedin_username:
                logger.info(f"Extracted LinkedIn username from GitHub: {linkedin_username}")
                return linkedin_username
        logger.error("GitHub data file not found or could not be opened.")
    
    if user_info.get('behance_username'):
        logger.info(f"Attempting to extract LinkedIn username from Behance for user: {user_info['behance_username']}")
        linkedin_username = behance_to_linkedin.behance_linkedin(user_info['behance_username'])
        if linkedin_username:
            logger.info(f"Extracted LinkedIn username from Behance: {linkedin_username}")
            return linkedin_username
        logger.error("Failed to extract LinkedIn username from Behance.")

    return None

def process_user(user_info, logger):
    linkedin_username = user_info.get('linkedin_username') or extract_username_from_alternate_sources(user_info, logger)
    full_name = f"{user_info.get('first_name')} {user_info.get('last_name')}"
    email = user_info.get('email')
    company_name = user_info.get('company_name')

    if email:
        if not company_name:
            logger.info("Extracting company name from email.")
            company_name = find_organization_by_email(email)
            if company_name in ["Failed to retrieve information.", "No data found for this domain.", "Organization information not available."]:
                logger.error(f"Could not extract company name from email: {company_name}")
                return
    else:
        logger.warning("Email not provided; limited functionality for organization extraction.")

    if not user_info.get('linkedin_username') and company_name:
        logger.info(f"Attempting to find LinkedIn username for: {full_name}")
        search_query = f'"{full_name}" "{company_name}" site:linkedin.com/in OR site:linkedin.com/pub'
        linkedin_username = get_first_google_search_url(search_query)
        if linkedin_username and linkedin_username != "Username not found in URL":
            user_info['linkedin_username'] = linkedin_username
            logger.info(f"Found LinkedIn Username: {linkedin_username}")
        else:
            logger.error("No LinkedIn Username found.")
            return
    elif not company_name:
        logger.warning("No company name provided; cannot perform LinkedIn search.")

    

    if linkedin_username:
        logger.info(f"Scraping LinkedIn for user: {linkedin_username}")
        linkedin_data_directory = scrape_linkedin(linkedin_username, os.getenv('LINKEDIN_API_KEY'), os.getenv('LINKEDIN_API_HOST'), os.getenv('PROSPEO_API_KEY'))
        print(linkedin_data_directory)
        if linkedin_data_directory:
            data_extractor = DataExtractor(f"{linkedin_data_directory}/{linkedin_username}_profile_data.json")
            try:
                company_name = data_extractor.get_company_name()
                print(company_name)
                if company_name:
                    logger.info(f"Extracted company name: {company_name}")
                    crunchbase_username = extract_crunchbase_username(company_name)
                    if crunchbase_username:
                        logger.info(f"Crunchbase username: {crunchbase_username}")
                        scrape_crunchbase_organization(crunchbase_username)
                    scrape_and_summarize_techcrunch(linkedin_username, company_name)
                else:
                    logger.info("Company name could not be extracted from LinkedIn data.")
            except Exception as e:
                logger.error(f"Error extracting company name: {e}")
    else:
        logger.error("No valid LinkedIn username found to proceed with scraping.")

def main():
    logger = setup_logging()
    users = []
    while True:
        user_info = get_user_input()
        users.append(user_info)
        if input("Add another user? (y/n): ").lower() != 'y':
            break

    for user_info in users:
        process_user(user_info, logger)

if __name__ == "__main__":
    main()
