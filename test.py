from pathlib import Path
p = Path("/data/test.txt")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("Hello", encoding="utf-8")
print("File exists:", p.exists(), p.resolve())
