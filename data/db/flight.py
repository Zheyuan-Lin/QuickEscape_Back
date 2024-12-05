from psycopg2.extras import execute_values
from datetime import datetime
from utils import *

def initialize_tables(connection):
    # Remove tables if they exist
    drop_query = """
        DROP TABLE IF EXISTS notes, taxes, fares, connections, segments, slices, trips;
    """

    execute_query(connection, drop_query)

    query = """
    -- Table: trips
    CREATE TABLE trips (
        trip_id SERIAL PRIMARY KEY,
        access_dt TIMESTAMP WITH TIME ZONE NOT NULL,
        trip_type VARCHAR(16),
        trip_departure_dt TIMESTAMP WITH TIME ZONE,
        summary VARCHAR(128),
        price NUMERIC(10,2),
        distance INTEGER
    );
    
    -- Table: slices
    CREATE TABLE slices (
        slice_id SERIAL PRIMARY KEY,
        trip_id INTEGER NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        departure_airport_cd CHAR(3), 
        arrival_airport_cd CHAR(3), 
        stops INTEGER,
        duration INTEGER,
        distance INTEGER
    );
    
    -- Table: segments
    CREATE TABLE segments (
        segment_id SERIAL PRIMARY KEY,
        slice_id INTEGER NOT NULL REFERENCES slices(slice_id) ON DELETE CASCADE,
        airline_cd CHAR(2),
        flight_nb INTEGER,
        departure_airport_cd CHAR(3),
        arrival_airport_cd CHAR(3),
        departure_dt TIMESTAMP WITH TIME ZONE,
        arrival_dt TIMESTAMP WITH TIME ZONE,
        aircraft VARCHAR(32),
        cabin VARCHAR(32),
        booking_class VARCHAR(2),
        codeshare BOOLEAN,
        operated_by VARCHAR(64),
        duration INTEGER
    );
    
    -- Table: connections
    CREATE TABLE connections (
        connection_id SERIAL PRIMARY KEY,
        slice_id INTEGER NOT NULL REFERENCES slices(slice_id) ON DELETE CASCADE,
        airport_cd CHAR(3),
        duration INTEGER,
        change_terminal BOOLEAN,
        change_airport BOOLEAN
    );
    
    -- Table: fares
    CREATE TABLE fares (
        fare_id SERIAL PRIMARY KEY,
        trip_id INTEGER NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        airline_cd CHAR(2),
        departure_city_cd CHAR(3),
        arrival_city_cd CHAR(3), 
        fare_cd VARCHAR(10),
        tag VARCHAR(16),
        price NUMERIC(10,2)
    );
    
    -- Table: taxes
    CREATE TABLE taxes (
        tax_id SERIAL PRIMARY KEY,
        trip_id INTEGER NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        tax_nm VARCHAR(128),
        tax_cd VARCHAR(4),
        price NUMERIC(8,2)
    );
    
    -- Table: notes
    CREATE TABLE notes (
        note_id SERIAL PRIMARY KEY,
        trip_id INTEGER NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
        note_text TEXT
    );
    """

    execute_query(connection, query)
    print(f"[{get_print_time()}] Tables initialized.")


def remove_trip(connection, departure_airport_cd=None, arrival_airport_cd=None, departure_date=None):
    if (departure_airport_cd is None and arrival_airport_cd is None) and departure_date is None:
        return ValueError("Departure_airport_cd and arrival_airport_cd or departure_date must be provided.")

    if departure_airport_cd and arrival_airport_cd:
        summary = f"{departure_airport_cd}-{arrival_airport_cd}"

    if departure_date:
        departure_dt = datetime.strptime(departure_date, "%Y-%m-%d")
        departure_dt_lower_str = departure_dt.strftime("%Y-%m-%d 00:00:00")
        departure_dt_upper = departure_dt.strftime("%Y-%m-%d 23:59:59")

    try:
        with connection.cursor() as cursor:
            if departure_airport_cd and arrival_airport_cd and departure_date:
                remove_trip_query = """
                    DELETE FROM trips
                    WHERE summary = %s AND 
                    trip_departure_dt BETWEEN %s AND %s;
                """
                cursor.execute(remove_trip_query, (summary, departure_dt_lower_str, departure_dt_upper))

            elif departure_airport_cd and arrival_airport_cd:
                remove_trip_query = """
                    DELETE FROM trips
                    WHERE summary = %s;
                """
                cursor.execute(remove_trip_query, (summary,))

            elif departure_date:
                remove_trip_query = """
                    DELETE FROM trips
                    WHERE trip_departure_dt BETWEEN %s AND %s;
                """
                cursor.execute(remove_trip_query, (departure_dt_lower_str, departure_dt_upper))

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error removing trip: {e}")
        raise ConnectionError("Error removing trip")


def insert_trip(connection, trip_data):
    try:
        with connection.cursor() as cursor:
            # Insert into trips table
            insert_trip_query = """
                INSERT INTO trips (access_dt, trip_type, trip_departure_dt, summary, price, distance)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING trip_id;
            """
            cursor.execute(insert_trip_query, (
                trip_data['access_dt'],
                trip_data['trip_type'],
                trip_data.get('trip_departure_dt'),  # Can be None
                trip_data['summary'],
                trip_data['price'],
                trip_data['distance']
            ))
            trip_id = cursor.fetchone()[0]

            # Insert into slices table
            for slice_data in trip_data.get('slices', []):
                insert_slice_query = """
                    INSERT INTO slices (trip_id, departure_airport_cd, arrival_airport_cd, stops, duration, distance)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING slice_id;
                """
                cursor.execute(insert_slice_query, (
                    trip_id,
                    slice_data['departure_airport_cd'],
                    slice_data['arrival_airport_cd'],
                    slice_data['stops'],
                    slice_data['duration'],
                    slice_data['distance']
                ))
                slice_id = cursor.fetchone()[0]

                # Insert into segments table
                segments = slice_data.get('segments', [])
                if segments:
                    segment_values = [
                        (
                            slice_id,
                            segment['airline_cd'],
                            segment['flight_nb'],
                            segment['departure_airport_cd'],
                            segment['arrival_airport_cd'],
                            segment['departure_dt'],
                            segment['arrival_dt'],
                            segment['aircraft'],
                            segment['cabin'],
                            segment['booking_class'],
                            segment['codeshare'],
                            segment['operated_by'],
                            segment['duration']
                        )
                        for segment in segments
                    ]
                    insert_segments_query = """
                        INSERT INTO segments (
                            slice_id, airline_cd, flight_nb, departure_airport_cd, arrival_airport_cd,
                            departure_dt, arrival_dt, aircraft, cabin, booking_class, codeshare, operated_by, duration
                        )
                        VALUES %s;
                    """
                    execute_values(cursor, insert_segments_query, segment_values)

                # Insert into connections table
                connections = slice_data.get('connections', [])
                if connections:
                    connection_values = [
                        (
                            slice_id,
                            connection['airport_cd'],
                            connection['duration'],
                            connection['change_terminal'],
                            connection['change_airport']
                        )
                        for connection in connections
                    ]
                    insert_connections_query = """
                        INSERT INTO connections (slice_id, airport_cd, duration, change_terminal, change_airport)
                        VALUES %s;
                    """
                    execute_values(cursor, insert_connections_query, connection_values)

            # Insert into fares table
            fares = trip_data.get('fares', [])
            if fares:
                fare_values = [
                    (
                        trip_id,
                        fare['airline_cd'],
                        fare['departure_city_cd'],
                        fare['arrival_city_cd'],
                        fare['fare_cd'],
                        fare['tag'],
                        fare['price']
                    )
                    for fare in fares
                ]
                insert_fares_query = """
                    INSERT INTO fares (trip_id, airline_cd, departure_city_cd, arrival_city_cd, fare_cd, tag, price)
                    VALUES %s;
                """
                execute_values(cursor, insert_fares_query, fare_values)

            # Insert into taxes table
            taxes = trip_data.get('taxes', [])
            if taxes:
                tax_values = [
                    (
                        trip_id,
                        tax['tax_nm'],
                        tax['tax_cd'],
                        tax['price']
                    )
                    for tax in taxes
                ]
                insert_taxes_query = """
                    INSERT INTO taxes (trip_id, tax_nm, tax_cd, price)
                    VALUES %s;
                """
                execute_values(cursor, insert_taxes_query, tax_values)

            # Insert into notes table
            notes = trip_data.get('notes', [])
            if notes:
                note_values = [
                    (
                        trip_id,
                        note_text
                    )
                    for note_text in notes
                ]
                insert_notes_query = """
                    INSERT INTO notes (trip_id, note_text)
                    VALUES %s;
                """
                execute_values(cursor, insert_notes_query, note_values)

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error inserting trip: {e}")
        raise ConnectionError("Error inserting trip")


if __name__ == "__main__":
    connection = create_db_connection()

    try:
        initialize_tables(connection)
    finally:
        close_db_connection(connection)
