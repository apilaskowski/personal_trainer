"""
Configuration constants for Personal Trainer.
Defines target weekly working sets and recovery thresholds.
All exercise-to-muscle classifications are handled directly via Hevy API templates.
"""

DEFAULT_WEEKLY_GOALS = {
    "Chest": 16,
    "Lats": 10,
    "Upper / Mid Back": 8,
    "Quads": 8,
    "Hamstrings": 8,
    "Glutes": 6,
    "Shoulders": 22,
    "Biceps": 12,
    "Triceps": 10,
    "Calves": 5,
    "Hip Adductors": 4,
    "Hip Abductors": 4,
    "Abs / Core": 8
}

DEFAULT_RECOVERY_HOURS = 48.0
RECOVERY_THRESHOLD_HOURS = 48.0  # Alias for backward compatibility

# Recovery threshold hours per muscle group
DEFAULT_RECOVERY_THRESHOLDS = {
    "Chest": 48.0,
    "Lats": 48.0,
    "Upper / Mid Back": 48.0,
    "Quads": 72.0,
    "Hamstrings": 72.0,
    "Glutes": 48.0,
    "Shoulders": 24.0,
    "Biceps": 36.0,
    "Triceps": 48.0,
    "Calves": 48.0,
    "Hip Adductors": 48.0,
    "Hip Abductors": 48.0,
    "Abs / Core": 24.0
}
