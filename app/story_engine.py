import json
from .models import Story, StoryRequest
from .llm_client import call_llm


CANONICAL_PROMPT = """
SYSTEM ROLE:
You are a mythological historian and cultural chronicler.

TASK:
Narrate ONLY events that are documented in canonical mythology, scriptures,
epics, or widely accepted traditional sources of the selected culture.

CULTURE:
{culture}

ANCHOR ENTITY (USER-PROVIDED — DO NOT ALTER):
{anchor}

MANDATORY RULES:
- Describe ONLY events that happened in the past
- Focus ONLY on the anchor entity exactly as written
- Do NOT introduce other gods or heroes
- Do NOT invent new events
- Do NOT add morals, lessons, or interpretations
- Do NOT modernize language or symbolism
- Use factual, traditional narration only

OUTPUT FORMAT:
Return ONLY valid JSON.

{{
  "scenes": [
    {{
      "title": "Scene title",
      "text": "Historically accurate narrative",
      "visual_prompt": "Accurate visual faithful to the culture"
    }}
  ]
}}
"""


def generate_story_pipeline(req: StoryRequest) -> Story:
    if req.mode != "cultural":
        raise ValueError("Only cultural mode is supported")

    anchor = req.user_input.strip()
    if not anchor:
        raise ValueError("User input is required")

    prompt = CANONICAL_PROMPT.format(
        culture=req.culture,
        anchor=anchor
    )

    raw = call_llm(prompt)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")

    if "scenes" not in parsed or not parsed["scenes"]:
        raise ValueError("No scenes returned")

    return Story(**parsed)
