import os
import httpx
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2"


class NewsAPIError(Exception):
    pass


def search_news(query: str, language: str = "en", page_size: int = 5):
    if not NEWS_API_KEY:
        raise NewsAPIError("NEWSAPI_KEY is not set")

    params = {
        "q": query,
        "language": language,
        "pageSize": page_size,
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    try:
        response = httpx.get(
            f"{BASE_URL}/everything",
            params=params,
            headers=headers,
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.TimeoutException:
        raise NewsAPIError("News API request timed out")
    except httpx.HTTPStatusError as e:
        raise NewsAPIError(f"News API error: {e.response.status_code}")

    data = response.json()
    articles = data.get("articles", [])

    if not articles:
        return []

    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "published_at": a["publishedAt"],
        }
        for a in articles
    ]


def get_top_headlines(country: str = "us", page_size: int = 5):
    if not NEWS_API_KEY:
        raise NewsAPIError("NEWSAPI_KEY is not set")

    params = {
        "country": country,
        "pageSize": page_size,
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    try:
        response = httpx.get(
            f"{BASE_URL}/top-headlines",
            params=params,
            headers=headers,
            timeout=10.0,
        )
        response.raise_for_status()
    except httpx.TimeoutException:
        raise NewsAPIError("News API request timed out")
    except httpx.HTTPStatusError as e:
        raise NewsAPIError(f"News API error: {e.response.status_code}")

    data = response.json()
    articles = data.get("articles", [])

    if not articles:
        return []

    return [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"],
            "published_at": a["publishedAt"],
        }
        for a in articles
    ]


# if __name__ == "__main__":
#     print("=== search_news 테스트 ===")
#     try:
#         results = search_news("AI", language="en", page_size=3)
#         for i, article in enumerate(results, 1):
#             print(f"{i}. {article['title']} ({article['source']})")
#     except NewsAPIError as e:
#         print("에러:", e)

#     print("\n=== get_top_headlines 테스트 ===")
#     try:
#         headlines = get_top_headlines(country="us", page_size=3)
#         for i, article in enumerate(headlines, 1):
#             print(f"{i}. {article['title']} ({article['source']})")
#     except NewsAPIError as e:
#         print("에러:", e)


