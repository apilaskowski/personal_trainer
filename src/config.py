"""
Configuration constants for Personal Trainer.
Defines target weekly working sets and recovery thresholds.
All exercise-to-muscle classifications are handled directly via Hevy API templates.
"""

DEFAULT_WEEKLY_GOALS = {
    "Chest": 12,
    "Lats": 10,
    "Upper / Mid Back": 8,
    "Quads": 10,
    "Hamstrings": 10,
    "Glutes": 8,
    "Shoulders": 12,
    "Biceps": 8,
    "Triceps": 8,
    "Calves": 6,
    "Hip Adductors": 4,
    "Hip Abductors": 4,
    "Abs / Core": 6
}

DEFAULT_RECOVERY_HOURS = 48.0
RECOVERY_THRESHOLD_HOURS = 48.0  # Alias for backward compatibility

# Default recovery threshold hours per muscle group
DEFAULT_RECOVERY_THRESHOLDS = {
    "Chest": 48.0,
    "Lats": 48.0,
    "Upper / Mid Back": 48.0,
    "Quads": 48.0,
    "Hamstrings": 48.0,
    "Glutes": 48.0,
    "Shoulders": 48.0,
    "Biceps": 48.0,
    "Triceps": 48.0,
    "Calves": 48.0,
    "Hip Adductors": 48.0,
    "Hip Abductors": 48.0,
    "Abs / Core": 48.0
}
