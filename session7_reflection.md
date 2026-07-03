# Session 7 — Error & Learning Reflection

---

## Patterns Observed

**1. Holding too much in working memory**
Several errors came from trying to wire multiple things together mentally before the structure was externalised. The whiteboard fixed this when used. Use it earlier.

**2. Bracket and scope placement**
`conn.commit()` ended up inside `conn.execute()` brackets multiple times. The error is spatial — not reading the shape of the code before writing the next line.

**3. Conflating different things**
Linear probing and separate chaining were merged into one description. Two distinct concepts with similar surface features got collapsed. Slow down when two things feel similar — that's when the distinction matters most.

**4. Checking after the crash**
The `if value == KeyError` pattern — trying to catch an event as if it were a return value. The instinct was right, the mechanism was wrong.

---

## How To Work On These

**Before writing a line — draw the shape.**
Your framework is clear: abstract shape first, then detail. A blank function with its inputs and outputs labelled is enough. Writing into undefined space is where bracket errors and scope confusion come from.

**When two things feel similar — name the difference explicitly.**
Don't proceed until you can state in one sentence what separates them.

**When something fails — ask what assumption broke, not what the fix is.**
The fix follows from the correct diagnosis. Rushing to the fix skips the learning.

---

*Errors are model updates. The discomfort is the signal the model is restructuring — not evidence of inability.*
