import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def fetch_article_text(url, headers):
    """
    Fetches the text content of an article from a given URL.
    
    Args:
    - url (str): The URL of the article.
    - headers (dict): Headers to be used in the HTTP request.
    
    Returns:
    - str: The text content of the article.
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_body = soup.find('div', class_='article-content')
            paragraphs = article_body.find_all('p')
            article_text = ' '.join(paragraph.text for paragraph in paragraphs)
            return article_text
    except Exception as e:
        print(f"An error occurred while fetching the article text: {e}")
    return ""

def search_and_scrape_articles(search_url, company_name, headers):
    """
    Searches for articles related to a given company and scrapes their text content.
    
    Args:
    - search_url (str): The URL of the search page.
    - company_name (str): The name of the company to search for.
    - headers (dict): Headers to be used in the HTTP request.
    
    Returns:
    - pd.DataFrame: A DataFrame containing the titles, URLs, and text content of the articles.
    """
    query = company_name.replace(' ', '+')
    full_url = f"{search_url}{query}"

    articles_data = []

    response = requests.get(full_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', class_='post-block__title__link')

        for article in articles:
            title = article.text.strip()
            url = article['href']
            article_text = fetch_article_text(url, headers)
            articles_data.append({"Title": title, "URL": url, "Text": article_text})
    else:
        print("Failed to retrieve the search results.")

    return pd.DataFrame(articles_data)

def summarize_text(text, tokenizer, model):
    """
    Summarizes a given text using BART large CNN model.
    
    Args:
    - text (str): The text to be summarized.
    - tokenizer: The tokenizer object.
    - model: The model object.
    
    Returns:
    - str: The summary of the text.
    """
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Example usage
def main():
    search_url = "https://techcrunch.com/search/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    company_name = 'instadeep'

    # Search and scrape articles
    df = search_and_scrape_articles(search_url, company_name, headers)

    # Load BART tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

    # Summarize each article in the DataFrame
    df['Summary'] = df['Text'].apply(lambda text: summarize_text(text, tokenizer, model))

    # Save the DataFrame with summaries to a new CSV
    df.to_csv(f"{company_name.replace(' ', '_')}_summarized_articles.csv", index=False)
    print("Data saved.")

if __name__ == "__main__":
    main()
