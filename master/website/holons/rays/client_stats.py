import datetime
import logging
import random
import requests
import time
from bs4 import BeautifulSoup

from rays.models import ClientStats


def store_client_stats(raw_rss: requests.models.Response, guid: str, feed_item: dict):
    """

    :param raw_rss:
    :param guid:
    :return:
    """
    client_data = parse_client_stats(guid)
    logging.info(client_data)
    record_exists = len(ClientStats.objects.filter(guid=guid))
    if 0 == record_exists:
        client_stats, created = ClientStats.objects.get_or_create(
            country=client_data.get('country'),
            city=client_data.get('city'),
            jobs_posted=client_data.get('jobs_posted'),
            hire_rate=client_data.get('hire_rate'),
            open_jobs=client_data.get('open_jobs'),
            rating=client_data.get('rating'),
            reviews_count=client_data.get('reviews_count'),
            guid=guid,
            pub_date=datetime.datetime.strptime(feed_item.get('published', ''), '%a, %d %b %Y %H:%M:%S %z'),
        )
    pass


def parse_client_stats(link):
    """
    Parse RSS-item for client data

    :return:
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3'}

    # data = [['country', 'city', 'jobs_posted', 'hire_rate', 'open_jobs', 'rating', 'reviews_count']]

    time.sleep(random.uniform(3, 19))

    s = requests.session()
    r = s.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    t = {}

    client_location = soup.find('li', {'data-qa': 'client-location'})
    if client_location:
        country = client_location.find('strong')
        if country:
            country = country.text.strip()
        t['country'] = country

        city = client_location.find('span')
        if city:
            city = city.text.strip()
        t['city'] = city
    else:
        t['country'] = None
        t['city'] = None

    job_posting_stats = soup.find('li', {'data-qa': 'client-job-posting-stats'})
    if job_posting_stats:
        jobs_posted = job_posting_stats.find('strong')
        if jobs_posted:
            jobs_posted = jobs_posted.text.strip().rstrip('jobs posted').strip()
        t['jobs_posted'] = jobs_posted

        hire_rate_and_jobs = job_posting_stats.find('div')
        if hire_rate_and_jobs:
            hire_rate_and_jobs = hire_rate_and_jobs.text.strip()
            hire_rate, open_jobs = hire_rate_and_jobs.split(',')
            hire_rate = hire_rate.strip().strip('hire rate').strip()
            open_jobs = open_jobs.strip().strip('open jobs').strip()

            t['hire_rate'] = hire_rate.replace('%', '')
            t['open_jobs'] = open_jobs
    else:
        t['jobs_posted'] = None
        t['hire_rate'] = None
        t['open_jobs'] = None

    member_since = soup.find('li', {'data-qa': 'client-contract-date'})
    if member_since:
        member_since = member_since.text.strip().replace('Member since', '').strip()
    t['member_since'] = member_since

    rating_block = soup.find('div', {'class': 'rating'})
    if rating_block:
        rating_block = rating_block.find('span').text.strip()
        rating = rating_block.split()[0].strip()
        reviews = rating_block.split()[2].strip()

        t['rating'] = rating
        t['reviews_count'] = reviews

    else:
        t['rating'] = None
        t['reviews_count'] = None

    return t

