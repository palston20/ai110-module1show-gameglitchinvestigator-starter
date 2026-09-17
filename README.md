# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- Describe the game's purpose.

 Game Glitch Investigator is a number guessing game built with Streamlit. The computer picks a secret number and you try to guess it, and after each guess the game tells you whether you need to go higher or lower. You pick a difficulty first — Easy is 1-20 with 6 attempts, Normal is 1-100 with 8, and Hard is 1-50 with 5 — and you earn points based on how fast you win, starting at 100 for a first-attempt win and dropping 10 points for each extra guess.

- Detail which bugs you found.
1. The hints were backwards. Guessing 60 when the secret was 50 told me to "Go HIGHER!", which pushed me further from the answer every time. The messages themselves were just swapped in check_guess.

2. Numbers were being compared as text. On every even-numbered guess, app.py converted the secret to a string before comparing it. Python compares strings letter by letter, so "9" > "10" is true, and guessing 9 against a secret of 10 told me to go lower.

3. The scoring was copletely off.  A first-attempt win only paid 80 points. The formula was 100 - 10 * (attempt + 1) instead of (attempt - 1), so every win was shorted one attempt's worth of points. Wrong guesses could raise my score. update_score had a branch that added 5 points for a "Too High" guess on even attempts, which makes no sense — being wrong should never help you.

4. The difficulty didn't change the secret number. The app always booted on Normal and rolled the secret once, so switching to Easy left me hunting a number that could be anywhere in 1-100 even though the screen promised 1-20. "New Game" had the same problem because it hardcoded random.randint(1, 100).


- Explain what fixes you applied.

For the hint bug I swapped the two messages back so "Too High" says Go LOWER and "Too Low" says Go HIGHER. For the string comparison, I deleted the TypeError fallback that was doing str(guess) and made check_guess convert both values to int before comparing, then removed the code in app.py that was turning the secret into a string in the first place. I fixed the scoring formula to 100 - 10 * (attempt - 1) and deleted the branch that gave points for a wrong guess. For the range bug, I stored the difficulty in session state so changing it starts a fresh round, and pointed both the new-game button and the instructions at get_range_for_difficulty instead of hardcoding 1-100.

I also moved check_guess, parse_guess, update_score, and get_range_for_difficulty into logic_utils.py. This mattered more than I expected — app.py runs Streamlit the moment it's imported, so pytest couldn't import those functions to test them while they were still in there. After the move I got all 43 tests passing, and I double-checked the tests were actually doing something by pasting the old broken code back in and confirming 26 of them failed.


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!--The player starts the game and makes their first guess. -->
2. <!-- The program lets them know whether their guess is above or below the secret number.  -->
3. <!-- The program lets them know whether their guess is above or below the secret number. ("Go Higher!" or "Go Lower!") -->
4. <!-- The user's score will update after each guess. -->
5. <!-- The game ends, either when the user runs out of guesses or they guess the correct number, and displays the user's final score.  -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
tests/test_game_logic.py ...........................................                               [100%]

=========================================== 43 passed in 0.05s ===========================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
