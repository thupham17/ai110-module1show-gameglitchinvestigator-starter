"""Exercise actual Streamlit reruns, inputs, and complete game rounds."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def new_app():
    app = AppTest.from_file(str(APP)).run()
    app.session_state["secret"] = 10
    return app


def submit(app, guess):
    app.text_input[0].set_value(str(guess))
    app.button[1].click().run()
    assert not app.exception
    return app


def test_correct_hints_and_stable_secret():
    app = new_app()
    submit(app, 15)
    assert app.warning[0].value == "📉 Go LOWER!"
    submit(app, 5)
    assert app.warning[0].value == "📈 Go HIGHER!"
    assert app.session_state["secret"] == 10
    assert "Attempts left: 6" in app.info[0].value


@pytest.mark.parametrize("raw", ["", "words", "3.9", "-5", "0", "101"])
def test_invalid_input_preserves_round(raw):
    app = new_app()
    submit(app, raw)
    assert len(app.error) == 1
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert app.session_state["secret"] == 10


def test_full_attempt_budget_then_restart_after_loss():
    app = new_app()
    for attempt in range(1, 9):
        submit(app, 15)
        assert f"Attempts left: {8 - attempt}" in app.info[0].value
        assert app.session_state["status"] == (
            "lost" if attempt == 8 else "playing"
        )
    assert "Out of attempts!" in app.error[0].value
    assert app.button[1].disabled
    app.button[0].click().run()
    assert not app.exception
    assert app.session_state["status"] == "playing"
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert not app.button[1].disabled


def test_win_restart_and_best_score_persistence():
    app = new_app()
    submit(app, 10)
    assert app.session_state["status"] == "won"
    assert app.session_state["score"] == 100
    assert app.session_state["high_score"] == 100
    assert "Correct!" in app.success[0].value
    assert app.button[1].disabled
    app.button[0].click().run()
    assert app.session_state["status"] == "playing"
    assert app.session_state["high_score"] == 100
    app.session_state["secret"] = 10
    submit(app, 15)
    submit(app, 10)
    assert app.session_state["score"] == 85
    assert app.session_state["high_score"] == 100


@pytest.mark.parametrize("difficulty, high, limit", [("Easy", 20, 6), ("Hard", 50, 5)])
def test_difficulty_change_and_new_game_use_selected_range(difficulty, high, limit):
    app = new_app()
    submit(app, 15)
    app.selectbox[0].set_value(difficulty).run()
    assert not app.exception
    assert app.session_state["status"] == "playing"
    assert app.session_state["attempts"] == 0
    assert app.session_state["history"] == []
    assert 1 <= app.session_state["secret"] <= high
    assert f"between 1 and {high}. Attempts left: {limit}" in app.info[0].value
    submit(app, high + 1)
    assert app.session_state["attempts"] == 0
    app.button[0].click().run()
    assert 1 <= app.session_state["secret"] <= high


def test_hidden_hint_does_not_hide_win():
    app = new_app()
    app.checkbox[0].uncheck().run()
    submit(app, 15)
    assert not app.warning
    submit(app, 10)
    assert "Correct!" in app.success[0].value


def test_win_on_final_allowed_guess():
    app = new_app()
    for _ in range(7):
        submit(app, 15)
    submit(app, 10)
    assert app.session_state["status"] == "won"
    assert not app.error
    assert "Attempts left: 0" in app.info[0].value
