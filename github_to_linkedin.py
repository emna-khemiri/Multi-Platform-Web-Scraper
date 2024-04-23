import json
import re

# Sample JSON string from GitHub scraping
github_json_str = '''
{
    "user_info": {
        "login": "brunoaugustoam",
        "id": 42394219,
        "node_id": "MDQ6VXNlcjQyMzk0MjE5",
        "avatar_url": "https://avatars.githubusercontent.com/u/42394219?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/brunoaugustoam",
        "html_url": "https://github.com/brunoaugustoam",
        "followers_url": "https://api.github.com/users/brunoaugustoam/followers",
        "following_url": "https://api.github.com/users/brunoaugustoam/following{/other_user}",
        "gists_url": "https://api.github.com/users/brunoaugustoam/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/brunoaugustoam/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/brunoaugustoam/subscriptions",
        "organizations_url": "https://api.github.com/users/brunoaugustoam/orgs",
        "repos_url": "https://api.github.com/users/brunoaugustoam/repos",
        "events_url": "https://api.github.com/users/brunoaugustoam/events{/privacy}",
        "received_events_url": "https://api.github.com/users/brunoaugustoam/received_events",
        "type": "User",
        "site_admin": false,
        "name": "Bruno Alemao Monteiro",
        "company": "UFMG, MG, BRAZIL",
        "blog": "https://www.linkedin.com/in/bruno-augusto-alem%C3%A3o-monteiro-4a9056113/",
        "location": "Belo Horizonte",
        "email": null,
        "hireable": null,
        "bio": "Msc. in Computer Science and Research Geologist",
        "twitter_username": null,
        "public_repos": 8,
        "public_gists": 0,
        "followers": 5,
        "following": 7,
        "created_at": "2018-08-15T00:03:10Z",
        "updated_at": "2023-10-19T16:43:41Z"
    }
}
'''

# Parse the JSON string
data = json.loads(github_json_str)

# Extract the blog URL
blog_url = data.get("user_info", {}).get("blog", "")

# Preprocess and extract the LinkedIn username
linkedin_username = None
if "linkedin.com/in" in blog_url:
    # Normalize the URL if it contains redundant parts
    cleaned_url = re.sub(r'^https?:\/\/(www\.)?linkedin\.com\/in\/', '', blog_url)
    # Normalize any trailing slashes or query parameters
    cleaned_url = re.sub(r'\/.*', '', cleaned_url)
    linkedin_username = cleaned_url

# Print the LinkedIn username
print(f"LinkedIn Username: {linkedin_username}")
