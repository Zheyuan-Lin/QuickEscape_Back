import pandas as pd
import time
import sys
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException
from data.flight.utils import get_print_time, PATH
from data.flight.ita_matrix_scraper import initialize_driver, close_driver, create_session, build_url, access_url, parse_results
from data.db.utils import create_db_connection
from data.db.flight import insert_trip, remove_trip


def create_dates(start_date, end_date, step=1):
    dates = pd.date_range(start=start_date, end=end_date, freq=f"{step}D").tolist()
    return [date.strftime("%Y-%m-%d") for date in dates]


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
results = []
max_retry = 3
retry_wait_time = 2


# Give two params: split by how many parts and which part to run
args = sys.argv[1:]
print(f"[{get_print_time()}] Args: {args}")

if len(args) == 2:
    part, total_parts = map(int, args)
    print(f"[{get_print_time()}] Running part {part} of {total_parts}")

    airports_df = pd.read_csv(f"{PATH}/data/city/data_processed/airports.csv")
    airports_df = airports_df.iloc[
        part - 1::total_parts
    ].reset_index(drop=True)

else:
    print(f"[{get_print_time()}] Running all parts")
    airports_df = pd.read_csv(f"{PATH}/data/city/data_processed/airports.csv")


# Create jobs
date_current = datetime.today().strftime("%Y-%m-%d")
date_begin = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
date_end = (datetime.today() + timedelta(days=100)).strftime("%Y-%m-%d")

jobs = []
jobs.extend(
    create_one_way_jobs(
        departure_airport_cd_list=['ATL'],
        arrival_airport_cd_list=airports_df["airport_cd"].tolist(),
        departure_dates=create_dates(date_begin, date_end)
    )
)
jobs.extend(
    create_one_way_jobs(
        departure_airport_cd_list=airports_df["airport_cd"].tolist(),
        arrival_airport_cd_list=['ATL'],
        departure_dates=create_dates(date_begin, date_end)
    )
)

total_jobs = len(jobs)
print(f"[{get_print_time()}] Created {total_jobs} jobs")


# Process jobs
try:
    # Initialize
    db_connection = create_db_connection()
    driver = initialize_driver()

    remove_trip(db_connection, departure_date=date_current)
    session_id = create_session(driver, currency_cd='USD')
    print(f"[{get_print_time()}] Initialized")

    for idx, job in enumerate(jobs, 1):
        print(f"[{get_print_time()}] Job: Processing {idx}/{total_jobs} ({job})")

        attempt = 0
        success = False

        while attempt < max_retry and not success:
            try:
                attempt += 1
                print(f"[{get_print_time()}] Job: Attempt {attempt}/{max_retry}")

                # Remove existing data
                for departure_airport_cd in job["slices"][0]["departure_airport_cds"]:
                    for arrival_airport_cd in job["slices"][0]["arrival_airport_cds"]:
                        remove_trip(db_connection,
                                    departure_airport_cd=departure_airport_cd,
                                    arrival_airport_cd=arrival_airport_cd,
                                    departure_date=job["slices"][0]["departure_date"])

                # Access new data
                url = build_url(**job, session_id=session_id)
                raw_results, access_dt = access_url(driver, url)
                parsed_results = parse_results(job["trip_type"], raw_results, access_dt)

                # Save new data
                results.extend(parsed_results)

                for trip_data in parsed_results:
                    insert_trip(db_connection, trip_data)

                # At success, finish up
                success = True
                time.sleep(1)


            # ---- Exceptions ----
            # *** Exceptions where the job should be skipped ***
            # -- 1. Element not found (such as no flights)
            except NoSuchElementException as e:
                print(f"[{get_print_time()}] Job: NoSuchElementException ({e})")
                success = True
                print(f"[{get_print_time()}] Job: Skipping job")

            # -- 2. Value Error (such as invalid parameters)
            except ValueError as e:
                print(f"[{get_print_time()}] Job: ValueError ({e})")
                success = True
                print(f"[{get_print_time()}] Job: Skipping job")

            # *** Exceptions where job is retried ***
            # -- 1. Invalid or expired session
            except InvalidSessionIdException as e:
                print(f"[{get_print_time()}] Job: InvalidSessionIdException (Invalid or expired session)")

                if attempt < max_retry:
                    print(f"[{get_print_time()}] Job: Retrying in {retry_wait_time} seconds (attempt {attempt}/{max_retry})")
                else:
                    print(f"[{get_print_time()}] Job FAILED: Max retry reached & skipping job in {retry_wait_time} seconds")

                time.sleep(retry_wait_time)
                close_driver(driver)
                driver = initialize_driver()
                session_id = create_session(driver, currency_cd='USD')

            # -- 2. Timeout
            except TimeoutException as e:
                print(f"[{get_print_time()}] Job: TimeoutException {e}")

                if attempt < max_retry:
                    print(f"[{get_print_time()}] Job: Retrying in {retry_wait_time} seconds (attempt {attempt}/{max_retry})")
                else:
                    print(f"[{get_print_time()}] Job FAILED: Max retry reached & skipping job in {retry_wait_time} seconds")

                time.sleep(retry_wait_time)
                close_driver(driver)
                driver = initialize_driver()

            # -- 3. DB Connection Error
            except ConnectionError as e:
                print(f"[{get_print_time()}] Job: ConnectionError {e}")

                if attempt < max_retry:
                    print(f"[{get_print_time()}] Job: Retrying in {retry_wait_time} seconds (attempt {attempt}/{max_retry})")
                else:
                    print(f"[{get_print_time()}] Job FAILED: Max retry reached & skipping job in {retry_wait_time} seconds")

                time.sleep(retry_wait_time)
                db_connection = create_db_connection()

            # -- 3. All other exceptions
            except Exception as e:
                print(f"[{get_print_time()}] Job: {type(e).__name__} {e}")

                if attempt < max_retry:
                    print(f"[{get_print_time()}] Job: Retrying in {retry_wait_time} seconds (attempt {attempt}/{max_retry})")
                else:
                    print(f"[{get_print_time()}] Job FAILED: Max retry reached & skipping job in {retry_wait_time} seconds")

                time.sleep(retry_wait_time)
                close_driver(driver)
                driver = initialize_driver()

except Exception as e:
    print(f"[{get_print_time()}] Driver: {e}")


finally:
    if len(results) == 0:
        print(f"[{get_print_time()}] No results found")
    else:
        save_to_path = f"{PATH}/data/flight/data/{time.strftime('%Y%m%d%H%M%S')}.json"
        pd.DataFrame(results).to_json(save_to_path, orient="records")
        print(f"[{get_print_time()}] Results saved to {save_to_path}")
        print(f"[{get_print_time()}] Scraping Completed. Total Trips: {len(results)}")

    # Close driver
    try:
        close_driver(driver)
        print(f"[{get_print_time()}] Driver closed")

    except Exception as e:
        print(f"[{get_print_time()}] Driver: {e}")

