import requests
from config import SEARCH_CONFIG, SARAMIN_API_KEY

BASE_URL = "https://oapi.saramin.co.kr/job-search"

JOB_TYPE_MAP = {
    "신입": "1",
    "인턴": "5",
}


def fetch_jobs() -> list:
    if not SARAMIN_API_KEY:
        print("[사람인] SARAMIN_API_KEY 환경변수가 없습니다.")
        return []

    job_types = ",".join(
        JOB_TYPE_MAP[c] for c in SEARCH_CONFIG["job_category"] if c in JOB_TYPE_MAP
    )

    params = {
        "access-key": SARAMIN_API_KEY,
        "keywords": " ".join(SEARCH_CONFIG["keywords"]),
        "job_mid_cd": "2",   # IT개발·데이터
        "loc_cd": "101000",  # 서울
        "job_type": job_types,
        "count": 100,
        "start": 1,
        "fields": "count,position,id,active",
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[사람인] 요청 실패: {e}")
        return []

    jobs = []
    for item in data.get("jobs", {}).get("job", []):
        position = item.get("position", {})
        company = position.get("company", {}).get("detail", {})
        location = position.get("location", {}).get("name", "")

        codes = [c.get("name", "") for c in position.get("job-code", [])]
        title = position.get("title", "")
        text = " ".join(codes) + " " + title
        if not any(k.lower() in text.lower() for k in SEARCH_CONFIG["keywords"]):
            continue

        close_type = item.get("close-type", {}).get("name", "")
        deadline = "상시" if close_type == "상시채용" else item.get("expiration-date", "상시")

        jobs.append({
            "id": str(item.get("id")),
            "title": title,
            "company": company.get("name", ""),
            "location": location,
            "skills": codes[:5],
            "deadline": deadline,
            "url": item.get("url", ""),
            "source": "사람인",
        })

    return jobs
