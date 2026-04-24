import requests
from datetime import datetime
from config import DISCORD_WEBHOOK_URL

SOURCE_COLORS = {
    "원티드": 0x258BF5,
    "사람인": 0xFF4D4D,
    "점핏":   0x845EF7,
}


def _format_deadline(deadline: str) -> str:
    if deadline == "상시":
        return "상시"
    try:
        dt = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
        return dt.strftime("%m/%d")
    except Exception:
        return deadline


def _build_embed(job: dict) -> dict:
    source = job.get("source", "")
    skills = job.get("skills", [])
    deadline = _format_deadline(job.get("deadline", "상시"))
    location = job.get("location", "")

    description = f"🏢 **{job['company']}**\n📍 {location}　·　📅 ~ {deadline}"

    embed = {
        "color": SOURCE_COLORS.get(source, 0x5865F2),
        "author": {"name": source},
        "title": job["title"],
        "url": job.get("url", ""),
        "description": description,
    }

    if skills:
        embed["fields"] = [
            {
                "name": "🛠 기술스택",
                "value": "  ".join(f"`{s}`" for s in skills),
                "inline": False,
            }
        ]

    return embed


def _build_content(jobs: list) -> str:
    from collections import Counter
    counts = Counter(job["source"] for job in jobs)
    summary = "  |  ".join(f"{src} {cnt}건" for src, cnt in counts.items())
    return f"🔔 **새 공고 {len(jobs)}건** — {summary}"


def send(jobs: list):
    if not jobs:
        return

    if not DISCORD_WEBHOOK_URL:
        print("[디스코드] DISCORD_WEBHOOK_URL 환경변수가 없습니다.")
        return

    for i in range(0, len(jobs), 10):
        chunk = jobs[i:i + 10]
        payload = {
            "content": _build_content(jobs) if i == 0 else None,
            "embeds": [_build_embed(job) for job in chunk],
        }

        try:
            resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[디스코드] 전송 실패: {e}")
