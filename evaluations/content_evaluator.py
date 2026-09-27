from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


def extract_final_post(content: str) -> str:

    if "FINAL LINKEDIN POST" in content:

        content = content.split(
            "FINAL LINKEDIN POST",
            1
        )[1]

    if "SEO KEYWORDS" in content:

        content = content.split(
            "SEO KEYWORDS",
            1
        )[0]

    return content.strip()


def evaluate_content(
    topic: str,
    research: str,
    final_content: str,
):

    linkedin_post = extract_final_post(
        final_content
    )

    test_case = LLMTestCase(
        input=topic,
        actual_output=linkedin_post,
        retrieval_context=[
            research
        ],
    )

    relevancy_metric = AnswerRelevancyMetric(
        threshold=0.7,
        model="gpt-4.1-mini",
    )

    quality_metric = GEval(
        name="LinkedIn Content Quality",
        criteria="""
Evaluate whether the LinkedIn post:

1. Directly addresses the requested topic.
2. Does not substantially drift into unrelated subjects.
3. Provides useful and accurate information.
4. Is appropriate for a professional LinkedIn audience.
5. Has a clear and readable structure.
6. Avoids unnecessary meta-commentary.
7. Avoids discussing the content-generation process.
8. Avoids SEO keyword lists, source lists, quality checks,
   or internal workflow instructions inside the post.
""",
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
        ],
        threshold=0.7,
        model="gpt-4.1-mini",
    )

    assert_test(
        test_case,
        [
            relevancy_metric,
            quality_metric,
        ],
    )