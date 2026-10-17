"""Create a portable archive of the complete coursework, excluding local metadata."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
destination = root / "dist" / "Assignment4_Aitpayev_Tamerlan.zip"
destination.parent.mkdir(exist_ok=True)
excluded = {".git", ".venv", ".tools", "dist", "__pycache__"}
with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if (path.is_file() and not any(part in excluded for part in relative.parts)
                and path.suffix not in {".log", ".pyc"}):
            archive.write(path, Path("Assignment4_Aitpayev_Tamerlan") / relative)
print(destination)
