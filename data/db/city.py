from utils import *
import pandas as pd

def initialize_tables(connection):
    # Remove tables if they exist
    drop_query = """
        DROP TABLE IF EXISTS airports;
        DROP TABLE IF EXISTS airlines;
    """

    execute_query(connection, drop_query)

    query = """
    -- Table: airports
    CREATE TABLE IF NOT EXISTS airports (
        airport_cd CHAR(3),
        airport_nm TEXT,
        city_nm TEXT,
        city_cd CHAR(3),
        country_cd CHAR(2),
        region_cd VARCHAR(10),
        timezone TEXT,
        latitude NUMERIC,
        longitude NUMERIC,
        attributes TEXT
    );
    
    -- Table: airlines
    CREATE TABLE IF NOT EXISTS airlines (
        airline_nm TEXT,
        airline_cd CHAR(2),
        icao_cd CHAR(3),
        country_nm TEXT
    );
    """

    execute_query(connection, query)
    print(f"[{get_print_time()}] Tables initialized.")

def upload_airport(connection, airport_data):
    try:
        with connection.cursor() as cursor:
            # Insert into hotels table
            airport_values = (
                airport_data["airport_cd"],
                airport_data["airport_nm"],
                airport_data["city_nm"],
                airport_data["city_cd"],
                airport_data["country_cd"],
                airport_data["region_cd"],
                airport_data["timezone"],
                airport_data["latitude"],
                airport_data["longitude"],
                airport_data["attributes"]
            )

            insert_airport_query = """
            INSERT INTO airports (airport_cd, airport_nm, city_nm, city_cd, country_cd, region_cd, timezone, latitude, longitude, attributes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_airport_query, airport_values)

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error inserting airport: {e}")
        raise ConnectionError("Error inserting airport")


def upload_airline(connection, airline_data):
    try:
        with connection.cursor() as cursor:
            # Insert into hotels table
            airline_values = (
                airline_data["airline_nm"],
                airline_data["airline_cd"],
                airline_data["icao_cd"],
                airline_data["country_nm"]
            )

            insert_airline_query = """
            INSERT INTO airlines (airline_nm, airline_cd, icao_cd, country_nm)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_airline_query, airline_values)

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error inserting airline: {e}")
        raise ConnectionError("Error inserting airline")


if __name__ == "__main__":
    connection = create_db_connection()

    try:
        initialize_tables(connection)
        airports_df = pd.read_csv("../city/data_processed/airports.csv")
        for i, row in airports_df.iterrows():
            upload_airport(connection, row)
        print(f"[{get_print_time()}] Airport data uploaded")

        airlines_df = pd.read_csv("../city/data_processed/airlines.csv")
        for i, row in airlines_df.iterrows():
            upload_airline(connection, row)
        print(f"[{get_print_time()}] Airline data uploaded")

    finally:
        close_db_connection(connection)
