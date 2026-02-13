import requests
from datetime import datetime, timedelta

USERNAME = "ashiksharonm"
DAYS_LOOKBACK = 365
MAX_PROJECTS = 4

since_date = datetime.utcnow() - timedelta(days=DAYS_LOOKBACK)

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
repos = requests.get(url, headers=headers).json()

selected = []

for repo in repos:
    if repo.get("fork"):
        continue

    topics = repo.get("topics", [])
    if "portfolio" not in topics:
        continue

    pushed_at = datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
    if pushed_at < since_date:
        continue

    selected.append(repo)

selected = sorted(selected, key=lambda r: r["pushed_at"], reverse=True)[:MAX_PROJECTS]

blocks = []
for r in selected:
    blocks.append(
        f"""### 🔹 {r['name']}
{r['description'] or "Production-grade AI project"}
➡️ Repo: {r['html_url']}
"""
    )

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

start = "<!-- PROJECTS:START -->"
end = "<!-- PROJECTS:END -->"

if start not in readme or end not in readme:
    raise ValueError("Markers not found in README")

new_section = start + "\n\n" + "\n\n".join(blocks) + "\n\n" + end

updated = readme.replace(
    readme[readme.index(start): readme.index(end) + len(end)],
    new_section
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)
