import pandas as pd
import time
import sys
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException
from data.flight.utils import get_print_time, PATH
from data.flight.ita_matrix_scraper import initialize_driver, close_driver, create_session, build_url, access_url, parse_results
from data.db.utils import create_db_connection
from data.db.flight import insert_trip, remove_trip


def create_one_way_jobs(departure_airport_cd_list,
                        arrival_airport_cd_list,
                        departure_dates):
    job_list = []

    for departure_airport_cd in departure_airport_cd_list:
        for arrival_airport_cd in arrival_airport_cd_list:
            for date in departure_dates:
                job_list.append({
                    "trip_type": "one-way",
                    "slices": [{
                        "departure_airport_cds": [departure_airport_cd],
                        "arrival_airport_cds": [arrival_airport_cd],
                        "departure_date": date
                    }],
                    "currency_cd": 'USD'
                })

    return job_list


# Initialize
jobs = []
jobs.extend(
    create_one_way_jobs(
        departure_airport_cd_list=['NAS', 'PTP', 'PUJ', 'SDQ', 'SXM'],
        arrival_airport_cd_list=['ATL'],
        departure_dates=['2024-12-01']
    )
)

total_jobs = len(jobs)
print(f"[{get_print_time()}] Created {total_jobs} jobs")


# Process jobs
db_connection = create_db_connection()
driver = initialize_driver()
session_id = create_session(driver, currency_cd='USD')

for idx, job in enumerate(jobs, 1):
    print(f"[{get_print_time()}] Job: Processing {idx}/{total_jobs} ({job})")

    url = build_url(**job, session_id=session_id)
    print(url)
    raw_results, access_dt = access_url(driver, url)
    print(raw_results)
    parsed_results = parse_results(job["trip_type"], raw_results, access_dt)
    print(parsed_results)

    time.sleep(1)

close_driver(driver)