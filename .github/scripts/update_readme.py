import os
import re
import requests

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

response = requests.get(
    f"https://api.github.com/users/{USERNAME}/repos",
    headers=headers,
    params={"sort": "stargazers", "per_page": 100, "type": "owner"}
)

repos = response.json()
repos = [r for r in repos if not r["fork"]]
top3 = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:3]

cards = "\n".join([
    f'<a href="{r["html_url"]}">\n'
    f'    <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={r["name"]}&theme=dark&hide_border=true" />\n'
    f'  </a>'
    for r in top3
])

block = f"<!-- TOP_REPOS_START -->\n<p>\n  {cards}\n</p>\n<!-- TOP_REPOS_END -->"

with open("README.md", "r") as f:
    content = f.read()

updated = re.sub(
    r"<!-- TOP_REPOS_START -->.*?<!-- TOP_REPOS_END -->",
    block,
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(updated)

print(f"Updated with top repos: {[r['name'] for r in top3]}")
