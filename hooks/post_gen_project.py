from pathlib import Path

p = Path(".env-template")
p.rename(Path(".env"))
