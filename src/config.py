"""
Configuration and Exercise Taxonomy for Personal Trainer.
Defines weekly set targets, recovery thresholds, and mapping from exercise titles to muscle groups.
"""

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

# Comprehensive exercise-to-muscle mapping for Hevy standard and custom exercises
EXERCISE_MUSCLE_MAP = {
    # Chest
    "bench press": ["Chest", "Triceps"],
    "incline bench press": ["Chest", "Shoulders"],
    "dumbbell bench press": ["Chest", "Triceps"],
    "incline dumbbell bench press": ["Chest", "Shoulders"],
    "decline bench press": ["Chest", "Triceps"],
    "chest fly": ["Chest"],
    "dumbbell fly": ["Chest"],
    "pec deck": ["Chest"],
    "cable crossover": ["Chest"],
    "push up": ["Chest", "Triceps"],
    "dip": ["Chest", "Triceps"],

    # Back
    "pull up": ["Back", "Biceps"],
    "chin up": ["Back", "Biceps"],
    "lat pulldown": ["Back", "Biceps"],
    "seated cable row": ["Back"],
    "barbell row": ["Back"],
    "bent over row": ["Back"],
    "pendlay row": ["Back"],
    "dumbbell row": ["Back"],
    "t-bar row": ["Back"],
    "cable row": ["Back"],
    "deadlift": ["Back", "Hamstrings", "Glutes"],
    "romanian deadlift": ["Hamstrings", "Glutes", "Back"],
    "hyperextension": ["Back", "Glutes"],
    "back extension": ["Back", "Glutes"],
    "face pull": ["Shoulders", "Back"],

    # Quads
    "squat": ["Quads", "Glutes"],
    "barbell squat": ["Quads", "Glutes"],
    "front squat": ["Quads"],
    "goblet squat": ["Quads"],
    "leg press": ["Quads"],
    "hack squat": ["Quads"],
    "leg extension": ["Quads"],
    "lunge": ["Quads", "Glutes"],
    "walking lunge": ["Quads", "Glutes"],
    "bulgarian split squat": ["Quads", "Glutes"],

    # Hamstrings
    "leg curl": ["Hamstrings"],
    "seated leg curl": ["Hamstrings"],
    "lying leg curl": ["Hamstrings"],
    "stiff leg deadlift": ["Hamstrings", "Glutes"],
    "nordic curl": ["Hamstrings"],

    # Glutes
    "hip thrust": ["Glutes"],
    "barbell hip thrust": ["Glutes"],
    "glute bridge": ["Glutes"],
    "cable kickback": ["Glutes"],

    # Calves
    "calf raise": ["Calves"],
    "standing calf raise": ["Calves"],
    "seated calf raise": ["Calves"],

    # Shoulders
    "overhead press": ["Shoulders", "Triceps"],
    "military press": ["Shoulders", "Triceps"],
    "dumbbell shoulder press": ["Shoulders", "Triceps"],
    "shoulder press": ["Shoulders", "Triceps"],
    "arnold press": ["Shoulders"],
    "lateral raise": ["Shoulders"],
    "dumbbell lateral raise": ["Shoulders"],
    "cable lateral raise": ["Shoulders"],
    "front raise": ["Shoulders"],
    "reverse fly": ["Shoulders"],
    "rear delt fly": ["Shoulders"],
    "upright row": ["Shoulders", "Traps"],

    # Arms - Biceps
    "bicep curl": ["Biceps"],
    "barbell curl": ["Biceps"],
    "dumbbell curl": ["Biceps"],
    "dumbbell bicep curl": ["Biceps"],
    "hammer curl": ["Biceps"],
    "preacher curl": ["Biceps"],
    "cable curl": ["Biceps"],
    "concentration curl": ["Biceps"],

    # Arms - Triceps
    "tricep pushdown": ["Triceps"],
    "cable tricep extension": ["Triceps"],
    "tricep extension": ["Triceps"],
    "skull crusher": ["Triceps"],
    "overhead tricep extension": ["Triceps"],
    "close grip bench press": ["Triceps", "Chest"],

    # Abs / Core
    "crunch": ["Abs"],
    "plank": ["Abs"],
    "hanging leg raise": ["Abs"],
    "leg raise": ["Abs"],
    "cable crunch": ["Abs"],
    "ab wheel": ["Abs"],
    "russian twist": ["Abs"]
}

def map_exercise_to_muscles(exercise_title: str) -> list[str]:
    """
    Maps an exercise title string to one or more muscle groups.
    Uses exact key search first, followed by keyword heuristics.
    """
    if not exercise_title:
        return ["Other"]

    title_lower = exercise_title.lower().strip()

    # 1. Exact or partial match in dictionary
    for key, muscles in EXERCISE_MUSCLE_MAP.items():
        if key in title_lower:
            return muscles

    # 2. Heuristic fallback rules
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
