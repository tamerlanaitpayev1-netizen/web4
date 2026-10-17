# Keyboard and submission checks

Browser: Playwright Chromium. Result: **44/44 passed**.

The tests use artificial example values and local HTTP only. No external forms are submitted. Computed outline/shadow checks verify a visible focus indicator; they do not replace a full accessibility review. Native date/time segments can take several Tab presses while retaining the same input ID.

| Check | Result |
| --- | --- |
| task1 audit: required fields and connected labels | PASS |
| task1 audit: carriage class is one required radio group | PASS |
| task1 audit: two journey radios share one name | PASS |
| task1 audit: passengers 1-6 | PASS |
| task1 audit: every field has a connected label | PASS |
| task1 audit: source order Clear then Find trains | PASS |
| task1 audit: button layout 375px | PASS |
| task1 audit: button layout 1280px | PASS |
| task1 audit: custom CSS has no fixed widths or absolute positioning | PASS |
| task1 audit: required palette appears in custom CSS | PASS |
| task1 audit: no script or novalidate | PASS |
| task1 1280px: Tab order matches source; no focus trap | PASS |
| task1 1280px: visible keyboard focus on every Tab stop | PASS |
| task1 375px: Tab order matches source; no focus trap | PASS |
| task1 375px: visible keyboard focus on every Tab stop | PASS |
| task1: empty submission blocked by native validation | PASS |
| task2 1280px: Tab order matches source; no focus trap | PASS |
| task2 1280px: visible keyboard focus on every Tab stop | PASS |
| task2 375px: Tab order matches source; no focus trap | PASS |
| task2 375px: visible keyboard focus on every Tab stop | PASS |
| task2: empty submission blocked by native validation | PASS |
| task3 1280px: Tab order matches source; no focus trap | PASS |
| task3 1280px: visible keyboard focus on every Tab stop | PASS |
| task3 375px: Tab order matches source; no focus trap | PASS |
| task3 375px: visible keyboard focus on every Tab stop | PASS |
| task3: empty submission blocked by native validation | PASS |
| task1: ArrowRight selects only the next journey radio | PASS |
| task1: Space toggles checkbox on and off | PASS |
| task1: ArrowRight selects only the next carriage radio | PASS |
| task1: Space toggles checkbox on and off | PASS |
| task2: ArrowRight selects only the next experience radio | PASS |
| task2: Space toggles checkbox on and off | PASS |
| task3: ArrowRight selects only the next seating radio | PASS |
| task3: Space toggles checkbox on and off | PASS |
| task1: completed example satisfies native constraints | PASS |
| task1: keyboard Enter submits POST and reaches local completion page | PASS |
| task2: completed example satisfies native constraints | PASS |
| task2: keyboard Enter submits POST and reaches local completion page | PASS |
| task3: invalid email rejected | PASS |
| task3: guest count 0 rejected | PASS |
| task3: guest count 1.5 rejected | PASS |
| task3: completed example satisfies native constraints | PASS |
| task3: keyboard Enter submits POST and reaches local completion page | PASS |
| task3: POST includes all nine field names and exactly one seating value | PASS |

Details and observed Tab order: [keyboard-results.json](keyboard-results.json). Reproduce with `python serve.py`, then `python tools/check_keyboard.py`.
