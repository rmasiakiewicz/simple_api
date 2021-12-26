import os.path

from database import Database

if os.path.isfile('./api_database.db'):
    print("Database already existed")
else:
    db = Database()
    db.create_schema()
    db.download_and_save_users_data()
    db.download_and_save_todo_data()
    print("Database created")
