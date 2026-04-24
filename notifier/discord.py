import requests
from datetime import datetime
from config import DISCORD_WEBHOOK_URL

SOURCE_COLORS = {
    "원티드": 0x5865F2,
    "사람인": 0x57F287,
    "점핏":   0xFEE75C,
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
    skill_text = "  ".join(f"`{s}`" for s in skills) if skills else "정보 없음"
    deadline = _format_deadline(job.get("deadline", "상시"))

    return {
        "color": SOURCE_COLORS.get(source, 0x5865F2),
        "author": {"name": source},
        "title": f"{job['company']} — {job['title']}",
        "url": job.get("url", ""),
        "fields": [
            {"name": "기술스택", "value": skill_text, "inline": False},
            {"name": "📍 위치", "value": job.get("location", ""), "inline": True},
            {"name": "📅 마감", "value": f"~ {deadline}", "inline": True},
        ],
    }


def send(jobs: list):
    if not jobs:
        return

    if not DISCORD_WEBHOOK_URL:
        print("[디스코드] DISCORD_WEBHOOK_URL 환경변수가 없습니다.")
        return

    # 디스코드 embed 최대 10개 제한
    for i in range(0, len(jobs), 10):
        chunk = jobs[i:i + 10]
        embeds = [_build_embed(job) for job in chunk]
        payload = {
            "content": f"🆕 새 공고 {len(jobs)}건" if i == 0 else None,
            "embeds": embeds,
        }

        try:
            resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[디스코드] 전송 실패: {e}")
