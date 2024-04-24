import re
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

load_dotenv()

def remove_digits_from_string(input_string):
    # Remove digits from the string using a regular expression
    return re.sub(r'\d+', '', input_string).strip()

def find_organization_by_email(email):
    # Extract the domain from the email address
    domain = email.split('@')[-1]
    api_key= os.getenv("HUNTER_API_KEY")
    # Hunter API endpoint for domain search
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
    
    # Make the request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Check if organization information is available
        if 'data' in data and 'organization' in data['data']:
            raw_company_name = data['data']['organization']
            if raw_company_name:
                # Clean the company name to remove any digits
                company_name = remove_digits_from_string(raw_company_name)
                return company_name
            else:
                return "Organization information not available."
        else:
            return "No data found for this domain."
    else:
        return "Failed to retrieve information."
    

def get_first_google_search_url(query):
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-gpu")

    # Start a new instance of Chrome web browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Open Google
    driver.get("https://www.google.com")

    try:
        # Wait for the search box to be present
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

        # Enter the query and submit the search
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tF2Cxc")))

        # Find the first search result and extract the URL
        first_result = driver.find_element(By.CLASS_NAME, "tF2Cxc")
        url = first_result.find_element(By.TAG_NAME, "a").get_attribute("href")

        # Extract LinkedIn username from URL
        linkedin_username = extract_linkedin_username(url)
        return linkedin_username
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        # Close the browser
        driver.quit()

def extract_linkedin_username(url):
    # This regular expression captures the username in typical LinkedIn URL paths
    match = re.search(r'linkedin\.com\/(in|pub)\/([^\/?#]+)', url)
    if match:
        # The username is in the second group of the match
        return match.group(2)
    else:
        return "Username not found in URL."



