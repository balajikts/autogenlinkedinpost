import json
import requests


TOKEN_FILE = ".linkedin_token.json"

USERINFO_URL = "https://api.linkedin.com/v2/userinfo"


def load_access_token():

    with open(
        TOKEN_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        token_data = json.load(file)

    return token_data["access_token"]


def get_linkedin_member():

    access_token = load_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        USERINFO_URL,
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"LinkedIn UserInfo API error: "
            f"{response.status_code} - "
            f"{response.text}"
        )

    data = response.json()

    member_id = data.get("sub")

    if not member_id:

        raise RuntimeError(
            "LinkedIn UserInfo response did not contain 'sub'."
        )

    return {
        "member_id": member_id,
        "name": data.get("name"),
        "given_name": data.get("given_name"),
        "family_name": data.get("family_name"),
        "email": data.get("email"),
        "picture": data.get("picture"),
    }


def get_member_urn():

    member = get_linkedin_member()

    return f"urn:li:person:{member['member_id']}"


if __name__ == "__main__":

    member = get_linkedin_member()

    print("\n========================================")
    print(" LinkedIn Member Information")
    print("========================================")

    print("\nMember ID:")
    print(member["member_id"])

    print("\nName:")
    print(member["name"])

    print("\nMember URN:")
    print(
        f"urn:li:person:{member['member_id']}"
    )