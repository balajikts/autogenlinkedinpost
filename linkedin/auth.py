import secrets
import urllib.parse
import requests

from config import (
    LINKEDIN_CLIENT_ID,
    LINKEDIN_CLIENT_SECRET,
    LINKEDIN_REDIRECT_URI,
)


AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

SCOPES = "openid profile w_member_social"


def build_authorization_url():

    state = secrets.token_urlsafe(32)

    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "state": state,
        "scope": SCOPES,
    }

    url = (
        f"{AUTHORIZATION_URL}?"
        f"{urllib.parse.urlencode(params)}"
    )

    return url, state


def exchange_code_for_token(code: str):

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
    }

    response = requests.post(
        TOKEN_URL,
        data=data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()