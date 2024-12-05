import json
import base64
import time
import datetime
import copy
from dateutil import parser as date_parser
from urllib.parse import quote, unquote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException
from utils import get_print_time, CHROMEDRIVER_PATH


def decode_base64(str):
    missing_padding = len(str) % 4
    if missing_padding != 0:
        str += "=" * (4 - missing_padding)

    str = base64.b64decode(str).decode('utf-8')

    return str


def encode_base64(str):
    str = base64.b64encode(str.encode('utf-8')).decode('utf-8')
    str = quote(str)

    return str


def extract_json(str):
    try:
        json_start = str.index('{')
        json_end = str.rindex('}') + 1
        json_str = str[json_start:json_end]
        data = json.loads(json_str)
        return data
    except ValueError as ve:
        print("Error locating JSON in the decoded data:", ve)
        return None
    except json.JSONDecodeError as je:
        print("Error parsing JSON:", je)
        return None


def build_url(
    trip_type,
    slices,
    pax_count=1,
    cabin_class='COACH',
    stops=2,
    extra_stops=-1,
    currency_cd=None,
    sales_city_cd=None,
    allow_airport_changes=True,
    session_id=None
):
    # Check trip type
    if trip_type == "one-way":
        if len(slices) != 1:
            raise ValueError("One-way trip must have exactly one slice")
    elif trip_type == "round-trip":
        if len(slices) != 2:
            raise ValueError("Round-trip trip must have exactly two slices")
    elif trip_type == "multi-city":
        if len(slices) < 2:
            raise ValueError("Multi-city trip must have at least two slices")
    else:
        raise ValueError("trip_type must be either 'one-way', 'round-trip', or 'multi-city'")

    # Check if necessary keys are present
    for s in slices:
        if not all(key in s for key in ["departure_airport_cds", "arrival_airport_cds", "departure_date"]):
            raise ValueError(
                "'departure_airport_cds', 'arrival_airport_cds', and 'departure_date' are required parameters for slices")

    # Process slices
    parsed_slices = []

    if trip_type == "one-way":
        routing = "" if "routing" not in slices[0] else slices[0]["routing"]
        ext = "" if "ext" not in slices[0] else slices[0]["ext"]
        departure_date_modifier = "0" if "departure_date_modifier" not in slices[0] else slices[0]["departure_date_modifier"]

        s = {
            "origin": slices[0]["departure_airport_cds"],
            "dest": slices[0]["arrival_airport_cds"],
            "routing": routing,
            "ext": ext,
            "routingRet": "",
            "extRet": "",
            "dates": {
                "searchDateType": "specific",
                "departureDate": slices[0]["departure_date"],
                "departureDateType": "depart",
                "departureDateModifier": departure_date_modifier,
                "departureDatePreferredTimes": [],
                "returnDateType": "depart",
                "returnDateModifier": "",
                "returnDatePreferredTimes": []
            }
        }
        parsed_slices.append(s)

    elif trip_type == "round-trip":
        routing = "" if "routing" not in slices[0] else slices[0]["routing"]
        ext = "" if "ext" not in slices[0] else slices[0]["ext"]
        routing_ret = "" if "routing" not in slices[1] else slices[1]["routing"]
        ext_ret = "" if "ext" not in slices[1] else slices[1]["ext"]
        departure_date_modifier = "0" if "departure_date_modifier" not in slices[0] else slices[0]["departure_date_modifier"]
        return_date_modifier = "0" if "departure_date_modifier" not in slices[1] else slices[1]["departure_date_modifier"]

        s = {
            "origin": slices[0]["departure_airport_cds"],
            "dest": slices[0]["arrival_airport_cds"],
            "routing": routing,
            "ext": ext,
            "routingRet": routing_ret,
            "extRet": ext_ret,
            "dates": {
                "searchDateType": "specific",
                "departureDate": slices[0]["departure_date"],
                "departureDateType": "depart",
                "departureDateModifier": departure_date_modifier,
                "departureDatePreferredTimes": [],
                "returnDate": slices[1]["departure_date"],
                "returnDateType": "depart",
                "returnDateModifier": return_date_modifier,
                "returnDatePreferredTimes": []
            }
        }
        parsed_slices.append(s)

    elif trip_type == "multi-city":
        for s in slices:
            routing = "" if "routing" not in s else s["routing"]
            ext = "" if "ext" not in s else s["ext"]
            departure_date_modifier = "0" if "departure_date_modifier" not in s else s["departure_date_modifier"]

            s = {
                "origin": s["departure_airport_cds"],
                "dest": s["arrival_airport_cds"],
                "routing": routing,
                "ext": ext,
                "dates": {
                    "searchDateType": "specific",
                    "departureDate": s["departure_date"],
                    "departureDateType": "depart",
                    "departureDateModifier": departure_date_modifier,
                    "departureDatePreferredTimes": []
                }
            }
            parsed_slices.append(s)

    search_params = {
        "type": trip_type,
        "slices": parsed_slices,
        "options": {
            "cabin": cabin_class,
            "stops": str(stops),
            "extraStops": str(extra_stops),
            "allowAirportChanges": str(allow_airport_changes).lower(),
            "showOnlyAvailable": "true"
        },
        "pax": {
            "adults": str(pax_count)
        },
        "solution": {
            "sessionId": session_id,
            "Zc": True,
            "Qg": None,
            "ai": None
        }
    }

    if currency_cd:
        search_params["options"]["currency"] = {
            "code": currency_cd
        }

    if sales_city_cd:
        search_params["options"]["salesCity"] = {
            "code": sales_city_cd
        }

    search_params = json.dumps(search_params)
    search_encoded = encode_base64(search_params)
    base_url = "https://matrix.itasoftware.com/flights?search="
    final_url = f"{base_url}{search_encoded}"

    return final_url


def initialize_driver(user_profile=None, is_headless=True):
    print(f"[{get_print_time()}] Initializing Chrome with chromedriver_path={CHROMEDRIVER_PATH}")
    if CHROMEDRIVER_PATH == "":
        service = Service()
    else:
        service = Service(CHROMEDRIVER_PATH)
    options = Options()

    if user_profile:
        options.add_argument(f"--user-data-dir={user_profile}")

    if is_headless:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    options.add_experimental_option("prefs", {})
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    time.sleep(1)
    print(f"[{get_print_time()}] Chrome initialized")

    return driver


def close_driver(driver):
    driver.quit()
    time.sleep(1)
    print(f"[{get_print_time()}] Browser closed")


def clear_browser_cache(driver):
    try:
        driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
        driver.execute_cdp_cmd('Network.clearDataForOrigin', {"origin": "https://matrix.itasoftware.com"})
        driver.execute_cdp_cmd('Network.clearDataForOrigin', {"origin": "https://www.google.com"})
        time.sleep(1)
        print(f"[{get_print_time()}] Browser cache cleared")
    except Exception as e:
        print(f"[{get_print_time()}] Failed to clear cache: {e}")


def open_new_tab(driver):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])


def close_current_tab(driver):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def create_session(driver,
                   currency_cd=None,
                   sales_city_cd=None,
                   timeout=90):
    # Create dummy url to trigger session creation
    departure_date = datetime.datetime.now() + datetime.timedelta(days=10)
    departure_date_str = departure_date.strftime("%Y-%m-%d")

    url = build_url(
        trip_type="one-way",
        slices=[{
            "departure_airport_cds": ['SFO'],
            "arrival_airport_cds": ['LAX'],
            "departure_date": departure_date_str
        }],
        stops=0,
        currency_cd=currency_cd,
        sales_city_cd=sales_city_cd,
    )

    open_new_tab(driver)
    driver.get(url)

    # Wait until the session_id is present in the decoded URL
    start_time = time.time()

    while time.time() - start_time < timeout:
        current_url = driver.current_url
        if "search=" in current_url:
            params_decoded = unquote(current_url).split("search=")[1]
            search_params = decode_base64(params_decoded)
            search_params = json.loads(search_params)

            session_id = search_params['solution'].get('sessionId')

            if session_id:
                close_current_tab(driver)
                print(f"[{get_print_time()}] Session Created: {session_id}")
                return session_id

        time.sleep(1)

    raise TimeoutError("Timed out creating session")


def access_url(driver, url, timeout=60):
    results = []
    access_time = datetime.datetime.now()

    try:
        open_new_tab(driver)
        driver.get(url)
        wait = WebDriverWait(driver, timeout)

        # Wait for sort header to be loaded
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.mat-sort-header-content")
                )
            )

        # When sort header is NOT loaded before timeout
        except TimeoutException:
            try:
                # Check if "No flights found" is present
                no_flights_element = driver.find_element(
                    By.XPATH, "//div[contains(@class, 'matrix-title') and text()='No flights found']"
                )

                # If "No flights found" is present
                if no_flights_element:
                    close_current_tab(driver)
                    raise NoSuchElementException("No flights found")

            # If "No flights found" is NOT present
            except NoSuchElementException:
                close_current_tab(driver)
                raise TimeoutException("Timed out loading time bars")

        time.sleep(1)

        # ---- Results are loaded ----
        # Click to reveal the details of each flight
        flight_rows = driver.find_elements(By.CSS_SELECTOR, "tr.mat-mdc-row")

        for index, row in enumerate(flight_rows):
            try:
                # Check if the row is clickable
                # Exclude: 'detail-row' class
                if "detail-row" not in row.get_attribute("class"):
                    driver.execute_script("arguments[0].scrollIntoView(true);", row)
                    time.sleep(0.35)  # Allow time for scrolling
                    row.click()

            except Exception as e:
                print(f"[{get_print_time()}] Error clicking row {index}: {e}")

        time.sleep(2)

        # ---- Capture network activities ----
        logs = driver.get_log("performance")

        for entry in logs:
            try:
                log = json.loads(entry["message"])["message"]

                if log.get("method") == "Network.responseReceived":
                    # Filter responses
                    response = log.get("params", {}).get("response", {})
                    response_url = response.get("url", "")

                    # Apply filtering based on the response URL
                    if (response_url.startswith("https://content-alkalimatrix-pa.googleapis.com/batch?") and
                        response.get("alternateProtocolUsage", "") != 'unspecifiedReason'):
                        try:
                            request_id = log.get("params", {}).get("requestId", "")
                            response_body = driver.execute_cdp_cmd(
                                "Network.getResponseBody", {"requestId": request_id}
                            )
                            body = response_body.get("body", "")
                            body = decode_base64(body)
                            result_json = extract_json(body)
                            if 'bookingDetails' in result_json:
                                results.append(result_json['bookingDetails'])

                        except Exception as e:
                            print(f"[{get_print_time()}] Failed to get response body for {response_url}\n{e}")
                            continue

            except Exception as e:
                print(f"[{get_print_time()}] Error processing log entry: {e}")
                continue

        close_current_tab(driver)
        print(f"[{get_print_time()}] Captured {len(results)} results")
        return results, access_time

    except Exception as e:
        close_current_tab(driver)

        if "departure time" in str(e).lower():
            raise ValueError("Invalid departure time")

        elif "return time" in str(e).lower():
            raise ValueError("Invalid return time")

        elif "airport" in str(e).lower():
            raise ValueError("Invalid airport code")

        elif "session" in str(e).lower():
            raise InvalidSessionIdException("Invalid or expired session")

        else:
            raise e


def parse_results(trip_type, raw_results, access_dt):
    # Define the templates
    itinerary_template = {
        'access_dt': access_dt.isoformat(),
        'trip_type': trip_type,  # one-way, round-trip, or multi-city
        'trip_departure_date': None, # for fast querying
        'summary': None, # for fast querying
        'price': 0.0,
        'distance': 0,  # miles
        'slices': [],
        'fares': [],
        'taxes': [],
        'notes': [],
    }

    slice_template = {
        'departure_airport_cd': None,
        'arrival_airport_cd': None,
        'stops': 0,
        'duration': 0,  # minutes
        'distance': 0,  # miles
        'segments': [],
        'connections': [],
    }

    segment_template = {
        'airline_cd': None,
        'flight_nb': None,
        'departure_airport_cd': None,
        'arrival_airport_cd': None,
        'departure_dt': None,
        'arrival_dt': None,
        'aircraft': None,
        'cabin': None,
        'booking_class': None,
        'codeshare': False,
        'operated_by': None,
        'duration': 0,  # minutes
    }

    connection_template = {
        'airport_cd': None,
        'duration': 0,  # minutes
        'change_terminal': False,
        'change_airport': False,
    }

    fare_template = {
        'airline_cd': None,
        'departure_city_cd': None,
        'arrival_city_cd': None,
        'fare_cd': None,
        'tag': None,
        'price': None,
    }

    tax_template = {
        'tax_nm': None,
        'tax_cd': None,
        'price': None,
    }

    def parse_price(price):
        try:
            if isinstance(price, str):
                # Remove non-numeric characters except the decimal point
                price = ''.join(char for char in price if char.isdigit() or char == '.')
                return float(price)
            elif isinstance(price, (int, float)):
                return float(price)
            else:
                print(f"Error parsing price: {price}")
                return 0.0
        except (ValueError, AttributeError) as e:
            print(f"Error parsing price: {price} {e}")
            return 0.0

    def parse_datetime(dt_str):
        try:
            dt = date_parser.isoparse(dt_str)
            return dt.isoformat()
        except (ValueError, TypeError):
            return None

    def extract_fares_taxes_notes(ticket):
        fares = []
        taxes = []
        notes = []
        pricings = ticket.get('pricings', [])
        for pricing in pricings:
            # Extract fares
            pricing_fares = pricing.get('fares', [])
            for fare in pricing_fares:
                fare_entry = copy.deepcopy(fare_template)
                fare_entry['airline_cd'] = fare.get('carrier')
                fare_entry['departure_city_cd'] = fare.get('originCity')
                fare_entry['arrival_city_cd'] = fare.get('destinationCity')
                fare_entry['fare_cd'] = fare.get('code')
                fare_entry['tag'] = fare.get('tag')
                fare_entry['price'] = parse_price(fare.get('displayAdjustedPrice'))
                fares.append(fare_entry)

            # Extract taxes
            tax_totals = pricing.get('ext', {}).get('taxTotals', [])
            for tax in tax_totals:
                tax_entry = copy.deepcopy(tax_template)
                tax_entry['tax_cd'] = tax.get('code')
                tax_entry['tax_nm'] = tax.get('tax', {}).get('name')
                tax_entry['price'] = parse_price(tax.get('totalDisplayPrice'))
                taxes.append(tax_entry)

            # Extract notes
            pricing_notes = pricing.get('notes', [])
            notes.extend(pricing_notes)

        return fares, taxes, notes

    parsed_itineraries = []

    for itinerary in raw_results:
        parsed_itinerary = copy.deepcopy(itinerary_template)
        route_segments = []

        # Total Price
        total_price_str = itinerary.get('ext', {}).get('totalPrice', 'USD0.0')
        parsed_itinerary['price'] = parse_price(total_price_str)

        # Distance
        distance_info = itinerary.get('itinerary', {}).get('distance', {})
        if distance_info.get('units') == 'MI':
            parsed_itinerary['distance'] = distance_info.get('value', 0)
        else:
            # Handle other units if necessary
            parsed_itinerary['distance'] = 0

        # Slices
        slices = itinerary.get('itinerary', {}).get('slices', [])
        for slice_item in slices:
            parsed_slice = copy.deepcopy(slice_template)
            # Departure and Arrival Airport Codes
            departure_airport_cd = slice_item.get('origin', {}).get('code')
            arrival_airport_cd = slice_item.get('destination', {}).get('code')
            parsed_slice['departure_airport_cd'] = departure_airport_cd
            parsed_slice['arrival_airport_cd'] = arrival_airport_cd
            route_segments.append(f"{departure_airport_cd}-{arrival_airport_cd}")

            # Stops
            parsed_slice['stops'] = slice_item.get('stopCount', 0)
            # Duration
            departure = slice_item.get('departure')
            arrival = slice_item.get('arrival')
            if departure and arrival:
                try:
                    dep_dt = date_parser.isoparse(departure)
                    arr_dt = date_parser.isoparse(arrival)
                    duration = int((arr_dt - dep_dt).total_seconds() / 60)
                    parsed_slice['duration'] = duration
                except (ValueError, TypeError):
                    parsed_slice['duration'] = 0

            # Segments
            segments = slice_item.get('segments', [])
            for segment in segments:
                parsed_segment = copy.deepcopy(segment_template)
                # Airline Code
                parsed_segment['airline_cd'] = segment.get('carrier', {}).get('code')
                # Flight Number
                parsed_segment['flight_nb'] = segment.get('flight', {}).get('number')
                # Departure and Arrival Airport Codes
                parsed_segment['departure_airport_cd'] = segment.get('origin', {}).get('code')
                parsed_segment['arrival_airport_cd'] = segment.get('destination', {}).get('code')
                # Departure and Arrival Datetimes
                parsed_segment['departure_dt'] = parse_datetime(segment.get('departure'))
                parsed_segment['arrival_dt'] = parse_datetime(segment.get('arrival'))
                # Aircraft
                legs = segment.get('legs', [])
                if legs:
                    parsed_segment['aircraft'] = legs[0].get('aircraft', {}).get('shortName')
                # Cabin and Booking Class
                booking_infos = segment.get('bookingInfos', [])
                if booking_infos:
                    parsed_segment['cabin'] = booking_infos[0].get('cabin')
                    parsed_segment['booking_class'] = booking_infos[0].get('bookingCode')
                # Codeshare
                parsed_segment['codeshare'] = segment.get('codeshare', False)
                # Operated By
                operational_disclosure = segment.get('ext', {}).get('operationalDisclosure', '')
                if operational_disclosure:
                    # Remove 'OPERATED BY ' prefix if present
                    operated_by = operational_disclosure.replace('OPERATED BY ', '').strip()
                    parsed_segment['operated_by'] = operated_by
                # Duration and Distance
                parsed_segment['duration'] = segment.get('duration', 0)

                parsed_slice['segments'].append(parsed_segment)

                # Connections (if any)
                connection_info = segment.get('connection', {})
                if connection_info:
                    parsed_connection = copy.deepcopy(connection_template)
                    parsed_connection['airport_cd'] = segment.get('destination', {}).get('code')
                    parsed_connection['duration'] = connection_info.get('duration', 0)
                    parsed_connection['change_terminal'] = connection_info.get('changeOfTerminal', False)
                    # Assuming change_airport is False unless specified
                    parsed_connection['change_airport'] = False
                    parsed_slice['connections'].append(parsed_connection)

            parsed_itinerary['slices'].append(parsed_slice)

        parsed_itinerary['summary'] = ', '.join(route_segments)
        parsed_itinerary['trip_departure_dt'] = parsed_itinerary['slices'][0]['segments'][0]['departure_dt']

        # Extract fares, taxes, and notes from tickets
        tickets = itinerary.get('tickets', [])
        for ticket in tickets:
            fares, taxes, notes = extract_fares_taxes_notes(ticket)
            parsed_itinerary['fares'].extend(fares)
            parsed_itinerary['taxes'].extend(taxes)
            parsed_itinerary['notes'].extend(notes)

        parsed_itineraries.append(parsed_itinerary)

    return parsed_itineraries