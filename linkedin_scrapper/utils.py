import json
from datetime import datetime
from pathlib import Path

from linkedin_scrapper.model import BaseJobData

user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]
cache_filename = 'cache.json'


def cache_data(data: list[BaseJobData], cache_file=cache_filename):
    jobs_dict_list = []
    for job in data:
        jobs_dict_list.append(job.to_dict())

    with open(cache_file, 'a', encoding='utf8') as f:
        json.dump(jobs_dict_list, f)


def read_cache(cache_file: Path):
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            return json.load(f)

    return []


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
