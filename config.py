import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not configured.")

if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY is not configured.")

print("OpenAI key loaded:", OPENAI_API_KEY[:7] + "...")
print("SerpApi key loaded:", SERPAPI_KEY[:7] + "...")

LINKEDIN_CLIENT_ID = os.getenv(
    "LINKEDIN_CLIENT_ID"
)

LINKEDIN_CLIENT_SECRET = os.getenv(
    "LINKEDIN_CLIENT_SECRET"
)

LINKEDIN_REDIRECT_URI = os.getenv(
    "LINKEDIN_REDIRECT_URI"
)

if not LINKEDIN_CLIENT_ID:
    raise ValueError(
        "LINKEDIN_CLIENT_ID is not configured."
    )

if not LINKEDIN_CLIENT_SECRET:
    raise ValueError(
        "LINKEDIN_CLIENT_SECRET is not configured."
    )

if not LINKEDIN_REDIRECT_URI:
    raise ValueError(
        "LINKEDIN_REDIRECT_URI is not configured."
    )