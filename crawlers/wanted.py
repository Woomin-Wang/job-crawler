import requests

BASE_URL = "https://www.wanted.co.kr/api/chaos/navigation/v1/results"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "wanted-user-country": "KR",
}

JOB_GROUP_ID = 518      # IT 개발 그룹
BACKEND_CATEGORY_ID = 872  # 서버/백엔드


def fetch_jobs() -> list:
    params = {
        "job_group_id": JOB_GROUP_ID,
        "country": "kr",
        "job_sort": "job.latest_order",
        "years": 0,
        "locations": "seoul.all",
        "limit": 100,
        "offset": 0,
    }

    try:
        resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[원티드] 요청 실패: {e}")
        return []

    jobs = []
    for item in data.get("data", []):
        if item.get("category_tag", {}).get("id") != BACKEND_CATEGORY_ID:
            continue

        jobs.append({
            "id": str(item.get("id")),
            "title": item.get("position", ""),
            "company": item.get("company", {}).get("name", ""),
            "location": item.get("address", {}).get("location", ""),
            "skills": [],
            "deadline": item.get("due_time", "상시") or "상시",
            "url": f"https://www.wanted.co.kr/wd/{item.get('id')}",
            "source": "원티드",
        })

    return jobs
