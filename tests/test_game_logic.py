"""
Regression tests for the Game Glitch Investigator.

Each test below targets one specific bug that was found and fixed. The comment
on each test describes what the buggy version did, so that if the bug ever
comes back the failure message points straight at it.
"""

import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    hint_for,
    parse_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# Baseline behavior (these passed before and must keep passing)
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ---------------------------------------------------------------------------
# BUG 1: hint messages were swapped
# "Too High" told the player to go HIGHER and "Too Low" told them to go LOWER,
# so following the hint walked you away from the secret every time.
# ---------------------------------------------------------------------------

def test_too_high_tells_player_to_go_lower():
    assert "LOWER" in hint_for("Too High")
    assert "HIGHER" not in hint_for("Too High")


def test_too_low_tells_player_to_go_higher():
    assert "HIGHER" in hint_for("Too Low")
    assert "LOWER" not in hint_for("Too Low")


def test_win_message_does_not_give_a_direction():
    message = hint_for("Win")
    assert "HIGHER" not in message
    assert "LOWER" not in message


# ---------------------------------------------------------------------------
# BUG 2: guess and secret were compared as strings
# check_guess had a TypeError fallback that compared str(guess) to the secret.
# String comparison is lexicographic, so "9" > "10" and the hint was inverted
# for any pair where the shorter number has the larger leading digit.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("guess, secret, expected", [
    (9, 10, "Too Low"),     # lexicographically "9" > "10" -> old code said Too High
    (9, 100, "Too Low"),    # same trap with a 3-digit secret
    (5, 20, "Too Low"),
    (100, 99, "Too High"),  # lexicographically "100" < "99" -> old code said Too Low
    (20, 3, "Too High"),
])
def test_numbers_are_compared_numerically_not_lexicographically(guess, secret, expected):
    assert check_guess(guess, secret) == expected


@pytest.mark.parametrize("guess, secret, expected", [
    (9, "10", "Too Low"),
    (100, "99", "Too High"),
    (50, "50", "Win"),
])
def test_string_secret_still_compares_numerically(guess, secret, expected):
    # app.py used to pass str(secret) into check_guess on every even-numbered
    # attempt, which is what triggered the string-comparison path above.
    # A string secret must now give the same answer as an int one.
    assert check_guess(guess, secret) == expected


# ---------------------------------------------------------------------------
# BUG 3: win score was off by one attempt
# The formula was 100 - 10 * (attempt_number + 1), so winning on the first
# attempt paid 80 instead of the advertised 100.
# ---------------------------------------------------------------------------

def test_win_on_first_attempt_is_worth_full_100():
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 100


@pytest.mark.parametrize("attempt_number, expected_points", [
    (1, 100),
    (2, 90),
    (3, 80),
    (5, 60),
])
def test_each_extra_attempt_costs_ten_points(attempt_number, expected_points):
    assert update_score(0, "Win", attempt_number) == expected_points


def test_win_points_never_drop_below_ten():
    # The floor still applies, so a very late win is worth 10 and never 0 or
    # negative.
    assert update_score(0, "Win", 20) == 10
    assert update_score(0, "Win", 100) == 10


def test_win_adds_to_the_existing_score():
    assert update_score(current_score=45, outcome="Win", attempt_number=2) == 135


# ---------------------------------------------------------------------------
# BUG 4: "Too High" awarded points on even-numbered attempts
# update_score had `if attempt_number % 2 == 0: return current_score + 5`,
# so a wrong guess could raise your score.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4, 10])
def test_too_high_always_costs_five_points(attempt_number):
    # Attempt 2 and 4 are the ones the old code rewarded.
    assert update_score(100, "Too High", attempt_number) == 95


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4, 10])
def test_too_low_always_costs_five_points(attempt_number):
    assert update_score(100, "Too Low", attempt_number) == 95


def test_wrong_guesses_never_increase_the_score():
    score = 100
    for attempt_number in range(1, 7):
        new_score = update_score(score, "Too High", attempt_number)
        assert new_score < score
        score = new_score


# ---------------------------------------------------------------------------
# BUG 5: the guess range ignored the chosen difficulty
# The secret was rolled once per session and "New Game" hardcoded
# random.randint(1, 100), so on Easy you could be hunting a number outside the
# 1-20 range the UI promised. Both call sites now read this function.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("difficulty, expected", [
    ("Easy", (1, 20)),
    ("Normal", (1, 100)),
    ("Hard", (1, 50)),
])
def test_each_difficulty_has_its_own_range(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


def test_easy_range_is_not_the_normal_range():
    # The specific symptom: the app booted on Normal (1-100) and kept that
    # secret after switching to Easy.
    assert get_range_for_difficulty("Easy") != get_range_for_difficulty("Normal")


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)


# ---------------------------------------------------------------------------
# Supporting behavior: parse_guess feeds check_guess, so a guess that parses
# into the wrong type would resurrect the string-comparison bug.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw, expected_value", [
    ("42", 42),
    ("7.9", 7),
    ("  ", None),
])
def test_parse_guess_returns_an_int_or_an_error(raw, expected_value):
    ok, value, error = parse_guess(raw)
    if expected_value is None:
        assert not ok
        assert error
    else:
        assert ok
        assert isinstance(value, int)
        assert value == expected_value


@pytest.mark.parametrize("raw", [None, "", "abc"])
def test_parse_guess_rejects_non_numbers(raw):
    ok, value, error = parse_guess(raw)
    assert not ok
    assert value is None
    assert error
