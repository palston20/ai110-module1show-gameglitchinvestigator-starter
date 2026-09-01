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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
