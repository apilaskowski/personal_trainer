import unittest
from src.config import map_exercise_to_muscles, DEFAULT_WEEKLY_GOALS, RECOVERY_THRESHOLD_HOURS
from src.hevy_client import get_workouts, generate_mock_workouts

class TestConfigAndMapping(unittest.TestCase):
    def test_weekly_goals_exist(self):
        self.assertIn("Chest", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Back", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Quads", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Hamstrings", DEFAULT_WEEKLY_GOALS)
        self.assertEqual(RECOVERY_THRESHOLD_HOURS, 48.0)

    def test_exercise_mapping_exact(self):
        self.assertEqual(map_exercise_to_muscles("Flat Bench Press"), ["Chest", "Triceps"])
        self.assertEqual(map_exercise_to_muscles("Lat Pulldown"), ["Back", "Biceps"])
        self.assertEqual(map_exercise_to_muscles("Barbell Squat"), ["Quads", "Glutes"])
        self.assertEqual(map_exercise_to_muscles("Lying Leg Curl"), ["Hamstrings"])
        self.assertEqual(map_exercise_to_muscles("Overhead Press"), ["Shoulders", "Triceps"])

    def test_exercise_mapping_fallback(self):
        self.assertIn("Quads", map_exercise_to_muscles("Unknown Machine Squat"))
        self.assertIn("Biceps", map_exercise_to_muscles("Special Heavy Curl"))
        self.assertIn("Other", map_exercise_to_muscles("Random Exercise 123"))

class TestHevyClient(unittest.TestCase):
    def test_mock_workouts_structure(self):
        workouts = generate_mock_workouts()
        self.assertGreaterEqual(len(workouts), 2)
        for w in workouts:
            self.assertIn("id", w)
            self.assertIn("title", w)
            self.assertIn("start_time", w)
            self.assertIn("exercises", w)
            for ex in w["exercises"]:
                self.assertIn("title", ex)
                self.assertIn("sets", ex)

    def test_get_workouts_offline_fallback(self):
        # Without API key, should return mock workouts safely
        workouts = get_workouts(api_key=None)
        self.assertIsInstance(workouts, list)
        self.assertGreater(len(workouts), 0)

if __name__ == "__main__":
    unittest.main()
