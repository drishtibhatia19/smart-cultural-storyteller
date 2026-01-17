from typing import List
from pydantic import BaseModel
from typing_extensions import Literal


class Scene(BaseModel):
    title: str
    text: str
    visual_prompt: str


class Story(BaseModel):
    scenes: List[Scene]


class StoryRequest(BaseModel):
    culture: str
    mode: Literal["cultural"]   # 🔒 cultural only
    user_input: str             # 🔒 THIS is the anchor entity
