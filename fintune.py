"""Freeze data splits and score regulatory obligation classifiers."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import TypedDict

LABELS = ("obligation", "prohibition", "permission", "definition", "other")


class Example(TypedDict):
    id: str
    family: str
    text: str
    label: str


def split(rows: list[Example], seed: int = 42) -> dict[str, list[Example]]:
    result: dict[str, list[Example]] = {"train": [], "validation": [], "test": []}
    seen: set[str] = set()
    for row in sorted(rows, key=lambda item: item["id"]):
        if row["id"] in seen or row["label"] not in LABELS or not row["family"].strip():
            raise ValueError("Duplicate ID, invalid label, or empty rule family")
        seen.add(row["id"])
        # Hash the group so a paraphrase from the same rule cannot leak across splits.
        key = f"{seed}:{row['family']}".encode()
        value = int(hashlib.sha256(key).hexdigest(), 16) % 100
        result["train" if value < 80 else "validation" if value < 90 else "test"].append(row)
    return result


def score(rows: list[Example], predictions: dict[str, str]) -> dict[str, object]:
    if not rows:
        raise ValueError("Cannot score an empty dataset")
    confusion = {label: dict.fromkeys((*LABELS, "invalid"), 0) for label in LABELS}
    for row in rows:
        predicted = predictions.get(row["id"])
        confusion[row["label"]][predicted if predicted in LABELS else "invalid"] += 1
    per_class = {}
    for label in LABELS:
        true_positive = confusion[label][label]
        denominator = sum(confusion[label].values()) + sum(row[label] for row in confusion.values())
        per_class[label] = 2 * true_positive / denominator if denominator else 0.0
    return {
        "accuracy": sum(confusion[label][label] for label in LABELS) / len(rows),
        "macro_f1": sum(per_class.values()) / len(LABELS),
        "per_class_f1": per_class,
        "confusion": confusion,
    }


def baseline(text: str) -> str:
    # Check negative obligations first because they also contain positive cue words.
    lower = text.casefold()
    for cue, label in [
        ("must not", "prohibition"),
        ("shall not", "prohibition"),
        ("must ", "obligation"),
        ("shall ", "obligation"),
        ("may ", "permission"),
        (" means ", "definition"),
    ]:
        if cue in lower:
            return label
    return "other"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["split", "baseline"])
    parser.add_argument("data", type=Path)
    args = parser.parse_args()
    rows: list[Example] = json.loads(args.data.read_text(encoding="utf-8"))
    partitions = split(rows)
    if args.mode == "baseline":
        result = score(rows, {row["id"]: baseline(row["text"]) for row in rows})
    else:
        canonical = json.dumps(partitions, sort_keys=True, separators=(",", ":")).encode()
        result = {"sha256": hashlib.sha256(canonical).hexdigest(), "partitions": partitions}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
