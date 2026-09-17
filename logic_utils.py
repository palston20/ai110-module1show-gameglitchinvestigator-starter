def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


HINTS = {
    "Win": "🎉 Correct!",
    # FIXME: these two were swapped. "Too High" told the player to go HIGHER,
    # which walked them further away from the secret on every hint.
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIXME: the old version fell back to comparing str(guess) against the
    # secret whenever the two weren't the same type. String comparison is
    # lexicographic, so "9" > "10" and the high/low hint came out backwards.
    # Fixed by coercing both sides to int before comparing.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_for(outcome: str):
    """Return the player-facing hint message for an outcome."""
    return HINTS.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIXME: this was 100 - 10 * (attempt_number + 1), so a win on the
        # first attempt paid 80 instead of 100 and every win was one step
        # under-paid. Win on attempt 1 is worth 100, each extra attempt -10.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIXME: "Too High" used to ADD 5 on even-numbered attempts, so a wrong
    # guess could raise your score. A wrong guess always costs 5 now.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
