from apify_client import ApifyClient
import json
import os
from dotenv import load_dotenv

def scrape_crunchbase(username, is_organization=True):
    # Load environment variables from .env file
    load_dotenv()

    # Initialize the ApifyClient with your API token
    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

    # Base URL for constructing the full URL
    base_url = "https://www.crunchbase.com/"
    url_path = "organization/" if is_organization else "person/"
    full_url = base_url + url_path + username

    # Prepare the Actor input for specific tasks
    run_input = {
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }
    
    # Dynamically set the URLs based on whether it's a company or person
    if is_organization:
        run_input["scrapeCompanyUrls"] = {"urls": [full_url]}
    else:
        run_input["scrapeProfileUrls"] = {"urls": [full_url]}

    # Run the Actor and wait for it to finish
    run = client.actor("qF73sh5AdGdFBxetv").call(run_input=run_input)

    # Fetch Actor results from the run's dataset
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    # Define your JSON file name
    filename = f"{username}_cb_data.json"

    # Save the data to the file
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(items, outfile, indent=4)

    print(f"Data saved to {filename}")

    