"""Independent keyboard and native submission checks for Assignment 4.

Start python serve.py first, then run python tools/check_keyboard.py.
Only this test uses browser automation; submitted HTML pages contain no JavaScript.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import parse_qs

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8000"
RESULTS: list[dict] = []


def record(name: str, passed: bool, details=None) -> None:
    RESULTS.append({"test": name, "passed": bool(passed), "details": details})
    print(f"{'PASS' if passed else 'FAIL'} {name}")


FOCUS = """() => {
  const el = document.activeElement;
  const key = el.id || (el.tagName.toLowerCase() + ':' + (el.getAttribute('href') || el.textContent.trim().slice(0, 55)));
  const labels = el.labels ? Array.from(el.labels) : [];
  const candidates = [el, ...labels, el.parentElement].filter(Boolean);
  const signals = candidates.map(candidate => {
    const s = getComputedStyle(candidate), r = candidate.getBoundingClientRect();
    const visible = r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0' && s.clip === 'auto';
    const outline = parseFloat(s.outlineWidth) > 0 && !['none','hidden'].includes(s.outlineStyle);
    return {tag: candidate.tagName, id: candidate.id, visible, outline, shadow: s.boxShadow !== 'none'};
  });
  return {key, domIndex: Array.from(document.querySelectorAll('*')).indexOf(el), tag: el.tagName, type: el.type || null, focusVisible: el.matches(':focus-visible'), indicator: signals.some(s => s.visible && (s.outline || s.shadow)), signals};
}"""


def tab_walk(page, task: str, width: int) -> None:
    page.set_viewport_size({"width": width, "height": 1000})
    page.goto(f"{BASE}/{task}.html", wait_until="networkidle")
    expected = page.locator('a[href], input:not([type="hidden"]), select, textarea, button, summary').evaluate_all("""els => {
      const radioGroups = new Set();
      return els.filter(el => {
        if (el.disabled) return false;
        if (el.type === 'radio') { if (radioGroups.has(el.name)) return false; radioGroups.add(el.name); }
        return true;
      }).map(el => el.id || (el.tagName.toLowerCase() + ':' + (el.getAttribute('href') || el.textContent.trim().slice(0, 55))));
    }""")
    states = []
    for _ in range(80):
        page.keyboard.press("Tab")
        state = page.evaluate(FOCUS)
        if state["tag"] == "BODY":
            continue
        if states and state["domIndex"] == states[0]["domIndex"]:
            break
        # Date/time inputs can have multiple native segments with the same ID.
        if not states or state["domIndex"] != states[-1]["domIndex"]:
            states.append(state)
    actual = [s["key"] for s in states]
    record(f"{task} {width}px: Tab order matches source; no focus trap", actual == expected, {"expected": expected, "actual": actual})
    failures = [s for s in states if not s["focusVisible"] or not s["indicator"]]
    record(f"{task} {width}px: visible keyboard focus on every Tab stop", not failures, {"stops": len(states), "failures": failures})


def blank_submit(page, task: str) -> None:
    page.goto(f"{BASE}/{task}.html", wait_until="networkidle")
    posts = []
    listener = lambda req: posts.append(req.url) if req.method == "POST" else None
    page.on("request", listener)
    page.locator('button[type="submit"]').focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(100)
    record(f"{task}: empty submission blocked by native validation", not posts and page.url.endswith(f"/{task}.html") and page.locator(":invalid").count() > 0, {"post_requests": len(posts), "focused_id": page.evaluate("document.activeElement.id")})
    page.remove_listener("request", listener)


def radio_and_checkbox(page, task: str, first: str, second: str, group: str, checkbox: str) -> None:
    page.goto(f"{BASE}/{task}.html", wait_until="networkidle")
    page.locator(first).focus()
    page.keyboard.press("Space")
    page.keyboard.press("ArrowRight")
    chosen = page.locator(f'input[type="radio"][name="{group}"]:checked').evaluate_all("els => els.map(el => el.id)")
    record(f"{task}: ArrowRight selects only the next {group} radio", chosen == [second.lstrip("#")], chosen)
    page.locator(checkbox).focus()
    page.keyboard.press("Space")
    first_state = page.locator(checkbox).is_checked()
    page.keyboard.press("Space")
    record(f"{task}: Space toggles checkbox on and off", first_state and not page.locator(checkbox).is_checked())


def valid_submit(page, task: str) -> None:
    page.goto(f"{BASE}/{task}.html", wait_until="networkidle")
    if task == "task1":
        page.locator("#one-way").focus(); page.keyboard.press("Space")
        values = {"from": "Astana", "to": "Almaty", "departure": "2026-11-21", "phone": "701 234 56 78", "email": "learner@example.com"}
        for field, value in values.items():
            page.locator(f"#{field}").fill(value)
        page.locator("#passengers").select_option("2")
        page.locator("#seat").focus(); page.keyboard.press("Space")
        page.locator("#train-agreement").focus(); page.keyboard.press("Space")
    elif task == "task2":
        values = {"full-name": "Demo Learner", "university-email": "learner@example.edu", "age": "20", "team-size": "2", "arrival-date": "2026-11-21", "checkin-time": "10:30", "entry-fee": "1500", "password": "DemoOnly123", "motivation": "I want to build useful tools with a small team, improve my skills and learn how to present a working prototype."}
        for field, value in values.items():
            page.locator(f"#{field}").fill(value)
        page.locator("#track").select_option("Web")
        page.locator("#experience-beginner").focus(); page.keyboard.press("Space")
        page.locator("#agreement").focus(); page.keyboard.press("Space")
    else:
        values = {"full-name": "Demo Guest", "email": "guest@example.com", "phone": "+7 700 000 00 00", "guests": "3", "date": "2026-11-21", "comments": "A quiet table, please."}
        for field, value in values.items():
            page.locator(f"#{field}").fill(value)
        page.locator("#meal").select_option("dinner")
        page.locator("#seating-inside").focus(); page.keyboard.press("Space"); page.keyboard.press("ArrowRight")
        page.locator("#terms").focus(); page.keyboard.press("Space")
        record("task3: invalid email rejected", page.locator("#email").evaluate("e => { e.value = 'not-an-email'; return !e.validity.valid && e.validity.typeMismatch; }"))
        page.locator("#email").fill("guest@example.com")
        for value, flag in [("0", "rangeUnderflow"), ("1.5", "stepMismatch")]:
            page.locator("#guests").fill(value)
            record(f"task3: guest count {value} rejected", page.locator("#guests").evaluate(f"e => !e.validity.valid && e.validity.{flag}"))
        page.locator("#guests").fill("3")
    record(f"{task}: completed example satisfies native constraints", page.locator("form").evaluate("f => f.checkValidity()"))
    with page.expect_request(lambda request: request.method == "POST" and request.url.endswith("/completed.html")) as post_info:
        page.locator('button[type="submit"]').focus()
        page.keyboard.press("Enter")
    payload = parse_qs(post_info.value.post_data or "", keep_blank_values=True)
    page.wait_for_url("**/completed.html")
    record(f"{task}: keyboard Enter submits POST and reaches local completion page", page.url.endswith("/completed.html"), {"method": post_info.value.method, "payload_field_names": sorted(payload)})
    if task == "task3":
        expected = {"full_name", "email", "phone", "guests", "date", "seating", "meal", "comments", "terms"}
        record("task3: POST includes all nine field names and exactly one seating value", set(payload) == expected and payload["seating"] == ["terrace"] and all(len(v) == 1 for v in payload.values()), {"names": sorted(payload), "seating": payload.get("seating")})


def static_task1(page) -> None:
    page.goto(f"{BASE}/task1.html")
    required = ["from", "to", "departure", "phone", "email", "train-agreement"]
    record("task1 audit: required fields and connected labels", all(page.locator(f"#{i}").get_attribute("required") is not None and page.locator(f"#{i}").evaluate("e => e.labels.length > 0") for i in required))
    record("task1 audit: carriage class is one required radio group", page.locator('input[name="carriage"][type="radio"][required]').count() == 3)
    record("task1 audit: two journey radios share one name", page.locator('input[name="journey"][type="radio"]').count() == 2)
    passengers = page.locator("#passengers option").evaluate_all("els => els.filter(e => e.value).map(e => e.value)")
    record("task1 audit: passengers 1-6", passengers == [str(n) for n in range(1, 7)], passengers)
    unlabeled = page.locator('input:not([type="hidden"]),select,textarea').evaluate_all("els => els.filter(e => !e.labels.length).map(e => e.id)")
    record("task1 audit: every field has a connected label", not unlabeled, unlabeled)
    actions = page.locator(".form-actions button").evaluate_all("els => els.map(e => e.type)")
    record("task1 audit: source order Clear then Find trains", actions == ["reset", "submit"], actions)
    for width in [375, 1280]:
        page.set_viewport_size({"width": width, "height": 1000})
        reset = page.locator('button[type="reset"]').bounding_box()
        submit = page.locator('button[type="submit"]').bounding_box()
        valid = submit["y"] < reset["y"] if width == 375 else reset["x"] < submit["x"] and abs(reset["y"]-submit["y"]) < 1
        record(f"task1 audit: button layout {width}px", valid)
    css = (ROOT / "assets/task1.css").read_text(encoding="utf-8")
    fixed_widths = re.findall(r"(?:^|[;{])\s*(?:width|min-width|max-width)\s*:\s*[\d.]+(?:px|rem|em)", css)
    absolute_positioning = re.findall(r"position\s*:\s*absolute", css)
    record("task1 audit: custom CSS has no fixed widths or absolute positioning", not fixed_widths and not absolute_positioning)
    record("task1 audit: required palette appears in custom CSS", all(color in css.lower() for color in ["#0f6b5f", "#f2a93b", "#16302b", "#f4f7f5", "#e6efec"]))
    record("task1 audit: no script or novalidate", page.locator("script,form[novalidate]").count() == 0)


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        static_task1(page)
        for task in ["task1", "task2", "task3"]:
            for width in [1280, 375]:
                tab_walk(page, task, width)
            blank_submit(page, task)
        radio_and_checkbox(page, "task1", "#one-way", "#round-trip", "journey", "#sms")
        radio_and_checkbox(page, "task1", "#seat", "#coupe", "carriage", "#train-agreement")
        radio_and_checkbox(page, "task2", "#experience-beginner", "#experience-intermediate", "experience", "#agreement")
        radio_and_checkbox(page, "task3", "#seating-inside", "#seating-terrace", "seating", "#terms")
        for task in ["task1", "task2", "task3"]:
            valid_submit(page, task)
        browser.close()
    summary = {"browser": "Playwright Chromium", "passed": sum(r["passed"] for r in RESULTS), "total": len(RESULTS), "checks": RESULTS}
    (ROOT / "docs/keyboard-results.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    rows = ["# Keyboard and submission checks", "", f"Browser: Playwright Chromium. Result: **{summary['passed']}/{summary['total']} passed**.", "", "The tests use artificial example values and local HTTP only. No external forms are submitted. Computed outline/shadow checks verify a visible focus indicator; they do not replace a full accessibility review. Native date/time segments can take several Tab presses while retaining the same input ID.", "", "| Check | Result |", "| --- | --- |"]
    rows += [f"| {r['test']} | {'PASS' if r['passed'] else 'FAIL'} |" for r in RESULTS]
    rows += ["", "Details and observed Tab order: [keyboard-results.json](keyboard-results.json). Reproduce with `python serve.py`, then `python tools/check_keyboard.py`."]
    (ROOT / "docs/keyboard-results.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Total: {summary['passed']}/{summary['total']}")
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
