"""Test the evaluation contract before connecting any model provider."""

import pytest

from fintune import Example, baseline, score, split


def test_negative_modal_takes_precedence() -> None:
    assert baseline("A firm must not erase its audit log.") == "prohibition"
    assert baseline("A firm must retain its audit log.") == "obligation"
    assert baseline("The agency published its annual report.") == "other"


def examples() -> list[Example]:
    return [
        {"id": "a", "family": "records", "text": "Retain the log.", "label": "obligation"},
        {"id": "b", "family": "records", "text": "A log is required.", "label": "obligation"},
    ]


def test_REQ_01_group_isolation() -> None:
    assert sorted(map(len, split(examples()).values())) == [0, 0, 2]


def test_REQ_02_validate_dataset() -> None:
    with pytest.raises(ValueError, match="Duplicate"):
        split(examples() * 2)


def test_REQ_03_metric_counts() -> None:
    result = score(examples(), {"a": "obligation", "b": "permission"})
    assert result["accuracy"] == 0.5
    assert result["macro_f1"] == pytest.approx((2 / 3) / 5)


def test_REQ_04_missing_predictions_are_errors() -> None:
    assert score(examples(), {"b": "unknown"})["accuracy"] == 0.0
