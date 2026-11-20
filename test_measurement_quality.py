import unittest
from measurement_quality import validate_phase

class TestQuality(unittest.TestCase):
    def test_release_screen(self):
        result = validate_phase({"Knee": 35, "Elbow": 172, "Trunk": 22}, "Release")
        self.assertIsNone(result["Knee"])
        self.assertEqual(result["Elbow"], 172)
    def test_outside_reference_retained(self):
        result = validate_phase({"Knee": 110}, "Release")
        self.assertEqual(result["Knee"], 110)
        self.assertIn("Outside", result["Knee quality"])
    def test_back_knee_bfc(self):
        result = validate_phase({"Knee": 60, "Back Knee": 150}, "BFC")
        self.assertEqual(result["Knee"], 60)
        self.assertIn("Within", result["Back Knee quality"])
    def test_nonfinite(self):
        self.assertIsNone(validate_phase({"Trunk": float("nan")}, "FFC")["Trunk"])
    def test_idempotent_reason(self):
        row = validate_phase({"Knee": 45}, "FFC")
        self.assertEqual(validate_phase(row, "FFC")["Knee quality"], row["Knee quality"])

if __name__ == "__main__":
    unittest.main()
