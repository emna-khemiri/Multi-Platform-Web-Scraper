import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



def extract_linkedin_username(url):
    # This regular expression captures the username in typical LinkedIn URL paths
    match = re.search(r'linkedin\.com\/(in|pub)\/([^\/?#]+)', url)
    if match:
        # The username is in the second group of the match
        return match.group(2)
    else:
        return "Username not found in URL."
    

def find_linkedin_username_from_email(email, first_name, last_name):
    def extract_linkedin_username(url):
        match = re.search(r'linkedin\.com\/(in|pub)\/([^\/?#]+)', url)
        if match:
            return match.group(2)
        else:
            return "Username not found in URL."

    api_key = os.getenv("HUNTER_API_KEY")
    company_name = find_organization_by_email(email, api_key)

    if company_name not in ["Failed to retrieve information.", "No data found for this domain.", "Organization information not available."]:
        search_query = f'"{first_name} {last_name}" "{company_name}" site:linkedin.com/in OR site:linkedin.com/pub'
        print("Search Query:", search_query)  # Debugging: Print the search query
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        try:
            driver.get("https://www.google.com")

            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tF2Cxc")))

            first_result = driver.find_element(By.CLASS_NAME, "tF2Cxc")
            url = first_result.find_element(By.TAG_NAME, "a").get_attribute("href")

            linkedin_username = extract_linkedin_username(url)
            print("LinkedIn Username found:", linkedin_username)  # Debugging: Print the found LinkedIn username
            return linkedin_username
        except Exception as e:
            print("An error occurred:", e)
            return None
        finally:
            driver.quit()
    else:
        return None
def find_organization_by_email(email, api_key):
    domain = email.split('@')[-1]
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'organization' in data['data']:
            raw_company_name = data['data']['organization']
            if raw_company_name:
                company_name = remove_digits_from_string(raw_company_name)
                return company_name
            else:
                return "Organization information not available."
        else:
            return "No data found for this domain."
    else:
        return "Failed to retrieve information."
    
def remove_digits_from_string(input_string):
    return re.sub(r'\d+', '', input_string).strip()