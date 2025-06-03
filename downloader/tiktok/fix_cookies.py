import json
from pathlib import Path

in_path = Path("downloader/tiktok/cookies.json")
cookies = json.loads(in_path.read_text())

for c in cookies:
    c["sameSite"] = "Lax"

in_path.write_text(json.dumps(cookies, indent=2))
print(f"✅ Cleaned {len(cookies)} cookies for Playwright.")
