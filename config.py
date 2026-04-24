import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SARAMIN_API_KEY = os.getenv("SARAMIN_API_KEY")

SEARCH_CONFIG = {
    "location": "서울",
    "job_type": "backend",
    "keywords": ["Java", "Spring"],
    "job_category": ["신입", "인턴"],
}
