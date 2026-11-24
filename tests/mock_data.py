"""
Mock workout fixtures for offline unit tests.
Isolated under tests/ so production code only interacts with the real Hevy API.
"""

from datetime import datetime, timedelta, timezone

def generate_mock_workouts() -> list[dict]:
    """Generates realistic mock workout sessions over the past 14 days for unit testing."""
    now = datetime.now(timezone.utc)
    return [
        {
            "id": "mock_w1",
            "title": "Full Body A (Chest, Back, Quads)",
            "start_time": (now - timedelta(hours=52)).isoformat(),
            "end_time": (now - timedelta(hours=51)).isoformat(),
            "exercises": [
                {
                    "exercise_template_id": "mock-squat",
                    "title": "Barbell Squat",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 100, "reps": 8},
                        {"set_type": "normal", "weight_kg": 100, "reps": 8},
                        {"set_type": "normal", "weight_kg": 105, "reps": 6}
                    ]
                },
                {
                    "exercise_template_id": "mock-wall-sit",
                    "title": "Wall Sit",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 0, "reps": 60},
                        {"set_type": "normal", "weight_kg": 0, "reps": 60}
                    ]
                },
                {
                    "exercise_template_id": "mock-bench",
                    "title": "Flat Bench Press",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 85, "reps": 8},
                        {"set_type": "normal", "weight_kg": 85, "reps": 8},
                        {"set_type": "normal", "weight_kg": 90, "reps": 6}
                    ]
                },
                {
                    "exercise_template_id": "mock-pulldown",
                    "title": "Lat Pulldown",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 70, "reps": 10},
                        {"set_type": "normal", "weight_kg": 70, "reps": 10},
                        {"set_type": "normal", "weight_kg": 75, "reps": 8}
                    ]
                }
            ]
        },
        {
            "id": "mock_w2",
            "title": "Full Body B (Upper Focus - Skipped Legs)",
            "start_time": (now - timedelta(hours=22)).isoformat(),
            "end_time": (now - timedelta(hours=21)).isoformat(),
            "exercises": [
                {
                    "exercise_template_id": "mock-ohp",
                    "title": "Overhead Press",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 50, "reps": 8},
                        {"set_type": "normal", "weight_kg": 50, "reps": 8},
                        {"set_type": "normal", "weight_kg": 52.5, "reps": 6}
                    ]
                },
                {
                    "exercise_template_id": "mock-curl",
                    "title": "Dumbbell Bicep Curl",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 16, "reps": 10},
                        {"set_type": "normal", "weight_kg": 16, "reps": 10},
                        {"set_type": "normal", "weight_kg": 16, "reps": 9}
                    ]
                },
                {
                    "exercise_template_id": "mock-pushdown",
                    "title": "Tricep Pushdown",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 25, "reps": 12},
                        {"set_type": "normal", "weight_kg": 25, "reps": 12},
                        {"set_type": "normal", "weight_kg": 30, "reps": 10}
                    ]
                }
            ]
        }
    ]
