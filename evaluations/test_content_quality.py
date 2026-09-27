from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric


def test_linkedin_content_relevance():

    topic = "Agentic AI"

    actual_output = """
Agentic AI is changing how AI systems can reason,
plan and execute tasks.

AI agents can work toward defined goals,
interact with tools and coordinate multiple steps.

Organizations are exploring agentic AI for
software engineering, customer support,
automation and enterprise workflows.

How are you exploring AI agents in your organization?
"""

    test_case = LLMTestCase(
        input=topic,
        actual_output=actual_output,
    )

    relevance_metric = AnswerRelevancyMetric(
        threshold=0.7
    )

    assert_test(
        test_case,
        [relevance_metric]
    )