from crawlers import wanted, saramin, jumpit
from notifier import discord
from storage.seen_jobs import filter_new


def run():
    all_new_jobs = []

    print("[원티드] 크롤링 시작...")
    new_wanted = filter_new(wanted.fetch_jobs(), "wanted")
    print(f"[원티드] 새 공고 {len(new_wanted)}건")
    all_new_jobs.extend(new_wanted)

    print("[사람인] 크롤링 시작...")
    new_saramin = filter_new(saramin.fetch_jobs(), "saramin")
    print(f"[사람인] 새 공고 {len(new_saramin)}건")
    all_new_jobs.extend(new_saramin)

    print("[점핏] 크롤링 시작...")
    new_jumpit = filter_new(jumpit.fetch_jobs(), "jumpit")
    print(f"[점핏] 새 공고 {len(new_jumpit)}건")
    all_new_jobs.extend(new_jumpit)

    if all_new_jobs:
        print(f"총 {len(all_new_jobs)}건 디스코드 전송 중...")
        discord.send(all_new_jobs)
        print("전송 완료!")
    else:
        print("새 공고 없음")


if __name__ == "__main__":
    run()
