import os
from behance import behance_scraper


def behance_linkedin(behance_username):
    # Construct URLs
    profile_url = f'https://www.behance.net/{behance_username}/info'
    projects_url = f'https://www.behance.net/{behance_username}/projects'
    user_url = f'https://www.behance.net/{behance_username}'

    # Fetch profile data
    profile_data = behance_scraper.fetch_profile_data(profile_url)

    # Fetch project links
    project_links = behance_scraper.fetch_project_links(projects_url)

    # Extract skills from projects
    skills = behance_scraper.extract_skills_from_projects(project_links)

    # Add Behance profile link to profile data
    profile_data["Behance Profile Link"] = user_url

    # Add skills to profile data
    profile_data["Skills"] = skills

    # Fetch LinkedIn username
    linkedin_username = behance_scraper.get_linkedin_username(profile_data)
    if linkedin_username:
        profile_data["LinkedIn Username"] = linkedin_username
        print('Linkedin Username:', linkedin_username)

    # Save data to JSON file under 'data' folder
    if not os.path.exists('Data'):
        os.makedirs('Data')
    behance_scraper.save_data_to_json(profile_data, f'Data/Behance/{behance_username}_behance_data.json')

    # Return the LinkedIn username for further processing
    return linkedin_username
    