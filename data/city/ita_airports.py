from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

airport_df = pd.read_csv('data_processed/airports.csv')
airports = airport_df['airport_cd'].tolist()
airports.extend([char for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'])

airport_list = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    target_url = 'https://matrix.itasoftware.com/search'
    driver.get(target_url)

    wait = WebDriverWait(driver, 10)

    origin_input = wait.until(
        EC.presence_of_element_located((By.ID, 'mat-mdc-chip-list-input-0'))
    )

    for airport in airports:
        print(f"Processing airport code: {airport} ({airports.index(airport) + 1}/{len(airports)})")
        origin_input.click()
        origin_input.send_keys(airport)
        time.sleep(1)

        suggestions_container = wait.until(
            EC.visibility_of_element_located((By.ID, 'mat-autocomplete-0'))
        )

        suggestions = suggestions_container.find_elements(By.TAG_NAME, 'mat-option')

        for suggestion in suggestions:
            text_element = suggestion.find_element(By.CSS_SELECTOR, 'span.mdc-list-item__primary-text')
            text = text_element.text.strip()
            if text:
                # Extract airport code and name
                # The format is: "Airport Name, Country (IATA)"
                # If one , is present, split the string into airport_cd, airport_nm, geo_level_1
                # If two , are present, split the string into airport_cd, airport_nm, geo_level_1, geo_level_2
                if '(' in text and ')' in text:
                    airport_cd = text[text.find('(') + 1:text.find(')')]
                    if len(airport_cd) != 3:
                        continue
                    airport_nm = text[:text.find(',')]
                    geo_level_1 = text[text.find(',') + 1:text.find('(')].strip()
                    if ',' in geo_level_1:
                        geo_level_2 = geo_level_1[:geo_level_1.find(',')]
                        geo_level_1 = geo_level_1[geo_level_1.find(',') + 1:].strip()
                    else:
                        geo_level_2 = None

                    airport_list.append({
                        'airport_cd': airport_cd,
                        'airport_nm': airport_nm,
                        'geo_level_2': geo_level_2,
                        'geo_level_1': geo_level_1
                    })

        # After processing, click on the 'remove' button to clear the input
        try:
            # Press backspace to clear the input
            origin_input.send_keys('\b')
            origin_input.send_keys('\b')
            origin_input.send_keys('\b')
            origin_input.send_keys('\b')
        except Exception as e:
            print(f"Could not remove airport code {airport} from input text box: {e}")

        time.sleep(1)

finally:
    airport_list_df = pd.DataFrame(airport_list)
    airport_list_df.drop_duplicates(inplace=True)
    airport_list_df = airport_list_df.sort_values(by=['airport_cd', 'airport_nm'])
    if not airport_list_df.empty:
        airport_list_df.to_csv('data_processed/ita_airports.csv', index=False)
    else:
        print(f"No suggestions found for airport code: {airport}")

    driver.quit()
