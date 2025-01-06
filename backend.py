from flask import Flask, request, jsonify
from newspaper import Article
from transformers import pipeline
import requests

from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

API_KEY = "YOUR_KEY"

def fetch_news(query, page_size):
    url = "https://newsapi.org/v2/everything"
    params = {"q": query, "pageSize": page_size, "apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["articles"]
    else:
        return None

def fetch_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def summarize_text(text, max_length=150, min_length=50, max_input_length=4800):
    summary = summarizer(text[0:max_input_length], max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

@app.route("/summarize-news", methods=["POST"])
def summarize_news():
    data = request.json
    query = data.get("query")
    page_size = data.get("page_size", 3)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    articles = fetch_news(query, page_size)
    if not articles:
        return jsonify({"error": "Failed to fetch news"}), 500

    results = []
    for article in articles:
        try:
            full_text = fetch_article_text(article["url"])
            summary = summarize_text(full_text)
            results.append({
                "title": article["title"],
                "summary": summary,
                "link": article["url"],
                "publisher": article["source"]["name"]
            })
        except Exception as e:
            continue  # Skip articles that cannot be processed

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)