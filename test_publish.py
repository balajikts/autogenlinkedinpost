from linkedin.member import get_member_urn
from linkedin.publisher import publish_post


def main():

    print("\n========================================")
    print(" LinkedIn API Publishing Test")
    print("========================================")

    # Get authenticated member URN
    author_urn = get_member_urn()

    print("\n✅ LinkedIn member identified.")
    print("Author URN:", author_urn)

    # Controlled test post
    test_content = (
        "🚀 Testing my AI LinkedIn Content Agent.\n\n"
        "This is a controlled API publishing test "
        "from my AutoGen + Streamlit application.\n\n"
        "#AI #Automation #AutoGen"
    )

    print("\nPublishing test post...")

    post_id = publish_post(
        author_urn=author_urn,
        post_text=test_content,
    )

    print("\n========================================")
    print(" TEST PUBLISH SUCCESSFUL")
    print("========================================")

    print("\nPost ID:")
    print(post_id)


if __name__ == "__main__":
    main()