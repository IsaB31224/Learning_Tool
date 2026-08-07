# Ticket: ReflectionTimer — 30-second forced-pause timer

**Component:** `shared/reflection_timer.py` (new file)

**Context:** Tool 2's Add-Reflection flow needs a mandatory 30-second pause where the reflection box is locked and a live counter is shown. This ticket covers only the underlying timer state object — the UI wiring (disabling the box, driving the live counter, scheduling repeated checks) is separate and out of scope here.

## Requirements

- A class, `ReflectionTimer`.
- On construction, it takes a `duration` (seconds) and records the moment it was created using a monotonic time source — not wall-clock time.
- `seconds_remaining()` — returns the whole seconds left in the countdown, computed fresh from `duration`, the recorded start point, and the current time each time it's called. Never returns a negative number.
- `is_timer_finished()` — returns `True` once the countdown has reached zero, `False` otherwise. This must be derived from `seconds_remaining()`, not tracked as its own separate flag.
- No dependency on PyQt6 or any UI framework — must be usable and testable entirely on its own.
- No internal looping, sleeping, or blocking — the object only answers questions when asked; it does not run anything itself.

## Acceptance criteria

- `ReflectionTimer(30)` created, then `seconds_remaining()` called immediately, returns `30` (agreed truncation behavior).
- Repeated calls to `seconds_remaining()` over real elapsed time stay accurate even if the calls happen at irregular intervals.
- Once 30 real seconds have passed, `seconds_remaining()` returns `0` and stays at `0` (doesn't go negative), and `is_timer_finished()` returns `True` from that point on.

## Out of scope

UI wiring, text box enable/disable, live counter rendering, `QTimer` scheduling — all handled separately once this is done.
