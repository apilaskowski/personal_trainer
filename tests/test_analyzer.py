"""Unit tests for the Workout Analysis and Recommendation Engine."""

import unittest
import json
from datetime import datetime, timedelta, timezone
from src.analyzer import analyze_workouts

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 24, 12, 0, 0, tzinfo=timezone.utc)
        self.goals = {
            "Chest": 10,
            "Back": 12,
            "Quads": 10,
            "Hamstrings": 10,
            "Shoulders": 10
        }

    def test_empty_workouts(self):
        """When no workouts exist, all muscles should be ready and have full deficit."""
        res = analyze_workouts([], weekly_goals=self.goals, current_time=self.now)
        muscles = {m["name"]: m for m in res["muscles"]}

        for name in self.goals:
            self.assertEqual(muscles[name]["recovery_status"], "ready")
            self.assertEqual(muscles[name]["sets_7d"], 0)
            self.assertEqual(muscles[name]["deficit_7d"], self.goals[name])

        self.assertGreater(len(res["today_recommendation"]["focus_muscles"]), 0)

    def test_recent_workout_triggers_resting(self):
        """A workout done 10 hours ago should put trained muscles into 'resting' status."""
        workouts = [
            {
                "id": "w1",
                "start_time": (self.now - timedelta(hours=10)).isoformat(),
                "exercises": [
                    {
                        "exercise_template_id": "mock-bench",
                        "title": "Flat Bench Press",
                        "sets": [
                            {"set_type": "normal", "weight_kg": 80, "reps": 10},
                            {"set_type": "normal", "weight_kg": 80, "reps": 10}
                        ]
                    }
                ]
            }
        ]

        res = analyze_workouts(workouts, weekly_goals=self.goals, current_time=self.now)
        muscles = {m["name"]: m for m in res["muscles"]}

        self.assertEqual(muscles["Chest"]["recovery_status"], "resting")
        self.assertEqual(muscles["Chest"]["sets_7d"], 2)
        self.assertEqual(muscles["Chest"]["deficit_7d"], 8)
        self.assertNotIn("Chest", res["today_recommendation"]["focus_muscles"])

    def test_recovering_status(self):
        """A workout done 30 hours ago should be in 'recovering' status (24h - 48h)."""
        workouts = [
            {
                "id": "w1",
                "start_time": (self.now - timedelta(hours=30)).isoformat(),
                "exercises": [
                    {
                        "exercise_template_id": "mock-pulldown",
                        "title": "Lat Pulldown",
                        "sets": [
                            {"set_type": "normal", "weight_kg": 70, "reps": 10},
                            {"set_type": "normal", "weight_kg": 70, "reps": 10}
                        ]
                    }
                ]
            }
        ]

        res = analyze_workouts(workouts, weekly_goals=self.goals, current_time=self.now)
        muscles = {m["name"]: m for m in res["muscles"]}

        self.assertEqual(muscles["Back"]["recovery_status"], "recovering")
        self.assertNotIn("Back", res["today_recommendation"]["focus_muscles"])

    def test_independent_muscle_recovery(self):
        """Hitting Quads while skipping Hamstrings leaves Hamstrings ready."""
        workouts = [
            {
                "id": "w1",
                "start_time": (self.now - timedelta(hours=12)).isoformat(),
                "exercises": [
                    {
                        "exercise_template_id": "mock-leg-extension",
                        "title": "Leg Extension",
                        "sets": [
                            {"set_type": "normal", "weight_kg": 60, "reps": 12},
                            {"set_type": "normal", "weight_kg": 60, "reps": 12}
                        ]
                    }
                ]
            }
        ]

        res = analyze_workouts(workouts, weekly_goals=self.goals, current_time=self.now)
        muscles = {m["name"]: m for m in res["muscles"]}

        self.assertEqual(muscles["Quads"]["recovery_status"], "resting")
        self.assertEqual(muscles["Hamstrings"]["recovery_status"], "ready")
        self.assertIn("Hamstrings", res["today_recommendation"]["focus_muscles"])
        self.assertNotIn("Quads", res["today_recommendation"]["focus_muscles"])

    def test_priority_ranking_by_deficit(self):
        """Ready muscles with the largest deficit should be prioritized first."""
        custom_goals = {
            "Back": 12,
            "Hamstrings": 10
        }
        workouts = [
            # 55 hours ago: did 6 sets of Back and 2 sets of Hamstrings
            {
                "id": "w1",
                "start_time": (self.now - timedelta(hours=55)).isoformat(),
                "exercises": [
                    {
                        "exercise_template_id": "mock-cable-row",
                        "title": "Seated Cable Row",
                        "sets": [{"set_type": "normal"} for _ in range(6)]
                    },
                    {
                        "exercise_template_id": "mock-leg-curl",
                        "title": "Lying Leg Curl",
                        "sets": [{"set_type": "normal"} for _ in range(2)]
                    }
                ]
            }
        ]

        res = analyze_workouts(workouts, weekly_goals=custom_goals, current_time=self.now)
        rec = res["today_recommendation"]["focus_muscles"]

        # Back deficit: 12 - 6 = 6. Hamstrings deficit: 10 - 2 = 8.
        # Both are ready (55h ago). Hamstrings has higher deficit (8 vs 6), so it ranks before Back!
        self.assertIn("Hamstrings", rec)
        self.assertIn("Back", rec)
        self.assertEqual(rec[0], "Hamstrings")
        self.assertEqual(rec[1], "Back")

    def test_secondary_muscle_half_set_weighting(self):
        """Primary muscle gets 1.0 set credit, secondary muscle gets 0.5 set credit."""
        workouts = [
            {
                "id": "w1",
                "start_time": (self.now - timedelta(hours=10)).isoformat(),
                "exercises": [
                    {
                        "exercise_template_id": "mock-bench",
                        "title": "Flat Bench Press",
                        "sets": [
                            {"set_type": "normal", "weight_kg": 80, "reps": 10},
                            {"set_type": "normal", "weight_kg": 80, "reps": 10},
                            {"set_type": "normal", "weight_kg": 80, "reps": 10}
                        ]
                    }
                ]
            }
        ]
        goals = {"Chest": 10, "Triceps": 10}
        res = analyze_workouts(workouts, weekly_goals=goals, current_time=self.now)
        muscles = {m["name"]: m for m in res["muscles"]}
        self.assertEqual(muscles["Chest"]["sets_7d"], 3)
        self.assertEqual(muscles["Triceps"]["sets_7d"], 1.5)
        self.assertEqual(muscles["Chest"]["deficit_7d"], 7)
        self.assertEqual(muscles["Triceps"]["deficit_7d"], 8.5)
        self.assertEqual(muscles["Triceps"]["recovery_status"], "resting")

    def test_json_serializability(self):
        """Verify the output can be directly serialized to JSON with no datetime errors."""
        res = analyze_workouts([], weekly_goals=self.goals, current_time=self.now)
        dumped = json.dumps(res)
        self.assertIsInstance(dumped, str)

if __name__ == "__main__":
    unittest.main()
