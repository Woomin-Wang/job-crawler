import requests
from config import SEARCH_CONFIG

BASE_URL = "https://www.wanted.co.kr/api/v4/jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "wanted-user-language": "ko",
    "wanted-user-country": "KR",
}

# 백엔드 직군 코드
JOB_CATEGORY_TAG = 872  # 서버/백엔드

def fetch_jobs() -> list:
    jobs = []
    params = {
        "job_category_tag_id": JOB_CATEGORY_TAG,
        "country": "kr",
        "job_sort": "job.latest_order",
        "years": 0,  # 신입
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

    for item in data.get("data", []):
        job = item.get("job", {})
        company = job.get("company", {})
        address = job.get("address", {})

        # 서울 필터
        location = address.get("location", "")
        if "서울" not in location:
            continue

        # Java or Spring 키워드 필터
        skills = [s.get("skill_tag", {}).get("title", "") for s in job.get("skill_tags", [])]
        title = job.get("title", "")
        desc = job.get("description", "")
        text = " ".join(skills) + " " + title + " " + desc

        if not any(k.lower() in text.lower() for k in SEARCH_CONFIG["keywords"]):
            continue

        jobs.append({
            "id": str(job.get("id")),
            "title": title,
            "company": company.get("name", ""),
            "location": location,
            "skills": skills[:5],
            "deadline": job.get("due_time", "상시") or "상시",
            "url": f"https://www.wanted.co.kr/wd/{job.get('id')}",
            "source": "원티드",
        })

    return jobs
