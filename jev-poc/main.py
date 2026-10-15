#!/usr/bin/env python3
"""Minimal support-ticket classification POC using the Jev Model API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://jevmodel.net/v1/systemone"
MODEL = "jev-latest"
CONFIDENCE_THRESHOLD = 0.65
CATEGORIES = {
    "billing": "Payments, invoices, charges, refunds, and subscriptions.",
    "technical": "Product bugs, outages, errors, and integrations.",
    "account": "Sign-in, password, profile, and account access issues.",
    "other": "Requests that do not fit any of the other categories.",
}


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE entries without overriding existing environment variables."""
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def make_payload(message: str) -> dict[str, Any]:
    return {
        "model": MODEL,
        "state": {"message": message},
        "questions": {
            "category": {
                "type": "choice",
                "instructions": "Which team should handle this support ticket?",
                "criteria": CATEGORIES,
            }
        },
    }


def classify(message: str, api_key: str, timeout: int = 30) -> dict[str, Any]:
    request = Request(
        API_URL,
        data=json.dumps(make_payload(message)).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Jev API returned HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach the Jev API: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("Jev API returned invalid JSON") from exc

    try:
        return body["answers"]["category"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError("Jev API response did not contain answers.category") from exc


def route_for(answer: dict[str, Any], threshold: float) -> str:
    confidence = answer.get("confidence", 0.0)
    category = answer.get("choice", "unknown")
    if category not in CATEGORIES or confidence < threshold:
        return "manual_review"
    return category


def print_result(label: str, answer: dict[str, Any], threshold: float) -> None:
    category = answer.get("choice", "unknown")
    confidence = answer.get("confidence", 0.0)
    print(f"{label}: category={category}, confidence={confidence:.3f}, route={route_for(answer, threshold)}")
    probabilities = answer.get("probabilities")
    if probabilities:
        print("  probabilities=" + json.dumps(probabilities, sort_keys=True))


def run_examples(path: Path, api_key: str, threshold: float) -> int:
    examples = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(examples, list) or not examples:
        raise ValueError("Examples file must contain a non-empty JSON array")

    correct = 0
    for example in examples:
        answer = classify(example["message"], api_key)
        actual = answer.get("choice", "unknown")
        expected = example["expected_category"]
        correct += actual == expected
        print_result(example.get("id", "example"), answer, threshold)
        print(f"  expected={expected}, match={actual == expected}")

    print(f"\nExact match: {correct}/{len(examples)} ({correct / len(examples):.0%})")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify a support ticket with Jev Model.")
    parser.add_argument("message", nargs="?", help="Ticket text to classify")
    parser.add_argument(
        "--examples",
        type=Path,
        help="Run the labeled examples in a JSON file instead of classifying one message",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=CONFIDENCE_THRESHOLD,
        help=f"Minimum confidence before routing automatically (default: {CONFIDENCE_THRESHOLD})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv()
    api_key = os.getenv("JEV_API_KEY")
    if not api_key:
        print("Set JEV_API_KEY in the environment or in a local .env file.", file=sys.stderr)
        return 2
    if not 0 <= args.threshold <= 1:
        print("--threshold must be between 0 and 1.", file=sys.stderr)
        return 2
    if not args.examples and not args.message:
        print("Provide a ticket message or pass --examples examples.json.", file=sys.stderr)
        return 2

    try:
        if args.examples:
            return run_examples(args.examples, api_key, args.threshold)
        answer = classify(args.message, api_key)
        print_result("ticket", answer, args.threshold)
        return 0
    except (OSError, json.JSONDecodeError, KeyError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
