import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from learning_plan_check import validate_plan, validate_stage


def stage(purpose: str, course_file: str, minutes: int = 20) -> dict[str, object]:
    return {
        "purpose": purpose,
        "course_file": course_file,
        "action": "Run one named check.",
        "expected_result": "A visible result appears.",
        "stop_condition": "Stop if the named result does not appear.",
        "minutes": minutes,
    }


class LearningPlanCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.course_root = Path(self.temp.name)
        for name in ("data.md", "baseline.md", "candidate.md", "errors.md", "finish.md"):
            (self.course_root / name).write_text("course step", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def valid_plan(self) -> dict[str, object]:
        return {
            "day": "Day 1",
            "stages": [
                stage("data: verify the real file", "data.md", 25),
                stage("baseline: establish a comparison", "baseline.md", 30),
                stage("candidate: complete one model", "candidate.md", 45),
                stage("errors: inspect held-out mistakes", "errors.md", 35),
                stage("finish: check evidence", "finish.md", 20),
            ],
        }

    def test_valid_stage_has_no_errors(self):
        errors = validate_stage(
            stage("data: verify", "data.md"), self.course_root, 1
        )
        self.assertEqual(errors, [])

    def test_missing_field_and_file_are_reported(self):
        item = stage("data: verify", "missing.md")
        item.pop("expected_result")
        errors = validate_stage(item, self.course_root, 2)
        self.assertTrue(any("expected_result" in error for error in errors))
        self.assertTrue(any("missing.md" in error for error in errors))

    def test_non_positive_minutes_are_reported(self):
        errors = validate_stage(
            stage("data: verify", "data.md", 0), self.course_root, 1
        )
        self.assertTrue(any("positive whole number" in error for error in errors))

    def test_complete_plan_passes(self):
        self.assertEqual(validate_plan(self.valid_plan(), self.course_root), [])

    def test_long_plan_and_missing_purpose_are_reported(self):
        plan = self.valid_plan()
        plan["stages"][0]["minutes"] = 100
        plan["stages"][2]["purpose"] = "train one stronger model"
        errors = validate_plan(plan, self.course_root)
        self.assertTrue(any("180" in error for error in errors))
        self.assertTrue(any("candidate" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
