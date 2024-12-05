import pandas as pd
import time
import json
from datetime import datetime, timedelta
from data.accommodation.booking_com_scraper import get_hotel_data
from data.db.utils import create_db_connection
from data.db.accommodation import insert_hotel, remove_hotel
from utils import *

results = []
max_retry = 3

dest_df = pd.read_csv(f"{PATH}/data/city/data_processed/booking_com_dest.csv")

date_begin =(datetime.today() + timedelta(days=1))
date_end = (datetime.today() + timedelta(days=100))

db_connection = create_db_connection()

# Clean up past data
date_current = datetime.today().strftime("%Y-%m-%d")
date_yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
date_tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

remove_hotel(db_connection, ci_date=date_yesterday, co_date=date_current)
remove_hotel(db_connection, ci_date=date_current, co_date=date_tomorrow)

for i, row in dest_df.iterrows():
    city_cd = row['city_cd']
    dest_id = row['dest_id']
    current_date = date_begin

    while current_date <= date_end:
        print(f"[{get_print_time()}] Checking {city_cd} on {current_date}")
        ci_date = current_date.strftime("%Y-%m-%d")
        co_date = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        current_date += timedelta(days=1)

        # Clean up outdated data (ready for new data)
        remove_hotel(db_connection, city_cd=city_cd, ci_date=ci_date, co_date=co_date)

        attempt = 0
        while attempt < max_retry:
            attempt += 1
            print(f"[{get_print_time()}] Attempt {attempt}/{max_retry}")

            try:
                hotels = get_hotel_data(city_cd, dest_id, ci_date, co_date, adults=2, price_min=40, price_max=350)
                results.append(hotels)
                for hotel in hotels:
                    insert_hotel(db_connection, hotel)
                break

            except Exception as e:
                print(f"Error: {e}")
                time.sleep(2)
                continue

# Save results as json
with open(f"{PATH}/data/accommodation/data/booking_com_data.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"[{get_print_time()}] Scraping Completed. Total Hotels: {len(results)}")