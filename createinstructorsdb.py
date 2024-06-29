import sqlite3
import pandas as pd

# SQLite database file path
db_file = 'synchllabus_database.db'

# Connect to SQLite database (will create if not exists)
conn = sqlite3.connect(db_file)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS instructor (
                    id INTEGER PRIMARY KEY,
                    Last_name TEXT,
                    First_name TEXT,
                    Middle_initial TEXT,
                    Full_name TEXT,
                    Employment_type TEXT,
                    Work_hours_per_week INTEGER,
                    Days_available TEXT,
                    Free_time INTEGER,
                    No_of_classes INTEGER
                )''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into SQLite database.")
