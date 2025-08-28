import requests

def get_latest_weather_news(location, api_key):
    """
    Fetch latest weather-related news articles for the given location using NewsAPI.
    Uses query 'weather <location>' to filter relevant news.
    """
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=weather {location}&language=en&sortBy=publishedAt&pageSize=10&apiKey={api_key}"
    )
    response = requests.get(url).json()
    articles = []
    for art in response.get("articles", []):
        articles.append({
            "title": art.get("title"),
            "url": art.get("url"),
            "image": art.get("urlToImage") or "https://static.streamlit.io/examples/cat.jpg",
            "source": art.get("source", {}).get("name", "Unknown"),
            "description": art.get("description") or "",
            "published": art.get("publishedAt", "")[:10]
        })
    return articles
