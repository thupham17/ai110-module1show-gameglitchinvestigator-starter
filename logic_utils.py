"""Pure rules for the number guessing game, independent of Streamlit."""


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive range; unknown difficulties use Normal's range."""
    return {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 50)}.get(
        difficulty, (1, 100)
    )


def parse_guess(raw: str):
    """Parse a whole number, returning (valid, value, error).

    Whitespace and signed integers are accepted. Empty input, decimals, and
    nonnumeric text are rejected without rounding or truncation. Range checks
    belong to the caller because the selected difficulty determines the range.
    """
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."
    return True, value, None


def check_guess(guess: int, secret: int):
    """Return Win, Too High, or Too Low by comparing integer values."""
    if guess == secret:
        return "Win"
    return "Too High" if guess > secret else "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Award 100 on a first-try win, decreasing by 10 per try (minimum 10).

    Either incorrect outcome costs five points. An unknown outcome leaves the
    score unchanged. Attempt numbers are one-based counts of valid guesses.
    """
    if outcome == "Win":
        return current_score + max(10, 100 - 10 * (attempt_number - 1))
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
