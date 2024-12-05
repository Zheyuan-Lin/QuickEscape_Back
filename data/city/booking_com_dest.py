import requests
import pandas as pd
from utils import *

df = pd.read_csv(f"{PATH}/data/city/data_processed/airports.csv")
cities = df["city_cd"].unique()

dest_list = []

for city in cities:
    print(f"Processing {city}...")
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    querystring = {"query": city}
    headers = {
        'x-rapidapi-host': BOOKING_COM_API_HOST,
        'x-rapidapi-key': BOOKING_COM_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    # Select the first response has 'type' == 'city'
    dest_pick = None

    for dest in data["data"]:
        if dest["search_type"] == "city":
            dest_pick = dest
            break

    if dest_pick is None:
        print(f"City {city} not found. Using the first match.")
        dest_pick = data["data"][0]

    dest_list.append({
        "city_cd": city,
        "dest_id": dest_pick["dest_id"],
        "dest_name": dest_pick["name"],
        "dest_lat": dest_pick["latitude"],
        "dest_lon": dest_pick["longitude"],
        "image_url": dest_pick["image_url"] if "image_url" in dest_pick else ''
    })

dest_df = pd.DataFrame(dest_list)
dest_df.to_csv(f"{PATH}/data/city/data_processed/booking_com_dest.csv", index=False)

