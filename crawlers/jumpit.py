import requests
from config import SEARCH_CONFIG

BASE_URL = "https://jumpit.saramin.co.kr/api/positions"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://jumpit.saramin.co.kr",
    "Referer": "https://jumpit.saramin.co.kr/",
}

JOB_CATEGORY = 1  # 서버/백엔드 개발자


def fetch_jobs() -> list:
    params = {
        "sort": "rsp_rate",
        "jobCategory": JOB_CATEGORY,
        "page": 1,
    }

    try:
        resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[점핏] 요청 실패: {e}")
        return []

    jobs = []
    for item in data.get("result", {}).get("positions", []):
        locations = item.get("locations", [])
        if not any("서울" in loc for loc in locations):
            continue

        stacks = item.get("techStacks", [])
        title = item.get("title", "")
        text = " ".join(stacks) + " " + title
        if not any(k.lower() in text.lower() for k in SEARCH_CONFIG["keywords"]):
            continue

        jobs.append({
            "id": str(item.get("id")),
            "title": title,
            "company": item.get("companyName", ""),
            "location": ", ".join(locations),
            "skills": stacks[:5],
            "deadline": item.get("closedAt") or "상시",
            "url": f"https://jumpit.saramin.co.kr/position/{item.get('id')}",
            "source": "점핏",
        })

    return jobs
