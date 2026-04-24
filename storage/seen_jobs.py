import json
import os

STORAGE_PATH = os.path.join(os.path.dirname(__file__), "seen_jobs.json")


def load_seen() -> set:
    if not os.path.exists(STORAGE_PATH):
        return set()
    with open(STORAGE_PATH, "r") as f:
        return set(json.load(f))


def save_seen(seen: set):
    with open(STORAGE_PATH, "w") as f:
        json.dump(list(seen), f)


def filter_new(jobs: list, source: str) -> list:
    seen = load_seen()
    new_jobs = []
    for job in jobs:
        job_id = f"{source}_{job['id']}"
        if job_id not in seen:
            new_jobs.append(job)
            seen.add(job_id)
    save_seen(seen)
    return new_jobs
