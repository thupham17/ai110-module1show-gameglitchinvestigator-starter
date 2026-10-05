"""Validate parsing boundaries and scoring rules without running the UI."""

import pytest

from logic_utils import get_range_for_difficulty, parse_guess, update_score


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_empty_input(raw):
    assert parse_guess(raw) == (False, None, "Enter a guess.")


@pytest.mark.parametrize("raw", ["hello", "3.9", "50.0", "NaN", "1e2"])
def test_invalid_whole_number(raw):
    assert parse_guess(raw) == (False, None, "Enter a whole number.")


@pytest.mark.parametrize("raw, expected", [(" -5 ", -5), (" +20 ", 20), ("0", 0)])
def test_signed_and_whitespace_integers(raw, expected):
    assert parse_guess(raw) == (True, expected, None)


@pytest.mark.parametrize("difficulty, expected", [
    ("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 50)),
    ("unknown", (1, 100)),
])
def test_difficulty_range(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


@pytest.mark.parametrize("attempt, points", [(1, 100), (2, 90), (10, 10), (20, 10)])
def test_win_score(attempt, points):
    assert update_score(0, "Win", attempt) == points


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
def test_wrong_guess_always_costs_five(outcome):
    assert update_score(10, outcome, 2) == 5


def test_unknown_outcome_does_not_change_score():
    assert update_score(10, "invalid", 1) == 10
