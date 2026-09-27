def request_human_approval(
    content: str
) -> bool:

    print(
        "\n========================================"
    )

    print(
        "\nHUMAN APPROVAL REQUIRED"
    )

    print(
        "\n========================================\n"
    )

    print(
        content
    )

    print(
        "\n========================================"
    )

    while True:

        choice = input(
            "\nApprove this LinkedIn post? "
            "(yes/no): "
        ).strip().lower()

        if choice in ["yes", "y"]:

            print(
                "\n✅ Content approved by human."
            )

            return True

        if choice in ["no", "n"]:

            print(
                "\n❌ Content rejected by human."
            )

            return False

        print(
            "\nPlease enter yes or no."
        )