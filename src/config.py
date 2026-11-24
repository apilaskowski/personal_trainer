"""
Configuration constants for Personal Trainer.
Defines target weekly working sets and recovery thresholds.
All exercise-to-muscle classifications are handled directly via Hevy API templates.
"""

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

RECOVERY_THRESHOLD_HOURS = 48.0
