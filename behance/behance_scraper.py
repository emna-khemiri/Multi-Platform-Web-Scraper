import json
import requests
from bs4 import BeautifulSoup
import re
import tldextract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome


def safe_get_text(selector, default=None):
    """Safely get the text from a BeautifulSoup selector or return a default value."""
    if selector:
        return selector.text.strip()
    return default

def get_site_name(url):
    extracted = tldextract.extract(url)
    site_name = extracted.domain.capitalize()
    special_cases = {
        "Linkedin": "Linkedin",
        "Instagram": "Instagram",
        "Telegram": "Telegram",
        # Add more special cases as needed
    }
    return special_cases.get(site_name, site_name)

def get_bio(username):
    # URL to scrape bio from
    url = f"https://www.behance.net/{username}/info"
    
    # Try to get bio using BeautifulSoup
    try:
        # Send GET request and parse HTML
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find and extract bio element
        bio_element = soup.select_one('.UserInfo-bio-OZA')
        if bio_element:
            # Check if "Read More" link is present
            xpath_selector = "/html//div[@id='site-content']/div[@class='Profile-profileContainer-gIq']/main[@class='Profile-root-_4h e2e-Profile-page-container profile-route-profileInfo']/div[@class='Profile-wrap-ivE']/div[@class='Profile-profileContents-6tC']//div[@class='UserInfo-readMore-Lp8']/a"

            read_more_link = soup.select_one(".Profile-profileContents-6tC .UserInfo-readMore-Lp8 > .ReadMore-readMoreButton-o67.UserInfo-readMoreOrLessText-vq9")
            if read_more_link:
                # If "Read More" link is present, proceed with Selenium logic
                # Set up Chrome options
                chrome_options = Options()
                chrome_options.add_argument("--headless")  # Set headless mode
                chrome_options.add_argument("--lang=en")
                
                # Initialize the Chrome driver
                driver = Chrome(options=chrome_options)
                
                # Navigate to the URL
                driver.get(url)

                # Wait for a brief moment to ensure the page is loaded
                driver.implicitly_wait(3)
                link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_selector)))
                driver.execute_script("arguments[0].scrollIntoView();", link)
                # Click on the "Read More" link
                link.click()
                
                # Wait until the full bio element is visible
                #full_bio_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ReadMore-content-F2D.UserInfo-readMoreOrLessContent-Ywr')))
                full_bio_element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "/html//div[@id='site-content']/div[@class='Profile-profileContainer-gIq']/main[@class='Profile-root-_4h e2e-Profile-page-container profile-route-profileInfo']/div[@class='Profile-wrap-ivE']/div[@class='Profile-profileContents-6tC']//div[@class='UserInfo-readMore-Lp8']/div[@class='ReadMore-content-F2D UserInfo-readMoreOrLessContent-Ywr']")))

                # Fetch the text of the full bio element
                full_bio = full_bio_element.text.strip()
                
                # Close the browser window
                driver.quit()
                
                return full_bio
            else:
                # If "Read More" link is not present, return the bio text
                bio = bio_element.text.strip()
                if bio:
                    return bio
                
    except Exception as e:
        print("Error:", e)
    
    # If bio not found or any error occurred, return None
    return None


def fetch_profile_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        full_name = safe_get_text(soup.select_one('.ProfileCard-userFullName-ule'))
        job = safe_get_text(soup.select_one('.ProfileCard-line-fVO.e2e-Profile-occupation'))
        location = safe_get_text(soup.select_one('.ProfileCard-anchor-q0M > .e2e-Profile-location'))
        followers = safe_get_text(soup.select_one('.UserInfo-statValue-d3q.e2e-UserInfo-statValue-followers-count'))

        # Replace fetching bio with get_bio function
        username = url.split('/')[-2]
        bio = get_bio(username)

        links = {}
        parent_element = soup.select_one('#site-content > div > main > div.Profile-wrap-ivE > div.Profile-profileContents-6tC > div > div > div > div:nth-child(2) > div.UserInfo-column-ckA > div')
        if parent_element:
            for link in parent_element.find_all('a', href=True):
                site_name = get_site_name(link['href'])
                links[site_name] = link['href']

        all_text = soup.get_text()
        emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', all_text))

        return {
            "Full Name": full_name,
            "Job": job,
            "Location": location,
            "Followers": followers,
            "Bio": bio,
            "Links": links,
            "Emails": list(emails)
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "Full Name": None,
            "Job": None,
            "Location": None,
            "Followers": None,
            "Bio": None,
            "Links": {},
            "Emails": []
        }
    
def fetch_project_links(url):
    """
    Fetches project links from a Behance user's projects page.
    Returns a list of project URLs.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            base_url = 'https://www.behance.net'
            project_links = soup.find_all('a', class_='ProjectCoverNeue-coverLink-U39')
            return [f'{base_url}{link.get("href")}' for link in project_links]
        else:
            print("Failed to fetch project links due to a non-success response.")
            return []
    except Exception as e:
        print(f"An error occurred while fetching project links: {e}")
        return []

def save_data_to_json(data, filename):
    """
    Saves data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")
def filter_skills(skills):
    """
    Filters out any irrelevant or incorrect skill names from the list of skills.
    """
    
    # Define a list of common irrelevant words
    irrelevant_words = ['outils', 'tools', 'disciplines', 'creative fields', 'mobile', 'behance','behance mobilebehance']

    # Define specific words to categorize skills
    figma_word = 'Figma'
    procreate_word = 'Procreate'

    # Initialize a set to store filtered skills
    filtered_skills = set()

    for skill in skills:
        # Remove irrelevant words
        if skill.lower() in irrelevant_words:
            continue
        
        # Categorize skill as "Figma" if it contains the word "Figma"
        if figma_word.lower() in skill.lower():
            filtered_skills.add(figma_word)
        
        # Categorize skill as "Procreate" if it contains the word "Procreate"
        elif procreate_word.lower() in skill.lower():
            filtered_skills.add(procreate_word)
        
        # Add skill to the filtered skills set if it doesn't match specific categories
        else:
            filtered_skills.add(skill)

    return list(filtered_skills)


def extract_skills_from_projects(project_links):
    # Initialize Chrome webdriver with options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Set headless mode
    chrome_options.add_argument("--lang=en")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Set to store unique skills
    unique_skills = set()
    
    try:
        for link in project_links:
            # Load the page
            driver.get(link)

            # Wait for the skills section to be present on the page
            skills_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ProjectTools-section-k_L'))
            )

            # Extract the text from the skills section
            skills_text = skills_section.text

            # Split the text by newline character to extract individual skills
            skills = skills_text.split('\n')

            # Filter out irrelevant or incorrect skills
            filtered_skills = filter_skills(skills)

            # Add unique filtered skills to the set
            unique_skills.update(filtered_skills)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser
        driver.quit()

    return list(unique_skills)

def get_linkedin_username(profile_data):
    # Check if LinkedIn link is present
    if "Linkedin" in profile_data["Links"]:
        linkedin_url = profile_data["Links"]["Linkedin"]
        # Regular expression pattern to match LinkedIn username in URL path
        pattern = r'/in/(?:[^\/]+\/)*([^\/]+)'
        # Search for the pattern in the LinkedIn URL
        match = re.search(pattern, linkedin_url)
        if match:
            return match.group(1)
    return None

