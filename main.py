import asyncio

from team import run_team


async def main():

    topic = "Latest developments in Agentic AI"

    result = await run_team(topic)

    print(
        "\n===== FINAL TEAM OUTPUT =====\n"
    )

    print(
        "\nTOPIC:\n"
    )

    print(
        result["topic"]
    )

    print(
        "\n===== RESEARCH =====\n"
    )

    print(
        result["research"]
    )

    print(
        "\n===== ARTICLE =====\n"
    )

    print(
        result["article"]
    )

    print(
        "\n===== FINAL LINKEDIN CONTENT =====\n"
    )

    print(
        result["final_content"]
    )


if __name__ == "__main__":

    asyncio.run(main())