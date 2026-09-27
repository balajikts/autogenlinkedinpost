import json
import requests


TOKEN_FILE = ".linkedin_token.json"

LINKEDIN_POST_URL = "https://api.linkedin.com/rest/posts"

LINKEDIN_VERSION = "202609"


def load_access_token():

    with open(
        TOKEN_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        token_data = json.load(file)

    access_token = token_data.get("access_token")

    if not access_token:
        raise RuntimeError(
            "LinkedIn access token was not found."
        )

    return access_token


def create_linkedin_post(
    author_urn: str,
    post_text: str
):

    access_token = load_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": LINKEDIN_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": author_urn,
        "commentary": post_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    response = requests.post(
        LINKEDIN_POST_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code not in (200, 201):

        raise RuntimeError(
            "LinkedIn API error: "
            f"{response.status_code} - "
            f"{response.text}"
        )

    return response


def publish_post(
    author_urn: str,
    post_text: str
):

    if not author_urn:
        raise ValueError(
            "LinkedIn author URN is required."
        )

    if not post_text.strip():
        raise ValueError(
            "Post content cannot be empty."
        )

    response = create_linkedin_post(
        author_urn=author_urn,
        post_text=post_text,
    )

    post_id = response.headers.get(
        "x-restli-id"
    )

    print(
        "\n========================================"
    )
    print(
        " LinkedIn Post Published"
    )
    print(
        "========================================"
    )

    print(
        f"\nPost ID: {post_id}"
    )

    return post_id