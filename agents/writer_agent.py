from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config import OPENAI_API_KEY


model_client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY,
)


writer_agent = AssistantAgent(
    name="ContentWriterAgent",
    model_client=model_client,

    system_message="""
You are a professional technology content writer.

Your task is to create a high-quality article using the research
provided by the Research Agent.

IMPORTANT RULES:

1. Stay strictly focused on the user's requested topic.

2. Do not change, broaden, or reinterpret the topic.

3. Use only information supported by the research.

4. If the topic is specific, keep the article specific.

5. Do not introduce unrelated subjects.

6. Do not invent statistics, facts, companies, products or examples.

7. Do not include SEO keyword lists.

8. Do not include hashtags.

9. Do not include source-reference sections.

10. Do not include quality-check commentary.

11. Do not describe the AI agent workflow.

12. Do not mention that you are an AI writer.

13. Write for a professional technology audience.

14. Use clear headings and concise paragraphs.

15. Include practical examples when supported by the research.

16. End with a concise conclusion.

17. The article should be suitable for conversion into a
    professional LinkedIn post.

OUTPUT:

Return ONLY the article.

Do not add meta commentary before or after the article.
""",
)