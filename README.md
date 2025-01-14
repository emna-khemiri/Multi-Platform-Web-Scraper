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
   git clone https://github.com/emna-khemiri/multi-platform-web-scraper.git
   cd multi-platform-web-scraper
