"""
Build script for Personal Trainer Web Dashboard.
Fetches recent workouts (Hevy API or mock fallback), analyzes recovery,
and generates the static public/data.json file.
"""

import sys
import os

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from src.hevy_client import get_workouts
from src.analyzer import analyze_workouts

def build() -> str:
    """Runs the analysis pipeline and outputs public/data.json."""
    api_key = os.environ.get("HEVY_API_KEY")
    workouts = get_workouts(api_key=api_key)
    analysis = analyze_workouts(workouts, api_key=api_key)

    public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
    os.makedirs(public_dir, exist_ok=True)

    data_file = os.path.join(public_dir, "data.json")
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)

    print(f"Successfully generated: {data_file}")
    print(f"Today's Recommendation: {analysis['today_recommendation']['headline']}")
    return data_file

if __name__ == "__main__":
    build()
