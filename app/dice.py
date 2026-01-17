import random
from .models import Fate

ORIGINS = [
    "Ancient India",
    "Japanese Folklore",
    "African Tribal Myth",
    "Greek Mythology",
    "Norse Legends"
]

EMOTIONS = ["Hope", "Loss", "Courage", "Faith", "Sacrifice"]
LESSONS = [
    "Kindness returns in unexpected ways",
    "Pride leads to downfall",
    "Wisdom comes through suffering"
]

def roll_fate() -> Fate:
    return Fate(
        origin=random.choice(ORIGINS),
        emotion=random.choice(EMOTIONS),
        lesson=random.choice(LESSONS)
    )
