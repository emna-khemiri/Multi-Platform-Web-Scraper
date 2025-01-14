# Multi-Platform Web Scraper

This project is a robust web scraping tool designed to gather and process user and company data from platforms like LinkedIn, GitHub, Behance, Crunchbase, and TechCrunch. It integrates multiple APIs and scraping techniques to extract, process, and summarize relevant information.

## Features

- **LinkedIn Scraping**: Extract user profiles, company details, and other relevant data.
- **GitHub Integration**: Identify LinkedIn usernames from GitHub profiles.
- **Behance Integration**: Extract LinkedIn usernames from Behance profiles.
- **Crunchbase and TechCrunch**: Scrape and summarize company details and news.
- **Google Search Support**: Perform LinkedIn user discovery via Google search.
- **Logging**: Detailed logging to track execution and debug issues.
- **Environment Variable Management**: Secure handling of sensitive API keys using `.env`.

## Prerequisites

1. Python 3.7 or higher.
2. Required Python packages (listed in `requirements.txt`).
3. API keys for LinkedIn, Crunchbase, and other integrated services.
4. Access to Google Search (optional).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/multi-platform-web-scraper.git
   cd multi-platform-web-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your API keys:
   ```
   LINKEDIN_API_KEY=your_linkedin_api_key
   LINKEDIN_API_HOST=your_linkedin_api_host
   PROSPEO_API_KEY=your_prospeo_api_key
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Follow the prompts to enter user information:
   - First name
   - Last name
   - Email
   - Company name
   - LinkedIn username
   - Behance username
   - GitHub username

3. The script processes the input, extracts data from various platforms, and logs the results.

## File Structure

- `main.py`: Entry point for the script.
- `linkedin_scraper/`: Contains modules for LinkedIn scraping and data extraction.
- `github/github_scraper.py`: Handles GitHub data scraping.
- `behance_to_linkedin/`: Maps Behance profiles to LinkedIn.
- `linkedin_google_search.py`: Performs LinkedIn discovery using Google search.
- `linkedin_to_cb_tc.py`: Handles integration with Crunchbase and TechCrunch.
- `logfile.log`: Log file generated during execution.

## Logging

Logs are saved in `logfile.log`, with details on each step, including errors and extracted information.

## Disclaimer

This project is intended for educational and personal use only. Scraping data from platforms like LinkedIn and others may violate their terms of service. Use responsibly.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

Happy Scraping!
