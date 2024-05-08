import setup_db as db
db.execute_query(
    "dashboard.db",
    '''
        CREATE TABLE USER_THRESHOLD (
            USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME VARCHAR NOT NULL,
            MAX_TEMPERATURE_THRESHOLD DECIMAL NOT NULL,
            MAX_HUMIDITY_THRESHOLD DECIMAL NOT NULL,
            MAX_LIGHT_INTENSITY_THRESHOLD INT NOT NULL,
            RFID_TAG_NUMBER TEXT
        );
    '''
)