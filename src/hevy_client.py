"""
Hevy REST API Client for Personal Trainer.
Handles fetching workouts, pagination, authentication, and offline mock generation.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

HEVY_API_BASE = "https://api.hevyapp.com/v1"

def get_workouts(api_key: str = None, page_count: int = 5) -> list[dict]:
    """
    Fetches recent workouts from the Hevy API.
    If no API key is provided, falls back to mock data for local testing.
    """
    api_key = api_key or os.environ.get("HEVY_API_KEY")

    if not api_key:
        print("[Notice] No HEVY_API_KEY provided. Using mock training data for local demonstration.")
        return generate_mock_workouts()

    headers = {
        "api-key": api_key,
        "Accept": "application/json",
        "User-Agent": "PersonalTrainer-App"
    }

    all_workouts = []
    page = 1
    page_size = 10

    while page <= page_count:
        url = f"{HEVY_API_BASE}/workouts?page={page}&pageSize={page_size}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                workouts = data.get("workouts", [])
                if not workouts:
                    break
                all_workouts.extend(workouts)
                page += 1
        except urllib.error.HTTPError as e:
            print(f"[Error] Failed to fetch Hevy workouts (HTTP {e.code}): {e.read().decode('utf-8')}")
            break
        except Exception as e:
            print(f"[Error] Failed to connect to Hevy API: {e}")
            break

    print(f"Successfully fetched {len(all_workouts)} workouts from Hevy API.")
    return all_workouts

def generate_mock_workouts() -> list[dict]:
    """
    Generates realistic mock workout sessions over the past 14 days
    reflecting a full body training style with legs alternate.
    """
    now = datetime.now(timezone.utc)
    return [
        {
            "id": "mock_w1",
            "title": "Full Body A (Chest, Back, Quads)",
            "start_time": (now - timedelta(hours=52)).isoformat(),
            "end_time": (now - timedelta(hours=51)).isoformat(),
            "exercises": [
                {
                    "title": "Barbell Squat",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 100, "reps": 8},
                        {"set_type": "normal", "weight_kg": 100, "reps": 8},
                        {"set_type": "normal", "weight_kg": 105, "reps": 6}
                    ]
                },
                {
                    "title": "Flat Bench Press",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 85, "reps": 8},
                        {"set_type": "normal", "weight_kg": 85, "reps": 8},
                        {"set_type": "normal", "weight_kg": 90, "reps": 6}
                    ]
                },
                {
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
                    "title": "Overhead Press",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 50, "reps": 8},
                        {"set_type": "normal", "weight_kg": 50, "reps": 8},
                        {"set_type": "normal", "weight_kg": 52.5, "reps": 6}
                    ]
                },
                {
                    "title": "Dumbbell Bicep Curl",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 16, "reps": 10},
                        {"set_type": "normal", "weight_kg": 16, "reps": 10},
                        {"set_type": "normal", "weight_kg": 16, "reps": 9}
                    ]
                },
                {
                    "title": "Tricep Pushdown",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 25, "reps": 12},
                        {"set_type": "normal", "weight_kg": 25, "reps": 12},
                        {"set_type": "normal", "weight_kg": 30, "reps": 10}
                    ]
                }
            ]
        },
        {
            "id": "mock_w3",
            "title": "Upper Body & Core",
            "start_time": (now - timedelta(days=5)).isoformat(),
            "end_time": (now - timedelta(days=5, hours=-1)).isoformat(),
            "exercises": [
                {
                    "title": "Incline Dumbbell Bench Press",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 30, "reps": 10},
                        {"set_type": "normal", "weight_kg": 30, "reps": 9},
                        {"set_type": "normal", "weight_kg": 30, "reps": 8}
                    ]
                },
                {
                    "title": "Seated Cable Row",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 65, "reps": 10},
                        {"set_type": "normal", "weight_kg": 65, "reps": 10},
                        {"set_type": "normal", "weight_kg": 70, "reps": 8}
                    ]
                },
                {
                    "title": "Hanging Leg Raise",
                    "sets": [
                        {"set_type": "normal", "weight_kg": 0, "reps": 15},
                        {"set_type": "normal", "weight_kg": 0, "reps": 12}
                    ]
                }
            ]
        }
    ]
