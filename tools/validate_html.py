"""Send the public assignment HTML to the official Nu HTML Checker.

Run: python tools/validate_html.py
The original JSON response is preserved in docs/w3c-task3.json. Network
failures are recorded and are never reported as successful validation.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", default="task3.html")
    args = parser.parse_args()
    source = ROOT / args.file
    output = ROOT / "docs" / f"w3c-{source.stem}.json"
    output.parent.mkdir(exist_ok=True)
    request = urllib.request.Request(
        "https://validator.w3.org/nu/?out=json",
        data=source.read_bytes(),
        headers={"Content-Type": "text/html; charset=utf-8", "User-Agent": "Assignment4-HTML-Validation/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
        errors = [message for message in result.get("messages", []) if message.get("type") == "error"]
        result["_evidence"] = {
            "file": source.name,
            "validator": request.full_url,
            "checked_utc": datetime.now(timezone.utc).isoformat(),
            "status": "passed" if not errors else "failed",
            "error_count": len(errors),
        }
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{source.name}: {len(errors)} W3C errors; {len(result.get('messages', []))} total messages")
        for message in result.get("messages", []):
            print(f"{message.get('type')}: line {message.get('lastLine', '?')}: {message.get('message')}")
        print(f"Evidence: {output.relative_to(ROOT)}")
        return 1 if errors else 0
    except (OSError, ValueError, urllib.error.URLError) as exc:
        output.write_text(json.dumps({"_evidence": {"file": source.name, "validator": request.full_url, "checked_utc": datetime.now(timezone.utc).isoformat(), "status": "unavailable", "reason": str(exc)}}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"W3C validation unavailable: {exc}. No success is claimed.")
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
