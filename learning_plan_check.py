"""Validate that an agent-created class plan connects to the real course."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_STAGE_FIELDS = (
    "purpose",
    "course_file",
    "action",
    "expected_result",
    "stop_condition",
    "minutes",
)
REQUIRED_PURPOSE_WORDS = ("data", "baseline", "candidate", "errors", "finish")


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_positive_whole_number(value: object) -> bool:
    # bool is an int subclass, so reject it explicitly.
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _course_file_error(course_file: object, course_root: Path) -> str | None:
    if not _is_non_empty_string(course_file):
        return None  # The missing/empty-field check already reports this.
    candidate = Path(course_file)
    if not candidate.is_absolute():
        candidate = course_root / candidate
    resolved = candidate.resolve()
    try:
        below_root = resolved.is_relative_to(course_root.resolve())
    except ValueError:
        below_root = False
    if resolved.is_file() and below_root:
        return None
    return f"course_file does not exist below course root: {course_file}"


def validate_stage(stage: object, course_root: Path, number: int) -> list[str]:
    """Return clear problems found in one stage."""
    errors: list[str] = []
    if not isinstance(stage, dict):
        return [f"stage {number} must be a dictionary, got {type(stage).__name__}"]
    for field in REQUIRED_STAGE_FIELDS:
        if field not in stage:
            errors.append(f"stage {number} missing required field: {field}")
            continue
        value = stage[field]
        if isinstance(value, str) and not value.strip():
            errors.append(f"stage {number} has an empty required field: {field}")
        elif value is None:
            errors.append(f"stage {number} has an empty required field: {field}")
    if "minutes" in stage and not _is_positive_whole_number(stage["minutes"]):
        errors.append(
            f"stage {number} minutes must be a positive whole number, "
            f"got {stage['minutes']!r}"
        )
    if "course_file" in stage:
        file_error = _course_file_error(stage["course_file"], course_root)
        if file_error:
            errors.append(f"stage {number} {file_error}")
    return errors


def validate_plan(plan: object, course_root: Path) -> list[str]:
    """Return all structural and course-connection problems in one plan."""
    errors: list[str] = []
    if not isinstance(plan, dict):
        errors.append("plan must be a dictionary")
        return errors
    if not _is_non_empty_string(plan.get("day")):
        errors.append("plan day must be a non-empty string")
    stages = plan.get("stages")
    if not isinstance(stages, list):
        errors.append("plan stages must be a list")
        return errors
    if len(stages) < 5:
        errors.append(f"plan requires at least 5 stages, got {len(stages)}")
    for number, stage in enumerate(stages, start=1):
        errors.extend(validate_stage(stage, course_root, number))

    total_minutes: int | None = None
    try:
        total_minutes = sum(
            int(stage["minutes"])
            for stage in stages
            if isinstance(stage, dict) and "minutes" in stage
        )
    except (TypeError, ValueError, KeyError):
        total_minutes = None
    if total_minutes is not None and total_minutes > 180:
        errors.append(f"total minutes must be 180 or less, got {total_minutes}")

    purposes = [
        stage.get("purpose", "")
        for stage in stages
        if isinstance(stage, dict)
    ]
    for word in REQUIRED_PURPOSE_WORDS:
        if not any(isinstance(text, str) and word in text for text in purposes):
            errors.append(f"no stage purpose mentions required word: {word}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a course learning plan")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--course-root", required=True, type=Path)
    args = parser.parse_args()

    if not args.plan.is_file():
        raise FileNotFoundError(f"Plan file not found: {args.plan}")
    if not args.course_root.is_dir():
        raise FileNotFoundError(f"Course root not found: {args.course_root}")

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    errors = validate_plan(plan, args.course_root.resolve())
    if errors:
        print("LEARNING PLAN CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LEARNING PLAN CHECK PASSED")
    print(f"Day: {plan['day']}")
    print(f"Stages: {len(plan['stages'])}")
    print(f"Total minutes: {sum(stage['minutes'] for stage in plan['stages'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
