import json

# Load the JSON file
with open('Data/Linkedin/jawher-jabri-b640b0176/jawher-jabri-b640b0176_profile_data.json', 'r', encoding='utf-8') as file:
    profile_data = json.load(file)

# Extracting required information
first_name = profile_data['data'].get('firstName', '')
last_name = profile_data['data'].get('lastName', '')
linkedin_username = profile_data['data'].get('username', '')
current_position = profile_data['data']['position'][0]['title'] if 'position' in profile_data['data'] else ''
current_company = profile_data['data']['position'][0]['companyName'] if 'position' in profile_data['data'] else ''
company_industry = profile_data['data']['position'][0]['companyIndustry'] if 'position' in profile_data['data'] else ''
company_size = profile_data['data']['position'][0]['companyStaffCountRange'] if 'position' in profile_data['data'] else ''

# Print the extracted information
print("First Name:", first_name)
print("Last Name:", last_name)
print("LinkedIn Username:", linkedin_username)
print("Current Position:", current_position)
print("Current Company:", current_company)
print("Company Industry:", company_industry)
print("Company Size:", company_size)
