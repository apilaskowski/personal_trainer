"""Unit tests for the site build pipeline and data.json generation."""

import unittest
import os
import json
from src.build_site import build

class TestBuildSite(unittest.TestCase):
    def test_build_generates_valid_json(self):
        """Verifies that build() outputs a valid public/data.json file with required schema."""
        output_path = build()
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate schema keys
        self.assertIn("generated_at", data)
        self.assertIn("today_recommendation", data)
        self.assertIn("muscles", data)
        self.assertIn("recent_workouts", data)

        # Validate today's recommendation structure
        rec = data["today_recommendation"]
        self.assertIn("focus_muscles", rec)
        self.assertIn("headline", rec)
        self.assertIn("summary", rec)
        self.assertIsInstance(rec["focus_muscles"], list)

        # Validate muscles list (10 muscle groups)
        self.assertEqual(len(data["muscles"]), 10)
        for m in data["muscles"]:
            self.assertIn("name", m)
            self.assertIn("recovery_status", m)
            self.assertIn("sets_7d", m)
            self.assertIn("deficit_7d", m)

if __name__ == "__main__":
    unittest.main()
