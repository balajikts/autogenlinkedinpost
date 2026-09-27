import serpapi

from config import SERPAPI_KEY


client = serpapi.Client(
    api_key=SERPAPI_KEY
)


def search_web(query: str) -> str:
    """
    Search Google through SerpApi and return
    structured results for the Research Agent.
    """

    results = client.search(
        {
            "engine": "google",
            "q": query,
            "hl": "en",
            "gl": "in",
            "num": 10,
        }
    )

    organic_results = results.get(
        "organic_results",
        []
    )

    if not organic_results:
        return "No web search results found."

    output = []

    for index, result in enumerate(
        organic_results[:10],
        start=1
    ):

        output.append(
            f"""
SOURCE {index}

TITLE:
{result.get("title", "")}

URL:
{result.get("link", "")}

SNIPPET:
{result.get("snippet", "")}
"""
        )

    return "\n".join(output)