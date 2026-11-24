"""Unit tests for the site build pipeline and data.json generation."""

import unittest
from unittest.mock import patch
import os
import json
from src.build_site import build
from tests.mock_data import generate_mock_workouts

class TestBuildSite(unittest.TestCase):
    @patch("src.build_site.get_workouts")
    def test_build_generates_valid_json(self, mock_get_workouts):
        """Verifies that build() outputs a valid public/data.json file with required schema."""
        mock_get_workouts.return_value = generate_mock_workouts()

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
