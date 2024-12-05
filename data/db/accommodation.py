from utils import *

def initialize_tables(connection):
    # Remove tables if they exist
    drop_query = """
        DROP TABLE IF EXISTS hotels;
    """

    execute_query(connection, drop_query)

    query = """
    -- Table: hotels
    CREATE TABLE hotels (
        id SERIAL PRIMARY KEY,
        access_dt TIMESTAMP NOT NULL,
        city_cd CHAR(3) NOT NULL,
        dest_id INTEGER NOT NULL,
        hotel_id INTEGER NOT NULL,
        hotel_nm TEXT,
        ci_date DATE NOT NULL,
        co_date DATE NOT NULL,
        price NUMERIC(10, 2),
        long DOUBLE PRECISION,
        lat DOUBLE PRECISION,
        review_score NUMERIC(3, 1),
        review_count INTEGER,
        photo_url TEXT
    );
    """

    execute_query(connection, query)
    print(f"[{get_print_time()}] Tables initialized.")


def remove_hotel(connection, city_cd=None, ci_date=None, co_date=None):
    if city_cd is None and ci_date is None and co_date is None:
        return ValueError("At least one of city_cd, ci_date, or co_date must be provided.")
    elif (ci_date is not None and co_date is None) or (ci_date is None and co_date is not None):
        return ValueError("Both ci_date and co_date must be provided.")

    try:
        with connection.cursor() as cursor:
            if city_cd and ci_date and co_date:
                remove_hotel_query = """
                DELETE FROM hotels
                WHERE city_cd = %s AND ci_date = %s AND co_date = %s;
                """
                cursor.execute(remove_hotel_query, (city_cd, ci_date, co_date))

            elif city_cd:
                remove_hotel_query = """
                DELETE FROM hotels
                WHERE city_cd = %s;
                """
                cursor.execute(remove_hotel_query, (city_cd,))

            elif ci_date and co_date:
                remove_hotel_query = """
                DELETE FROM hotels
                WHERE ci_date = %s AND co_date = %s;
                """
                cursor.execute(remove_hotel_query, (ci_date, co_date))

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error removing hotel: {e}")
        raise ConnectionError("Error removing hotel")


def insert_hotel(connection, hotel_data):
    try:
        with connection.cursor() as cursor:
            # Insert into hotels table
            hotel_values = (
                hotel_data['access_dt'],
                hotel_data['city_cd'],
                hotel_data['dest_id'],
                hotel_data['hotel_id'],
                hotel_data['hotel_nm'],
                hotel_data['ci_date'],
                hotel_data['co_date'],
                hotel_data['price'],
                hotel_data['long'],
                hotel_data['lat'],
                hotel_data['review_score'],
                hotel_data['review_count'],
                hotel_data['photo_url']
            )

            insert_hotel_query = """
            INSERT INTO hotels (
                access_dt, city_cd, dest_id, hotel_id, hotel_nm, ci_date, co_date,
                price, long, lat, review_score, review_count, photo_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_hotel_query, hotel_values)

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"[{get_print_time()}] Error inserting hotel: {e}")
        raise ConnectionError("Error inserting hotel")


if __name__ == "__main__":
    connection = create_db_connection()

    try:
        initialize_tables(connection)
    finally:
        close_db_connection(connection)
