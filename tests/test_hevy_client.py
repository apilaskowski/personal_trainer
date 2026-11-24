import unittest
from src.config import DEFAULT_WEEKLY_GOALS, RECOVERY_THRESHOLD_HOURS
from src.hevy_client import (
    get_workouts,
    normalize_hevy_muscle,
    resolve_exercise_muscles,
    load_templates_cache
)
from tests.mock_data import generate_mock_workouts

class TestConfig(unittest.TestCase):
    def test_weekly_goals_exist(self):
        self.assertIn("Chest", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Lats", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Upper / Mid Back", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Quads", DEFAULT_WEEKLY_GOALS)
        self.assertIn("Hamstrings", DEFAULT_WEEKLY_GOALS)
        self.assertEqual(RECOVERY_THRESHOLD_HOURS, 48.0)

class TestHevyClientAndTemplates(unittest.TestCase):
    def test_normalize_hevy_muscle(self):
        """Verifies Hevy raw API muscle strings normalize to our standard groups."""
        self.assertEqual(normalize_hevy_muscle("quadriceps"), "Quads")
        self.assertEqual(normalize_hevy_muscle("quads"), "Quads")
        self.assertEqual(normalize_hevy_muscle("lats"), "Lats")
        self.assertEqual(normalize_hevy_muscle("upper_back"), "Upper / Mid Back")
        self.assertEqual(normalize_hevy_muscle("adductors"), "Hip Adductors")
        self.assertEqual(normalize_hevy_muscle("abductors"), "Hip Abductors")
        self.assertEqual(normalize_hevy_muscle("abdominals"), "Abs / Core")
        self.assertEqual(normalize_hevy_muscle("shoulders"), "Shoulders")
        self.assertIsNone(normalize_hevy_muscle("unknown_muscle"))

    def test_load_templates_cache(self):
        """Verifies that templates cache loads from disk."""
        cache = load_templates_cache()
        self.assertIsInstance(cache, dict)
        self.assertIn("mock-wall-sit", cache)
        self.assertEqual(cache["mock-wall-sit"]["muscles"], ["Quads"])

    def test_resolve_exercise_muscles_from_cache(self):
        """Verifies that templates in cache resolve directly with primary (1.0) and secondary (0.5) weights."""
        self.assertEqual(resolve_exercise_muscles("Wall Sit", template_id="mock-wall-sit"), {"Quads": 1.0})
        self.assertEqual(resolve_exercise_muscles("Barbell Squat", template_id="mock-squat"), {"Quads": 1.0, "Glutes": 0.5})
        self.assertEqual(resolve_exercise_muscles("Flat Bench Press", template_id="mock-bench"), {"Chest": 1.0, "Triceps": 0.5})

    def test_resolve_exercise_muscles_by_title_fallback(self):
        """When template_id is missing, falls back to matching known titles in cache."""
        self.assertEqual(resolve_exercise_muscles("Wall Sit", template_id=None), {"Quads": 1.0})
        self.assertEqual(resolve_exercise_muscles("Nonexistent Exercise", template_id=None), {})

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
                self.assertIn("exercise_template_id", ex)
                self.assertIn("sets", ex)

    def test_get_workouts_requires_api_key(self):
        """get_workouts must fail fast if HEVY_API_KEY is missing, preventing silent mock fallbacks in production."""
        with self.assertRaises(ValueError):
            get_workouts(api_key=None)

if __name__ == "__main__":
    unittest.main()
