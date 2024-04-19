import sqlite3
from contextlib import closing

def get_db_connection(db_file_name):
    conn = sqlite3.connect(db_file_name)
    return conn

def execute_query(db_connection, query):
    with closing(get_db_connection("dashboard.db")) as connection:
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
