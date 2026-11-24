"""
Configuration and Exercise Taxonomy for Personal Trainer.
Defines weekly set targets, recovery thresholds, and mapping from exercise titles to muscle groups.
"""

import os
import json

# Default weekly target working sets per muscle group
DEFAULT_WEEKLY_GOALS = {
    "Chest": 12,
    "Back": 14,
    "Quads": 10,
    "Hamstrings": 10,
    "Glutes": 8,
    "Shoulders": 12,
    "Biceps": 8,
    "Triceps": 8,
    "Calves": 6,
    "Abs": 6
}

# Standard recovery threshold in hours
RECOVERY_THRESHOLD_HOURS = 48.0

# TODO: Revisit dynamic fetching from Hevy API /v1/exercise_templates.
# Hevy provides primary_muscle_group and secondary_muscle_groups per exercise template.
# For now, we load a structured mapping from exercise_map.json which can be customized without code changes.
_MAP_FILE = os.path.join(os.path.dirname(__file__), "exercise_map.json")

def load_exercise_map() -> dict:
    if os.path.exists(_MAP_FILE):
        with open(_MAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {k: v for k, v in data.items() if not k.startswith("_")}
    return {}

EXERCISE_MUSCLE_MAP = load_exercise_map()

def map_exercise_to_muscles(exercise_title: str) -> list[str]:
    """
    Maps an exercise title string to one or more muscle groups.
    Uses exact key search in structured map first, followed by keyword heuristics.
    """
    if not exercise_title:
        return ["Other"]

    title_lower = exercise_title.lower().strip()

    # 1. Match in structured exercise mapping
    for key, muscles in EXERCISE_MUSCLE_MAP.items():
        if key in title_lower:
            return muscles

    # 2. Heuristic fallback rules for unmapped exercises
    if "squat" in title_lower or "quad" in title_lower:
        return ["Quads"]
    if "deadlift" in title_lower or "rdl" in title_lower:
        return ["Hamstrings", "Back"]
    if "bench" in title_lower or "chest" in title_lower or ("press" in title_lower and "shoulder" not in title_lower and "leg" not in title_lower):
        return ["Chest"]
    if "shoulder" in title_lower or "overhead" in title_lower or "lateral" in title_lower:
        return ["Shoulders"]
    if "pull" in title_lower or "row" in title_lower or "lat" in title_lower:
        return ["Back"]
    if "curl" in title_lower and "leg" not in title_lower and "hamstring" not in title_lower:
        return ["Biceps"]
    if "tricep" in title_lower or "pushdown" in title_lower:
        return ["Triceps"]
    if "calf" in title_lower or "calves" in title_lower:
        return ["Calves"]
    if "abs" in title_lower or "ab" in title_lower or "core" in title_lower:
        return ["Abs"]

    return ["Other"]
