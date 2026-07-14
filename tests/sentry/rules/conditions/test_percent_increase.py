import math

import pytest

from sentry.rules.conditions.event_frequency import percent_increase


@pytest.mark.parametrize(
    ("current", "comparison", "expected"),
    [
        (0, 0, 0.0),
        (0, -1, 0.0),
        (100, 100, 0.0),
        (50, 100, 0.0),
        (110, 100, 10.0),
        (110.5, 100, 10.5),
        (200, 100, 100.0),
    ],
)
def test_percent_increase(
    current: int | float,
    comparison: int | float,
    expected: float,
) -> None:
    assert percent_increase(current, comparison) == expected


@pytest.mark.parametrize(
    ("current", "comparison"),
    [
        (1, 0),
        (10, 0),
        (1, -1),
    ],
)
def test_percent_increase_from_non_positive_baseline_is_infinite(
    current: int | float,
    comparison: int | float,
) -> None:
    assert math.isinf(percent_increase(current, comparison))


def test_percent_increase_preserves_fractional_precision() -> None:
    assert percent_increase(110.1, 100) > 10


def test_percent_increase_exact_threshold_is_not_greater() -> None:
    assert not percent_increase(110, 100) > 10
