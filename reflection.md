# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first time I ran it, the game looked like a simple number guessing game with a difficulty selector, a guess input, and buttons to submit a guess or start a new game. The hints were backwards because the messages in `check_guess` contradicted the comparison: a high guess told me to go higher. The attempt count was wrong because it started at 1 and was displayed before the next increment, so Normal mode ended after seven guesses while showing one attempt left. Decimal input such as `3.9` was converted to `3` by `int(float(raw))`, and New Game did not reset the completed status, score, or history. Codex reproduced these issues in the actual starter UI using Streamlit AppTest, with the secret set to 50 for repeatability; the trace is saved in `evidence/starter-session.txt`.

**Bug Reproduction Log**

| Input / trigger | Expected behavior | Actual starter behavior | Cause / evidence |
|---|---|---|---|
| Secret 50; submit 60 | Tell me to guess lower. | “📈 Go HIGHER!” | Reversed message in `check_guess`; recorded AppTest session. |
| Submit seven guesses in Normal mode | One valid guess should remain; eight total are allowed. | Game over appears while the display still shows one attempt left. | Counter starts at 1 and the display precedes the increment; recorded session. |
| Submit `3.9` | Reject a decimal without spending an attempt. | History records `3` and the attempt is consumed. | `int(float(raw))` truncates input; recorded session. |
| Click New Game after losing | Reset to a playable round with zero attempts, zero score, and empty history. | Status stays `lost`, and the game tells me to start a new game again. | Reset omits status, score, and history; recorded session. |
| Submit text such as `hello` | Show an error without spending an attempt. | Attempt count increases before parsing fails. | Validation happens after incrementing the counter. |
| Switch to Easy, then start a new game | Secret and displayed range should both be 1–20. | Reset draws from 1–100, and the prompt always says 1–100. | Hard-coded range and missing difficulty reset in `app.py`. |
| Submit a high wrong guess on an even attempt | Lose five points just as for a low wrong guess. | Gain five points. | Parity-dependent branch in `update_score`. |

The reproduction trace and verified post-fix browser walkthrough are included in the README.

## 2. How did you use AI as a teammate?

I used ChatGPT Codex to clone the project, troubleshoot localhost, explain bugs, implement repairs, and verify the results under my request to complete the work. Codex explained that starting attempts at 1 and rendering the count before incrementing caused the early game-over and stale display; I accepted resetting the count to 0 and updating state before rendering because the full-round test then allowed exactly eight guesses. We revised Codex's original setup suggestion, `pip install -r requirements.txt`, after the old pip tried building pandas from source: Codex upgraded pip and installed prebuilt dependencies, then verified the running server's health check. When Codex offered a choice between preserving the starter's outcome-and-message tuple and returning a simple outcome string, I chose the string because it kept the logic simple and preserved the existing tests, revising the AI-generated starter interface. The setup revision was carried out by Codex during delegated troubleshooting, and the interface choice was my direct response; I did not independently reject a separate debugging chat answer.

## 3. Debugging and testing your fixes

I checked fixes by repeating the original failure inputs and comparing the results with the expected behavior, rather than relying only on the code looking correct. The original three tests failed with `NotImplementedError`; after Codex completed `logic_utils.py` and added regression coverage, `python -m pytest -q` reported 38 passing tests. The Streamlit tests verified that invalid inputs leave the secret, attempts, score, and history unchanged, and that Normal mode permits exactly eight valid guesses with zero left at game over. Those tests also caught a new issue where the submit button stayed enabled immediately after a win or loss, which Codex fixed by rerunning after processing a valid guess. In the browser, Codex verified that guessing 50 against a secret of 37 produced “Go LOWER!”, then guessing 37 won with 85 points; the screenshot and trace are saved in `evidence/`.

## 4. What did you learn about Streamlit and state?

Streamlit reruns a Python script from top to bottom when a user interacts with a widget, while a form groups inputs until submission. Session state is like a notebook that remembers the current player's secret, attempts, score, and history across those runs. This starter already stored the secret in session state, so its actual bugs were incomplete resets, inconsistent difficulty handling, and when counters were updated and displayed. The repaired app initializes the secret once per round, uses callbacks to reset a round, and reruns after a valid submission so the screen reflects the new state immediately. The best score is kept separately so it survives a new round within the same browser session.

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing a reproduction log with the exact input, expected behavior, and actual result before changing code. I also want to test both pure functions and the UI, because a correct comparison function does not prove that attempt counters or restart buttons work. Next time, I would ask AI for small changes with clear verification steps and record accepted or revised suggestions as they happen. This project showed me that AI-generated code and descriptions can be convincing while still containing mistakes: even the starter README's claim that the secret changed on every submit did not match this version's implementation. I need to compare AI advice with observed behavior and test results before treating it as correct.
