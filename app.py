"""Streamlit interface for a stateful number guessing game."""

import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}
HINTS = {"Too High": "📉 Go LOWER!", "Too Low": "📈 Go HIGHER!"}


def reset_game():
    """Start a fresh round at the selected difficulty; preserve the best score."""
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    st.session_state.update(
        secret=random.randint(low, high),
        attempts=0,
        score=0,
        status="playing",
        history=[],
        last_outcome=None,
        guess_input="",
    )


st.set_page_config(page_title="Number Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number. Each valid guess counts as one attempt.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox(
    "Difficulty", list(ATTEMPT_LIMITS), index=1,
    key="difficulty", on_change=reset_game,
)
low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.sidebar.caption("Changing difficulty starts a fresh round.")
st.sidebar.caption("Win: 100 points minus 10 per extra try; wrong guess: −5.")

if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "secret" not in st.session_state:
    reset_game()

st.button("New Game 🔁", on_click=reset_game)
show_hint = st.checkbox("Show hint", value=True)
st.subheader("Make a guess")
with st.form("guess_form", clear_on_submit=True):
    raw_guess = st.text_input("Enter your guess:", key="guess_input")
    submit = st.form_submit_button(
        "Submit Guess 🚀", disabled=st.session_state.status != "playing"
    )

if submit and st.session_state.status == "playing":
    ok, guess, error = parse_guess(raw_guess)
    if not ok:
        st.error(error)
    elif not low <= guess <= high:
        st.error(f"Enter a whole number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        outcome = check_guess(guess, st.session_state.secret)
        st.session_state.last_outcome = outcome
        st.session_state.score = update_score(
            st.session_state.score, outcome, st.session_state.attempts
        )
        st.session_state.history.append({
            "Attempt": st.session_state.attempts,
            "Guess": guess,
            "Result": outcome,
            "Score": st.session_state.score,
        })
        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.high_score = max(
                st.session_state.high_score, st.session_state.score
            )
            st.balloons()
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
        st.rerun()

remaining = attempt_limit - st.session_state.attempts
st.info(f"Guess a number between {low} and {high}. Attempts left: {remaining}")
score_col, best_col = st.columns(2)
score_col.metric("Round score", st.session_state.score)
best_col.metric("Best winning score (this session)", st.session_state.high_score)
st.progress(st.session_state.attempts / attempt_limit)

if st.session_state.status == "won":
    st.success(
        f"🎉 Correct! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Start a new game to try again."
    )
elif show_hint and st.session_state.last_outcome in HINTS:
    st.warning(HINTS[st.session_state.last_outcome])

if st.session_state.history:
    st.subheader("Guess history")
    st.table(st.session_state.history)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Invalid guesses do not cost attempts or points. Best score resets on a new session.")
