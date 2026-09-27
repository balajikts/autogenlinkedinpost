import asyncio

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

from guardrails.content_guardrail import validate_content
from evaluations.content_evaluator import evaluate_content

from agents.research_agent import research_agent
from agents.writer_agent import writer_agent
from agents.seo_linkedin_agent import seo_linkedin_agent


# ==========================================
# TEAM TERMINATION
# ==========================================

termination = TextMentionTermination(
    "CONTENT OPTIMIZATION COMPLETE"
)


# ==========================================
# AUTOGEN TEAM
# ==========================================

team = RoundRobinGroupChat(
    participants=[
        research_agent,
        writer_agent,
        seo_linkedin_agent,
    ],
    termination_condition=termination,
    max_turns=6,
)


# ==========================================
# RUN TEAM
# ==========================================

async def run_team(topic: str):

    task = f"""
Create a LinkedIn post about:

{topic}

Follow this workflow:

Research Agent:
Research current information using web search.

Writer Agent:
Use the research to create the article.

SEO LinkedIn Agent:
Optimize the article for LinkedIn and SEO.

Do not publish anything.

Return the final optimized content.
"""

    # ==========================================
    # RUN AUTOGEN TEAM
    # ==========================================

    result = await team.run(
        task=task
    )

    # ==========================================
    # EXTRACT AGENT OUTPUTS
    # ==========================================

    research_text = None
    article_text = None
    final_content = None

    for message in result.messages:

        content = message.content

        if not isinstance(content, str):
            continue

        # ------------------------------------------
        # Research Agent
        # ------------------------------------------

        if message.source == "ResearchAgent":

            research_text = content

        # ------------------------------------------
        # Writer Agent
        # ------------------------------------------

        elif message.source == "ContentWriterAgent":

            article_text = content

        # ------------------------------------------
        # SEO Agent
        # ------------------------------------------

        elif message.source == "SEOLinkedInAgent":

            final_content = content

    # ==========================================
    # DEBUG INFORMATION
    # ==========================================

    print(
        "\n===== EXTRACTED PIPELINE DATA =====\n"
    )

    print(
        "Research captured:",
        bool(research_text)
    )

    print(
        "Article captured:",
        bool(article_text)
    )

    print(
        "Final content captured:",
        bool(final_content)
    )

    # ==========================================
    # VALIDATE TEAM OUTPUT
    # ==========================================

    if not research_text:

        raise ValueError(
            "Research Agent did not produce research."
        )

    if not article_text:

        raise ValueError(
            "Writer Agent did not produce an article."
        )

    if not final_content:

        raise ValueError(
            "SEO Agent did not produce final content."
        )

    # ==========================================
    # GUARDRAILS
    # ==========================================
    passed, errors = validate_content(
    content=final_content,
    topic=topic,
    research=research_text,
)

    print(
        "\n===== GUARDRAIL RESULT =====\n"
    )

    print(
        "PASSED:",
        passed
    )

    if errors:

        print(
            "\nGUARDRAIL ERRORS:"
        )

        for error in errors:

            print(
                "-",
                error
            )

    # ==========================================
    # BLOCK FAILED CONTENT
    # ==========================================

    if not passed:

        raise ValueError(
            "Content failed guardrails. "
            "Publishing must be stopped."
        )

    # ==========================================
    # DEEPEVAL QUALITY EVALUATION
    # ==========================================

    print(
        "\n===== RUNNING DEEPEVAL =====\n"
    )

    evaluate_content(
        topic=topic,
        research=research_text,
        final_content=final_content,
    )

    print(
        "\n===== DEEPEVAL PASSED =====\n"
    )

    # ==========================================
    # RETURN STRUCTURED RESULT
    #
    # Human approval is now handled by Streamlit.
    # ==========================================

    return {
        "topic": topic,
        "research": research_text,
        "article": article_text,
        "final_content": final_content,
    }


# ==========================================
# DIRECT TEST
# ==========================================

if __name__ == "__main__":

    async def main():

        result = await run_team(
            "Latest developments in Agentic AI"
        )

        print(
            "\n===== TEAM RESULT =====\n"
        )

        print(
            "\nTOPIC:\n",
            result["topic"]
        )

        print(
            "\nRESEARCH:\n",
            result["research"]
        )

        print(
            "\nARTICLE:\n",
            result["article"]
        )

        print(
            "\nFINAL CONTENT:\n",
            result["final_content"]
        )

    asyncio.run(main())