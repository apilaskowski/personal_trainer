import unittest
from src.config import map_exercise_to_muscles, DEFAULT_WEEKLY_GOALS, RECOVERY_THRESHOLD_HOURS
from src.hevy_client import (
    get_workouts,
    generate_mock_workouts,
    normalize_hevy_muscle,
    resolve_exercise_muscles,
    load_templates_cache
)

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

    def test_wall_sit_mapping(self):
        """Verifies that Wall Sit and Walk Sit correctly map to Quads."""
        self.assertEqual(map_exercise_to_muscles("Wall Sit"), ["Quads"])
        self.assertEqual(map_exercise_to_muscles("Walk Sit"), ["Quads"])

    def test_exercise_mapping_fallback(self):
        self.assertIn("Quads", map_exercise_to_muscles("Unknown Machine Squat"))
        self.assertIn("Biceps", map_exercise_to_muscles("Special Heavy Curl"))
        self.assertIn("Other", map_exercise_to_muscles("Random Exercise 123"))

class TestHevyClient(unittest.TestCase):
    def test_normalize_hevy_muscle(self):
        self.assertEqual(normalize_hevy_muscle("quadriceps"), "Quads")
        self.assertEqual(normalize_hevy_muscle("quads"), "Quads")
        self.assertEqual(normalize_hevy_muscle("lats"), "Back")
        self.assertEqual(normalize_hevy_muscle("upper_back"), "Back")
        self.assertEqual(normalize_hevy_muscle("abdominals"), "Abs")
        self.assertIsNone(normalize_hevy_muscle("unknown_muscle"))

    def test_load_templates_cache(self):
        cache = load_templates_cache()
        self.assertIsInstance(cache, dict)
        self.assertIn("mock-wall-sit", cache)
        self.assertEqual(cache["mock-wall-sit"]["muscles"], ["Quads"])

    def test_resolve_exercise_muscles(self):
        # 1. From template cache
        muscles = resolve_exercise_muscles("Any Name", template_id="mock-wall-sit")
        self.assertEqual(muscles, ["Quads"])

        # 2. From fallback title mapping
        muscles_title = resolve_exercise_muscles("Wall Sit", template_id=None)
        self.assertEqual(muscles_title, ["Quads"])

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
        workouts = get_workouts(api_key=None)
        self.assertIsInstance(workouts, list)
        self.assertGreater(len(workouts), 0)

if __name__ == "__main__":
    unittest.main()
