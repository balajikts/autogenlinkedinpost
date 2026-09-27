import re


def validate_content(
    content: str,
    topic: str,
    research: str = ""
) -> tuple[bool, list[str]]:

    errors = []

    # ==========================================
    # 1. EMPTY CONTENT
    # ==========================================

    if not content or not content.strip():

        errors.append(
            "Content is empty."
        )

        return False, errors


    # ==========================================
    # 2. MINIMUM CONTENT LENGTH
    # ==========================================

    if len(content.strip()) < 300:

        errors.append(
            "Content is too short."
        )


    # ==========================================
    # 3. FINAL LINKEDIN POST CHECK
    # ==========================================

    content_upper = content.upper()

    if "FINAL LINKEDIN POST" not in content_upper:

        errors.append(
            "Missing FINAL LINKEDIN POST section."
        )


    # ==========================================
    # 4. EXTRACT ACTUAL LINKEDIN POST
    # ==========================================

    linkedin_post = content

    if "FINAL LINKEDIN POST" in content_upper:

        linkedin_post = content.split(
            "FINAL LINKEDIN POST",
            1
        )[1]

    if "CONTENT OPTIMIZATION COMPLETE" in linkedin_post.upper():

        linkedin_post = linkedin_post.split(
            "CONTENT OPTIMIZATION COMPLETE",
            1
        )[0]

    linkedin_post = linkedin_post.strip()


   # ==========================================
# 5. SOURCE URL VALIDATION
# ==========================================

# Source URLs belong to the research evidence,
# not necessarily inside the publishable LinkedIn post.

    url_pattern = r"https?://[^\s]+"

    research_urls = re.findall(
    url_pattern,
    research
)

    if len(research_urls) == 0:

     errors.append(

        "No source URLs detected in research."
    )
    # ==========================================
    # 6. STATISTIC / NUMERIC CLAIM CHECK
    # ==========================================

    statistic_patterns = [

        # Percentage claims
        r"\b\d+(?:\.\d+)?%\s+(?:of|increase|decrease|growth|reduction|rise|drop)",

        r"\b\d+(?:\.\d+)?%\s+(?:more|less|higher|lower)",

        r"\b(?:increase|decrease|growth|reduction|rise|drop)\s+of\s+\d+(?:\.\d+)?%",

        # Currency claims
        r"\$\s?\d+(?:\.\d+)?\s*(?:million|billion|trillion)?",

        # Large numeric claims
        r"\b\d+(?:\.\d+)?\s*(?:million|billion|trillion)\s+"
        r"(?:users|people|dollars|USD|companies|organizations)",
    ]


    for pattern in statistic_patterns:

        if re.search(
            pattern,
            linkedin_post,
            re.IGNORECASE
        ):

            errors.append(
                "Potential statistic detected. "
                "Verify against the research sources."
            )

            break


    # ==========================================
    # 7. PROMPT INJECTION / SAFETY
    # ==========================================

    forbidden_phrases = [

        "ignore previous instructions",

        "system prompt",

        "reveal your instructions",

        "bypass guardrail",

    ]


    for phrase in forbidden_phrases:

        if phrase.lower() in content.lower():

            errors.append(
                f"Potential prompt injection detected: {phrase}"
            )


    # ==========================================
    # 8. TOPIC RELEVANCE
    # ==========================================

    topic_lower = topic.lower()

    content_lower = linkedin_post.lower()


    stop_words = {

        "latest",

        "developments",

        "development",

        "information",

        "about",

        "with",

        "from",

        "into",

        "what",

        "this",

        "that",

        "technology",

        "technologies",

        "how",

        "can",

        "does",

        "the",

        "and",

        "for",

    }


    topic_words = [

        word.strip(".,!?():;")

        for word in topic_lower.split()

        if len(word.strip(".,!?():;")) > 3

        and word.strip(".,!?():;") not in stop_words

    ]


    # ==========================================
    # DIRECT TOPIC MATCH
    # ==========================================

    matching_words = [

        word

        for word in topic_words

        if word in content_lower

    ]


    # ==========================================
    # TOPIC ALIASES
    # ==========================================

    topic_aliases = {

        "agentic": [

            "agentic ai",

            "ai agent",

            "ai agents",

            "autonomous agent",

            "autonomous agents",

        ],

        "ai": [

            "artificial intelligence",

            "ai",

            "agentic ai",

        ],

        "earth": [

            "earth observation",

            "earth science",

            "satellite",

            "geospatial",

            "remote sensing",

        ],

        "observation": [

            "earth observation",

            "remote sensing",

            "satellite imagery",

            "geospatial",

        ],

        "documents": [

            "document",

            "documents",

            "document processing",

            "document analysis",

        ],

    }


    alias_match = False


    for word in topic_words:

        aliases = topic_aliases.get(
            word,
            []
        )

        if any(
            alias in content_lower
            for alias in aliases
        ):

            alias_match = True

            break


    # ==========================================
    # TOPIC RELEVANCE THRESHOLD
    # ==========================================

    if topic_words:

        # Require at least one meaningful topic
        # word or alias.

        if not matching_words and not alias_match:

            errors.append(
                "Generated content does not appear "
                "to be related to the requested topic."
            )


    # ==========================================
    # 9. FINAL LINKEDIN POST QUALITY CHECK
    # ==========================================

    if len(linkedin_post) < 250:

        errors.append(
            "Final LinkedIn post is too short."
        )


    # ==========================================
    # FINAL RESULT
    # ==========================================

    passed = len(errors) == 0

    return passed, errors