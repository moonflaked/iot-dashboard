import sqlite3
from contextlib import closing

def get_db_connection(db_file_name):
    conn = sqlite3.connect(db_file_name)
    return conn

def execute_query(db_connection, query):
    with closing(db_connection) as connection:
        with closing(connection.cursor) as cursor:
            cursor.execute(query)

get_db_connection("dashboard.db")
execute_query(
    '''
        CREATE TABLE USER_THRESHOLD (
            USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME VARCHAR NOT NULL,
            THRESHOLD_ID INT NOT NULL,
            MAX_TEMPERATURE_THRESHOLD DECIMAL NOT NULL,
            MAX_HUMIDITY_THRESHOLD DECIMAL NOT NULL,
            MAX_LIGHT_INTENSITY_THRESHOLD INT NOT NULL,
            RFID_TAG_NUMBER TEXT
        );
    '''
)

def insert_user_threshold(conn, user_id, name, threshold_id, max_temperature, max_humidity, max_light_intensity, rfid_tag_number):
    query = f"""
        INSERT INTO USER_THRESHOLD (USER_ID, NAME, THRESHOLD_ID, MAX_TEMPERATURE_THRESHOLD, MAX_HUMIDITY_THRESHOLD, MAX_LIGHT_INTENSITY_THRESHOLD, RFID_TAG_NUMBER) 
        VALUES ({user_id}, '{name}', {threshold_id}, {max_temperature}, {max_humidity}, {max_light_intensity}, '{rfid_tag_number}')
    """
    execute_query(conn, query)

def delete_user_threshold(conn, user_id, threshold_id):
    query = f"""
        DELETE FROM USER_THRESHOLD 
        WHERE USER_ID = {user_id} AND THRESHOLD_ID = {threshold_id}
    """
    execute_query(conn, query) 

def select_user_threshold_by_rfid(conn, rfid_tag_number):
    query = f"""
        SELECT *
        FROM USER_THRESHOLD
        WHERE RFID_TAG_NUMBER = '{rfid_tag_number}'
    """
    result = execute_query(conn, query)
    return result.fetchall()
