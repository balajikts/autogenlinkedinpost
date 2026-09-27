from guardrails.content_guardrail import validate_content


def main():

    sample_content = """
FINAL LINKEDIN POST

Agentic AI is changing how software systems
can reason, plan and execute tasks.

SEO KEYWORDS

Agentic AI, AI Agents, Generative AI

HASHTAGS

#AgenticAI #GenerativeAI #AI

CALL TO ACTION

How are you exploring AI agents in your organization?

SOURCE REFERENCES

https://example.com/agentic-ai
"""

    topic = "Quantum Computin"

    passed, errors = validate_content(
        sample_content,
        topic
    )

    print("\n===== GUARDRAIL RESULT =====")

    print(
        "PASSED:",
        passed
    )

    if errors:

        print("\nERRORS:")

        for error in errors:

            print(
                "-",
                error
            )


if __name__ == "__main__":
    main()