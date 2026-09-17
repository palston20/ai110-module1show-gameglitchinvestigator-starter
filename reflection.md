# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The game is a number guesser where you have to guess the number the computer is thinking. The game provides hints where it will let you know if the number you guessed is higher or lower than the secret number, and there are different difficulties you can play. Easy mode has a smaller range of 1-20 with 6 guesses, normal has 1-100 range with 8 guesses, and hard has 1-50 range with 4 guesses. 
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  - Bugs I noticed while playing the game were that the new game button doesn't 
    work, the secret number does not change based on the difficulty (so the number would be out of the expected range), and the higher/lower or the hint function is off. The new game button does not fully restart the game every single time, you would typically have to refresh the page. If you guessed a number, the program would tell you to go higher when the secret number is actually lower and vice versa. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

|    Input      |  Expected Behavior |   Actual Behavior |  Console Output / Error |
|---------------|------------------- |-----------------  |------------------------|
|guess is 60    |"Go lower!"         | "Go higher!"      | None
|game is over   |restart game    |page is stuck on previousgame |   None           |
| game is on easy|  secret is 1-20   | secret is 1-100   | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? 

I used Claude as an AI tool on this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude suggested that check_guess was giving the wrong hints because the fallback path was comparing the guess and secret as strings instead of numbers. The fix was to convert both values to integers before comparing them. I verified this by testing check_guess(9, 10), which now correctly returns "Too Low" instead of "Too High". I also reverted the code back to the buggy version and saw that 26 of my tests failed, confirming that the fix was working.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Claude first told me the high/low bug was caused only by the str(secret) conversion in app.py and implied that removing it finished the fix, but this was misleading. When I ran git diff, the original check_guess also had the two hint messages themselves swapped ("Too High" returned "📈 Go HIGHER!"), and update_score had separate bugs where a first-attempt win was 80 instead of 100 and a wrong "Too High" guess added 5 points on even attempts. I verified this by reading the actual diff against the committed version rather than trusting the summary, which showed at least four distinct bugs where Claude had described one. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I would make sure I could reproduce the bug first, then re-ran the same input after the fix and checked that the output actually changed. For the hint bug, that meant guessing a number I knew was below the secret and confirming the game said "Go HIGHER" instead of sending me the wrong way.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I ran python -m pytest tests/ and wrote a test asserting check_guess(9, 10) == "Too Low", which was the case that used to break because "9" > "10" is true when you compare them as strings. The bigger thing it showed me was when I pasted the old version back in and 26 of my 43 tests failed — that proved my tests were actually catching the bugs and not just passing no matter what.

- Did AI help you design or understand any tests? How?

Yes, Claude pointed out that update_score and get_range_for_difficulty were still sitting in app.py, and since app.py runs Streamlit as soon as it's imported, pytest couldn't import those functions to test them at all. Moving them into logic_utils.py was what made three of my five bugs testable, which I wouldn't have realized on my own.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?



---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.



- What is one thing you would do differently next time you work with AI on a coding task?



- In one or two sentences, describe how this project changed the way you think about AI generated code.



