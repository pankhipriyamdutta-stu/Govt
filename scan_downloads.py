import os
import glob
from pathlib import Path
import json

downloads_dir = Path("C:/Users/pankh/Downloads")

files = []
for f in downloads_dir.iterdir():
    if f.is_file():
        files.append({
            "name": f.name,
            "size": f.stat().st_size,
            "mtime": f.stat().st_mtime,
            "ext": f.suffix
        })

# Sort by modification time descending
files.sort(key=lambda x: x["mtime"], reverse=True)

with open("downloads_inventory.json", "w", encoding="utf-8") as out:
    json.dump(files[:100], out, indent=2)

print(f"Total files in Downloads: {len(files)}")
print("Top 30 most recent files:")
for f in files[:30]:
    print(f"{f['name']} ({f['size']} bytes)")
