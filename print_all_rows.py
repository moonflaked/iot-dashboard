import setup_db as db
print(db.select_user_threshold_by_rfid("dashboard.db", "f357b54"))
print(db.select_user_threshold_by_rfid("dashboard.db", "2ca53e4a"))