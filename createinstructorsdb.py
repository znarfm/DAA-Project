import sqlite3

# SQLite database file path
db_file = 'synchllabus_database.db'

# Connect to SQLite database
conn = sqlite3.connect(db_file)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table with the updated schema
cursor.execute('''CREATE TABLE IF NOT EXISTS instructor (
                    id INTEGER PRIMARY KEY,
                    Last_name TEXT,
                    First_name TEXT,
                    Middle_initial TEXT,
                    Full_name TEXT,
                    Work_hours_per_week INTEGER DEFAULT 40,
                    Free_time INTEGER DEFAULT 40
                )''')

# Transfer data from the old table to the new table
cursor.execute('''INSERT INTO instructor (id, Last_name, First_name, Middle_initial, Full_name, Work_hours_per_week, Free_time)
                  SELECT id, Last_name, First_name, Middle_initial, Full_name, 
                         CASE WHEN Work_hours_per_week IS NULL THEN 40 ELSE Work_hours_per_week END,
                         Free_time
                  FROM instructor''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database schema updated successfully.")
