import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from .env file
env = dotenv_values(".env")

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()

# Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to f6s.com/login
driver.get("https://www.f6s.com/login")

# Common steps whether or not CAPTCHA was found/solved
wait = WebDriverWait(driver, 20)
login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#csEmailLoginButton2")))

# Click on the button
login_button.click()

wait = WebDriverWait(driver, 20)
email_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[placeholder='Email address']"))) 
password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[type='password']")))

# Fill in the email and password fields
email_field.send_keys(env["EMAIL"])
password_field.send_keys(env["PASSWORD"])

# Click on the continue button
continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='dialog'] span[role='button']")))
continue_button.click()

# Wait for the login to complete
WebDriverWait(driver, 10).until(EC.url_contains("https://www.f6s.com/"))
time.sleep(5)  # You might need to adjust this delay

# Now you're logged in, you can scrape the desired information
search_word = 'YourStep'
url = f'https://www.f6s.com/search?q={search_word}'
driver.get(url)
time.sleep(5)

# Get the first link in the search results
first_result_link = driver.find_element(By.CSS_SELECTOR, "#csSearchResultsList > div:nth-child(1) > div:nth-child(2) > div.t.b18 > a").get_attribute("href")
driver.get(first_result_link)
time.sleep(5)

# Scrape data from the result page
company_data = {}
try:
    company_data["Name"] = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > div:nth-child(1) > div.header-main > div > div.profile-data > div.profile-heading > h1").text
except NoSuchElementException:
    company_data["Name"] = None
try:
    company_data["Service"] = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > div:nth-child(1) > div.header-main > div > div.profile-data > div.member-badges.member-badges > span:nth-child(1) > span").text
except NoSuchElementException:
    company_data["Service"] = None
try:
    company_data["Description"] = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > div:nth-child(1) > div.header-main > div > div.profile-data > p").text
except NoSuchElementException:
    company_data["Description"] = None
try:
    company_data["Location"] = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > section > div > div > section.section.overview > div.centered-content.g8.overview-line").text
except NoSuchElementException:
    company_data["Location"] = None
try:
    company_data["Link"] = driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > div > a").get_attribute("href")
except NoSuchElementException:
    company_data["Link"] = None
try:
    company_data["Company"] = driver.find_element(By.CSS_SELECTOR, "#investments > div > div > a").text
except NoSuchElementException:
    company_data["Company"] = None
try:
    company_data["Linkedin"] = driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > a:nth-child(2)").get_attribute("href")
except NoSuchElementException:
    company_data["Linkedin"] = None
try:
    company_data["Twitter"] = driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > a").get_attribute("href")
except NoSuchElementException:  
    company_data["Twitter"] = None
try:
    company_data["Facebook"] = driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > a:nth-child(3)").get_attribute("href")
except NoSuchElementException:
    company_data["Facebook"] = None

# Scroll down to the specified section
try:
    about_section = driver.find_element(By.CSS_SELECTOR, "#about > section.section.details")
    driver.execute_script("arguments[0].scrollIntoView();", about_section)
    time.sleep(2)
    # Click the link if found
    link_element = about_section.find_element(By.CSS_SELECTOR, "div.profile-about.mt16 > a")
    link_element.click()
except NoSuchElementException:
    pass

# Grab the about
about = None
try:
    about_element = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > section > div > div > section.section.details > div.profile-about.mt16 > div > p")
    about = about_element.text
except NoSuchElementException:
    pass

# Add about section to company_data
company_data["About"] = about

# Save data to a JSON file
company_name = company_data["Name"].lower().replace(" ", "_")
file_name = f"{company_name}_f6s.json"
with open(file_name, "w") as json_file:
    json.dump(company_data, json_file, indent=4)

print(f"Data saved to {file_name}")

# Close the browser
driver.quit()
