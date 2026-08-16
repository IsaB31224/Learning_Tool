import os
import anthropic
from dotenv import load_dotenv

_ENV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "git", ".env"
)
load_dotenv(_ENV_PATH)

_API_KEY = os.environ["ANTHROPIC_API_KEY"]

_SYSTEM_CALL1 = (
    "You are a reflection coach. The user will give you a piece of source content and their initial understanding of it.\n\n"
    "Your job is to generate exactly 3 questions. Each question must be fully written from the specific content and the user's own understanding — not from a generic template.\n\n"
    "The 3 questions must target:\n"
    "1. Where this concept is present or absent in a specific situation in the user's actual life right now, do not suggest specific situations force them to surface one themselves, do not refer to an example from content \n"
    "2. The gap between how they actually behave and how the concept demands they behave explicitly asking them to recall the exact situation getting them to live in the moment\n"
    "3. What is concretely blocking them from closing that gap\n\n"
    "Rules:\n"
    "- Each question must be rooted in something specific from the content or the user's reflection — no generic questions\n"
    "- Push toward a real situation, decision, or behaviour — never back into the concept itself\n"
    "- No preamble, no numbering labels, no headers\n"
    "- Return the 3 questions each on a new line with no other text, formatting, or separators"
)

_SYSTEM_CALL2 = (
    "Your role is to take the structured forms of data regarding a user's encounter with a piece of content and analyse their reflection across the 4 sources. "
    "Using this analysis you will identify a pattern or belief they hold through their own responses. "
    "You will then surface this in the form of a Socratic question with relevant context that leads the user to name their own belief themselves and force them to surface an action which will directly attach this belief.\n\n"
    "Return one question only. No preamble, no analysis, no additional text."
)


def generate_context_questions(source_content, initial_reflection):
    client = anthropic.Anthropic(api_key=_API_KEY)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=_SYSTEM_CALL1,
        messages=[
            {"role": "user", "content": f"Source Content:\n{source_content}\n\nMy understanding:\n{initial_reflection}"}
        ]
    )
    return response.content[0].text.strip().split('\n')


def generate_final_question(source_content, initial_reflection, questions, responses):
    client = anthropic.Anthropic(api_key=_API_KEY)
    content = (
        f"Source Content:\n{source_content}\n\n"
        f"Initial Reflection:\n{initial_reflection}\n\n"
        f"Question 1:\n{questions[0]}\n\nUser's Response to Question 1:\n{responses[0]}\n\n"
        f"Question 2:\n{questions[1]}\n\nUser's Response to Question 2:\n{responses[1]}\n\n"
        f"Question 3:\n{questions[2]}\n\nUser's Response to Question 3:\n{responses[2]}"
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=_SYSTEM_CALL2,
        messages=[{"role": "user", "content": content}]
    )
    return response.content[0].text.strip()
