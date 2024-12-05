import requests
from datetime import datetime
from utils import *

def get_hotel_data(city_cd,
                   dest_id,
                   ci_date,
                   co_date,
                   adults=2,
                   price_min=40,
                   price_max=350):
    results = []

    url = f"https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels?dest_id={dest_id}&search_type=CITY&arrival_date={ci_date}&departure_date={co_date}&adults={adults}&children_age=0&room_qty=1&page_number=1&price_min={price_min}&price_max={price_max}&categories_filter=property_type%3A%3A204&units=metric&temperature_unit=c&languagecode=en-us&currency_code=USD"
    headers = {
        'x-rapidapi-host': BOOKING_COM_API_HOST,
        'x-rapidapi-key': BOOKING_COM_API_KEY
    }

    try:
        response = requests.request("GET", url, headers=headers)
        data = response.json()

        for hotel in data['data']['hotels']:
            hotel_dict = {
                "access_dt": datetime.now().isoformat(),
                "city_cd": city_cd,
                "dest_id": dest_id,
                "hotel_id": hotel['hotel_id'],
                "hotel_nm": hotel['property']['name'],
                "ci_date": ci_date,
                "co_date": co_date,
                "price": hotel['property']['priceBreakdown']['grossPrice']['value'],
                "long": hotel['property']['longitude'],
                "lat": hotel['property']['latitude'],
                "review_score": hotel['property']['reviewScore'],
                "review_count": hotel['property']['reviewCount'],
                "photo_url": hotel['property']['photoUrls'][0],
            }
            results.append(hotel_dict)

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []
