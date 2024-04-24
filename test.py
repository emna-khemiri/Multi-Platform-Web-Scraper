from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_GdATSVisUQ8ZHSolSWumx3xtvzHFJA24nMDm")

# Prepare the Actor input
run_input = {
    "urls": [
        { "url": "https://www.crunchbase.com/organization/instadeep" }],
        
    "cleanedData": True,
}

# Run the Actor and wait for it to finish
run = client.actor("qF73sh5AdGdFBxetv").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)