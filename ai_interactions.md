# AI Interactions Log

Tool used: ChatGPT Codex. Changes were delegated within this chat; no separate
subagents or second AI model were used.

## Agent Workflow — Session Best Score

**User task:** “ok complete the rest of the work”, following a rubric review of
missing implementation, tests, documentation, and Git history.

**Agent design:** Codex added a best winning score for the current session as a
small meaningful feature. It is updated only on a win, survives New Game and
difficulty resets, and does not persist across independent browser sessions.

**Files modified:** `app.py`, `logic_utils.py`, `tests/test_app.py`,
`tests/test_edge_cases.py`, `requirements.txt`, `README.md`, `reflection.md`,
`ai_interactions.md`, and evidence files.

**What Codex completed:** extracted pure rules, repaired hints and input handling,
corrected counting/scoring, reset full round state, implemented the best-score
metric, added a progress bar and structured history, tested the app, and documented
an actual browser win.

**Verification and corrections:** the first expanded test run had 36 passes and
two failures because Submit remained enabled just after a completed round. Codex
added `st.rerun()` after a valid submission; all 38 tests then passed. The best-score
test wins with 100 points, restarts, wins again with 85 points, and verifies the
best remains 100. No manual code correction by the student is claimed.

**Student choice:** Codex asked whether to return a simple outcome string or keep
outcome and hint together; the user answered, “Accept it: keep the logic simple and
preserve the existing tests.” The original three tests remain unchanged.

## Test Generation — Advanced Edge Cases

**Prompt/context:** the same user request, “ok complete the rest of the work”,
followed a rubric review identifying failing tests and the optional edge-case
coverage. Codex selected the test cases below based on observed starter bugs.
There was no separate student-written test-generation prompt.

| Case | Generated coverage | Why it matters | Result |
|---|---|---|---|
| Empty input and whitespace | Parser rejects `None`, empty, and spaces; UI leaves round state unchanged. | An accidental blank submission should not waste an attempt. | Pass |
| Decimals, scientific notation, and nonnumeric strings | Reject `3.9`, `50.0`, `NaN`, `1e2`, and text. | Avoid silent truncation and ambiguous number formats. | Pass |
| Signed integers and out-of-range values | Parser preserves signed integers; UI rejects `-5`, `0`, and `101` in Normal mode. | Separate valid integer syntax from the difficulty's allowed range. | Pass |
| Final-attempt win | Seven wrong guesses followed by the correct eighth guess wins. | Win handling must take precedence over exhaustion. | Pass |
| Restart after loss/win | Clear attempts, score, status, and history; preserve best score. | Prevent the starter's stuck completed state. | Pass |
| Difficulty switch | Use Easy/Hard range and attempt budget immediately and after reset. | Secret, validation, prompt, and reset must agree. | Pass |

Final output is in the README and `evidence/pytest-results.txt`. The suite includes
the original outcome tests, pure-function edge cases, and Streamlit AppTest
integration tests. Test secrets are controlled for repeatability; the browser
demonstration used the actual random secret shown in Developer Debug Info.

## Scope

Enhanced UI was implemented and described in the README. Pure functions have
expanded docstrings, but the professional linting stretch criterion was not
attempted. No second-model comparison or invented interaction is recorded.
