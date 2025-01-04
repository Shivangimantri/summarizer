import requests
from newspaper import Article

def fetch_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# Replace with your NewsAPI key
API_KEY = "YOUR_NEWSAPI"

# Function to fetch news articles
def fetch_news(query, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,  # Query term
        "pageSize": page_size,  # Number of articles
        "apiKey": API_KEY  # Your API key
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


# Example usage
if __name__ == "__main__":
    query = "technology"  # Replace with your topic of interest
    articles = fetch_news(query, page_size=3) 
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"Article {i}:")
            print(f"Title: {article['title']}")
            print(f"Text: {article['text']}")
            print(f"Link: {article['link']}")
            print(f"Publisher: {article['publisher']}")
            print(f"Full-text: {fetch_article_text(article['link'])}")
            print("-" * 50)






