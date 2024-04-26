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
        CREATE TABLE USER(
            USER_ID INT NOT NULL,
            NAME TEXT NOT NULL,
            CONSTRAINT USER_USERID_PK PRIMARY KEY(USER_ID)
        );
        CREATE TABLE THRESHOLD(
            THRESHOLD_ID INT NOT NULL,
            MAX_TEMPERATURE_THRESHOLD DECIMAL(3,1) NOT NULL,
            MAX_HUMIDITY_THRESHOLD DECIMAL(3,1) NOT NULL,
            MAX_LIGHT_INTENSITY_THRESHOLD INT NOT NULL,
            USER_ID INT NOT NULL,
            CONSTRAINT THRESHOLD_USERID_FK FOREIGN KEY REFERENCES
        );
    '''
)

def insert_user(conn, user_id, name):
    query = f"INSERT INTO USER (USER_ID, NAME) VALUES ({user_id}, '{name}')"
    execute_query(conn, query)

def insert_threshold(conn, threshold_id, max_temperature, max_humidity, max_light_intensity, user_id):
    query = f"INSERT INTO THRESHOLD (THRESHOLD_ID, MAX_TEMPERATURE_THRESHOLD, MAX_HUMIDITY_THRESHOLD, MAX_LIGHT_INTENSITY_THRESHOLD, USER_ID) VALUES ({threshold_id}, {max_temperature}, {max_humidity}, {max_light_intensity}, {user_id})"
    execute_query(conn, query)

def delete_user(conn, user_id):
    query = f"DELETE FROM USER WHERE USER_ID = {user_id}"
    execute_query(conn, query)

def delete_threshold(conn, threshold_id):
    query = f"DELETE FROM THRESHOLD WHERE THRESHOLD_ID = {threshold_id}"
    execute_query(conn, query)