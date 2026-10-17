"""Browser checks for Assignment 4. Run a local server before this script.

Install once: python -m pip install playwright
              python -m playwright install chromium
Run: python tools/check_forms.py --base-url http://127.0.0.1:8000

Typing, blur and submit-button clicks exercise native browser validation.
The event listener is test instrumentation only; the submitted HTML has no JS.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
MOTIVATION = "I aim to build useful student apps, learn teamwork, and improve my skills while solving practical problems at AITU Hack."
assert len(MOTIVATION) == 120


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--task2", default="task2.html")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    results = []

    def record(name: str, passed: bool, detail: object = None) -> None:
        results.append({"test": name, "passed": bool(passed), "detail": detail})
        print(f"{'PASS' if passed else 'FAIL'} {name}", flush=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        url = f"{base}/{args.task2.lstrip('/')}"
        page.goto(url, wait_until="networkidle")
        form = page.locator("form").first

        # Inspect source constraints independently of the example values.
        constraints = {
            "full-name": {"type": "text", "minlength": "2", "maxlength": "40", "required": ""},
            "university-email": {"type": "email", "required": ""},
            "age": {"type": "number", "min": "16", "max": "30", "step": "1", "required": ""},
            "team-size": {"type": "number", "min": "1", "max": "4", "step": "1", "required": ""},
            "track": {"required": ""},
            "arrival-date": {"type": "date", "min": "2026-11-20", "max": "2026-11-22", "required": ""},
            "checkin-time": {"type": "time", "min": "09:00", "max": "18:00", "step": "1800", "required": ""},
            "entry-fee": {"type": "number", "min": "0", "max": "5000", "step": "500", "required": ""},
            "github-url": {"type": "url", "required": None},
            "password": {"type": "password", "minlength": "8", "maxlength": "20", "required": ""},
            "motivation": {"minlength": "50", "maxlength": "300", "required": ""},
            "agreement": {"type": "checkbox", "required": ""},
        }
        for field, expected in constraints.items():
            actual = {attribute: page.locator(f"#{field}").get_attribute(attribute) for attribute in expected}
            record(f"HTML attributes: {field}", actual == expected, {"expected": expected, "actual": actual})

        record("Task 2 contains no script, pattern or novalidate", page.locator("script, [pattern], form[novalidate]").count() == 0)
        options = page.locator("#track option").evaluate_all("els => els.filter(el => el.value).map(el => el.textContent.trim())")
        record("Track offers exactly Web, Mobile, AI and GameDev", set(options) == {"Web", "Mobile", "AI", "GameDev"}, options)
        radio_names = page.locator('input[type="radio"]').evaluate_all("els => els.map(el => ({name: el.name, required: el.required}))")
        record("Three experience radios form one required group", len(radio_names) == 3 and len({item["name"] for item in radio_names}) == 1 and bool(radio_names[0]["name"]) and any(item["required"] for item in radio_names), radio_names)
        initially_visible = page.locator(".invalid-feedback").evaluate_all("els => els.filter(el => getComputedStyle(el).display !== 'none' && getComputedStyle(el).visibility !== 'hidden').map(el => el.textContent.trim())")
        record("No error feedback on initial page load", not initially_visible, initially_visible)

        def type_value(field: str, value: str) -> None:
            locator = page.locator(f"#{field}")
            locator.fill("")
            field_type = locator.get_attribute("type")
            if field_type in {"date", "time", "number"}:
                locator.fill(value)
            elif value:
                # Real keystrokes are necessary for the dirty-value flag used
                # by native minlength/maxlength checking.
                locator.press_sequentially(value)

        defaults = {
            "full-name": "Anna-Maria Lee",
            "university-email": "a.fedenko@astanait.edu.kz",
            "age": "18",
            "team-size": "4",
            "arrival-date": "2026-11-21",
            "checkin-time": "10:30",
            "entry-fee": "1500",
            "github-url": "",
            "password": "Astana2026",
            "motivation": MOTIVATION,
        }

        def prepare(field: str, value: str | bool) -> None:
            page.goto(url, wait_until="domcontentloaded")
            for field_id, default in defaults.items():
                type_value(field_id, str(value) if field_id == field else default)
            if field != "track" or value:
                page.locator("#track").select_option(label="Web")
            if field != "experience" or value:
                page.locator("#experience-beginner").check()
            if field == "track":
                if value:
                    page.locator("#track").select_option(label=str(value))
            if field != "agreement" or value:
                page.locator("#agreement").check()
            # A capture listener observes real submit events. Browsers never
            # dispatch that event for invalid forms after a button click.
            page.locator("form").first.evaluate("form => { form.dataset.testSubmits = '0'; form.addEventListener('submit', event => { event.preventDefault(); form.dataset.testSubmits = String(Number(form.dataset.testSubmits) + 1); }, true); }")

        examples = [
            ("Full name: Anna-Maria Lee", "full-name", "Anna-Maria Lee", True),
            ("Full name: A", "full-name", "A", False),
            ("Email: a.fedenko@astanait.edu.kz", "university-email", "a.fedenko@astanait.edu.kz", True),
            ("Email: a.fedenko", "university-email", "a.fedenko", False),
            ("Email: a.fedenko@", "university-email", "a.fedenko@", False),
            ("Age: 18", "age", "18", True),
            ("Age: 15", "age", "15", False),
            ("Age: 31", "age", "31", False),
            ("Team size: 4", "team-size", "4", True),
            ("Team size: 5", "team-size", "5", False),
            ("Team size: 2.5", "team-size", "2.5", False),
            ("Track: Web", "track", "Web", True),
            ("Track: Choose...", "track", "", False),
            ("Arrival: 2026-11-21", "arrival-date", "2026-11-21", True),
            ("Arrival: 2026-11-25", "arrival-date", "2026-11-25", False),
            ("Check-in: 10:30", "checkin-time", "10:30", True),
            ("Check-in: 10:15", "checkin-time", "10:15", False),
            ("Check-in: 19:00", "checkin-time", "19:00", False),
            ("Entry fee: 1500", "entry-fee", "1500", True),
            ("Entry fee: 1250", "entry-fee", "1250", False),
            ("Entry fee: 6000", "entry-fee", "6000", False),
            ("Experience: Beginner", "experience", True, True),
            ("Experience: none", "experience", False, False),
            ("GitHub: empty", "github-url", "", True),
            ("GitHub: full HTTPS URL", "github-url", "https://github.com/yerassyl-dev", True),
            ("GitHub: no protocol", "github-url", "github.com/yerassyl-dev", False),
            ("Password: Astana2026", "password", "Astana2026", True),
            ("Password: short", "password", "short", False),
            ("Motivation: 120 characters", "motivation", MOTIVATION, True),
            ("Motivation: 49 characters", "motivation", "a" * 49, False),
            ("Agreement: checked", "agreement", True, True),
            ("Agreement: unchecked", "agreement", False, False),
        ]
        boundaries = [
            ("Full name lower bound: 2", "full-name", "Li", True),
            ("Full name upper bound: 40", "full-name", "A" * 40, True),
            ("Age lower bound: 16", "age", "16", True),
            ("Age upper bound: 30", "age", "30", True),
            ("Age fraction: 18.5", "age", "18.5", False),
            ("Team size lower bound: 1", "team-size", "1", True),
            ("Team size below range: 0", "team-size", "0", False),
            ("Arrival lower bound: 2026-11-20", "arrival-date", "2026-11-20", True),
            ("Arrival upper bound: 2026-11-22", "arrival-date", "2026-11-22", True),
            ("Arrival before range: 2026-11-19", "arrival-date", "2026-11-19", False),
            ("Check-in lower bound: 09:00", "checkin-time", "09:00", True),
            ("Check-in upper bound: 18:00", "checkin-time", "18:00", True),
            ("Check-in below range: 08:30", "checkin-time", "08:30", False),
            ("Entry fee lower bound: 0", "entry-fee", "0", True),
            ("Entry fee upper bound: 5000", "entry-fee", "5000", True),
            ("Entry fee below range: -500", "entry-fee", "-500", False),
            ("Password lower bound: 8", "password", "Abcd1234", True),
            ("Password upper bound: 20", "password", "a" * 20, True),
            ("Motivation lower bound: 50", "motivation", "a" * 50, True),
            ("Motivation upper bound: 300", "motivation", "a" * 300, True),
            ("Track: Mobile", "track", "Mobile", True),
            ("Track: AI", "track", "AI", True),
            ("Track: GameDev", "track", "GameDev", True),
        ]
        for section, cases in (("PDF example", examples), ("Boundary", boundaries)):
            for name, field, value, expected in cases:
                prepare(field, value)
                actual = page.locator("form").first.evaluate("form => form.checkValidity()")
                invalid = page.locator("form :invalid").evaluate_all("els => els.filter(el => el.matches('input,select,textarea')).map(el => ({id:el.id, value:el.type === 'password' ? '(test password)' : el.value, missing:el.validity.valueMissing, type:el.validity.typeMismatch, underflow:el.validity.rangeUnderflow, overflow:el.validity.rangeOverflow, step:el.validity.stepMismatch, short:el.validity.tooShort, long:el.validity.tooLong}))")
                page.locator('form button[type="submit"], form input[type="submit"]').first.click()
                count = int(page.locator("form").first.get_attribute("data-test-submits") or "0")
                record(f"{section}: {name}", actual == expected and count == int(expected), {"expected_valid": expected, "actual_valid": actual, "submit_events": count, "invalid_controls": invalid})

        for field, limit in (("full-name", 40), ("password", 20), ("motivation", 300)):
            prepare(field, "a" * (limit + 1))
            length = len(page.locator(f"#{field}").input_value())
            record(f"maxlength prevents typing past {limit}: {field}", length == limit, {"typed": limit + 1, "stored_length": length})

        page.goto(url, wait_until="networkidle")
        type_value("full-name", "A")
        page.locator("#university-email").focus()
        feedback = page.locator("#full-name").evaluate("el => {const message = el.parentElement.querySelector('.invalid-feedback'); return { userInvalid:el.matches(':user-invalid'), visible:!!message && getComputedStyle(message).display !== 'none', text:message?.textContent.trim()}; }")
        record("Changed invalid field shows feedback after blur", feedback["userInvalid"] and feedback["visible"], feedback)

        screenshots = ROOT / "screenshots"
        screenshots.mkdir(exist_ok=True)
        for filename in ("index.html", "task1.html", "task2.html", "task3.html", "completed.html"):
            if not (ROOT / filename).exists():
                continue
            for width in (375, 1280):
                page.set_viewport_size({"width": width, "height": 1000})
                page.goto(f"{base}/{filename}", wait_until="networkidle")
                dimensions = page.evaluate("({viewport:innerWidth, document:document.documentElement.scrollWidth, body:document.body.scrollWidth})")
                record(f"No horizontal overflow: {filename} at {width}px", dimensions["document"] <= width and dimensions["body"] <= width, dimensions)
                if filename in ("task2.html", "task3.html"):
                    page.screenshot(path=str(screenshots / f"{Path(filename).stem}-{width}.png"), full_page=True)
                    if filename == "task2.html" and width == 1280:
                        page.screenshot(path=str(screenshots / "task2-overview.png"))
            if filename.startswith("task"):
                record(f"No JavaScript or novalidate: {filename}", page.locator("script, form[novalidate]").count() == 0)
        page.set_viewport_size({"width": 1280, "height": 1000})
        prepare("full-name", "Anna-Maria Lee")
        page.locator("#agreement").focus()
        page.screenshot(path=str(screenshots / "task2-filled.png"), full_page=True)
        page.goto(url, wait_until="networkidle")
        type_value("full-name", "A")
        type_value("university-email", "a.fedenko@")
        type_value("age", "15")
        type_value("team-size", "2.5")
        page.locator("#track").focus()
        page.screenshot(path=str(screenshots / "task2-errors.png"), full_page=True)
        page.locator(".registration-panel").screenshot(path=str(screenshots / "task2-errors-panel.png"))
        page.locator("fieldset.form-section").first.screenshot(path=str(screenshots / "task2-errors-detail.png"))
        browser_version = browser.version
        browser.close()

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "browser": f"Chromium {browser_version}",
        "base_url": base,
        "passed": sum(result["passed"] for result in results),
        "total": len(results),
        "results": results,
    }
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "task2-results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Результаты проверки форм", "", f"Браузер: {payload['browser']}. Проверено: {payload['passed']}/{payload['total']}.", "", "Проверки выполняют ввод с клавиатуры, смену фокуса и нажатие кнопки отправки. У невалидной формы событие submit не возникает. Обработчик, который отменяет отправку валидной формы, добавляется только тестом и отсутствует в HTML проекта.", "", "| Проверка | Результат |", "|---|---|"]
    lines.extend(f"| {item['test']} | {'PASS' if item['passed'] else 'FAIL'} |" for item in results)
    (docs / "task2-results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nPassed {payload['passed']}/{payload['total']}; evidence: docs/task2-results.json")
    return 0 if payload["passed"] == payload["total"] else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
