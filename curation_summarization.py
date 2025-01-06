import requests
from newspaper import Article
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

API_KEY = "YOUR_API_KEY"

def fetch_news(query, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": page_size,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = []
        for article in data["articles"]:
            articles.append({
                "title": article.get("title"),
                "text": article.get("description"),
                "link": article.get("url"),
                "publisher": article.get("source", {}).get("name")
            })
        return articles
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def summarize_text(text, max_length=150, min_length=50, max_input_length=4800):
    summary = summarizer(text[0:max_input_length], max_length=max_length, min_length=min_length, do_sample=False)
    #ummary = summarizer(text)
    return summary[0]['summary_text']

if __name__ == "__main__":
    query = "technology"
    articles = fetch_news(query, page_size=3)
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"Article {i}:")
            print(f"Title: {article['title']}")
            full_text = fetch_article_text(article['link'])
            summary = summarize_text(full_text)
            print(f"Summary: {summary}")
            print(f"Link: {article['link']}")
            print(f"Publisher: {article['publisher']}")
            print("-" * 50)
