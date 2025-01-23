import json
import logging
from datetime import datetime
from typing import List, Optional
from urllib.parse import parse_qs, urlparse, urlencode, urlunparse

import pandas
import requests
import urllib3
from bs4 import BeautifulSoup
from pandas import DataFrame

from .model import BaseJobData
from .utils import cache_data

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


class LinkedInScraper:
    def __init__(self, query_search: str, location: str, max_pages: int = 5):
        self.search_query = query_search
        self.base_url = f"https://www.linkedin.com/jobs/search"
        self.url_params = {'keywords': query_search, 'location': location, 'pageNum': 0}
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.jobs: List[BaseJobData] = []
        self.max_pages = max_pages

    @property
    def get_jobs(self):
        if self.jobs:
            return self.jobs
        else:
            return ['No jobs to return.']

    def to_dataframe(self) -> DataFrame:
        return pandas.DataFrame(data=self.jobs)

    def append_url_params(self, params=None):

        parsed_url = urlparse(self.base_url)
        query_params = parse_qs(parsed_url.query)
        query_params.update(params if params else self.url_params)

        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed_url._replace(query=new_query)

        return urlunparse(new_parsed)

    def get_new_jobs_data(self, cached=False):
        response = None
        
        while True:
            logging.debug(f"Params: {self.url_params}")
            new_url = self.append_url_params()
            response = self.session.get(new_url)

            if response.status_code == 429:
                logging.error(f"Failed to retrieve data from {new_url}. Status code: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('div', class_='base-card')

            if not jobs:
                logging.info(f"No more jobs found on page.")
                logging.debug(f'URL: {new_url}')
                break

            for job in jobs:
                try:
                    title = job.find('h3', class_='base-search-card__title').text.strip()
                    company = job.find('h4', class_='base-search-card__subtitle').text.strip()
                    location = job.find('span', class_='job-search-card__location').text.strip()
                    job_link = job.find('a', class_='base-card__full-link')['href'].split('?')[0]
                    date_posted = (job.find('time', class_='job-search-card__listdate') or
                                   job.find('time', class_='job-search-card__listdate--new')
                                   )
                    if date_posted:
                        date_posted = date_posted['datetime']
                    logging.debug(f'Job found: title: {title}, company: {company}, location: {location}, date_posted:{date_posted}')
                    self.jobs.append(
                        BaseJobData(
                            title=title,
                            company=company,
                            location=location,
                            link=job_link,
                            created_at=date_posted
                        )
                    )
                except AttributeError as e:
                    logging.error(f"Error parsing job data: {e}")
            if cached:
                cache_data(data=self.jobs)

            if self.url_params['pageNum'] >= self.max_pages:
                break

            self.url_params['pageNum'] += 1

        logging.info(f'Getting new jobs finished. Found {len(self.jobs)} jobs')


# Usage example
if __name__ == "__main__":
    from time import sleep

    search_query = ''
    location = 'California, USA'
    jobs = []
    retries = 5
    retry_count = 0
    wait_threshold = 1

    linkedin = LinkedInScraper(query_search=search_query, location=location)

    while not jobs:
        linkedin.get_new_jobs_data()

        print(f"Going to sleep for {wait_threshold} seconds (retry: {retry_count}/{retries})...")
        sleep(wait_threshold)

        wait_threshold += wait_threshold
        retry_count += 1

        if retry_count == retries:
            break
