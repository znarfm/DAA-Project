import sqlite3

# SQLite database file path
db_file = 'synchllabus_database.db'

# Connect to SQLite database
conn = sqlite3.connect(db_file)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table with the updated schema including columns for each day of the week
cursor.execute('''CREATE TABLE IF NOT EXISTS instructor (
                    id INTEGER PRIMARY KEY,
                    Last_name TEXT,
                    First_name TEXT,
                    Middle_initial TEXT,
                    Full_name TEXT,
                    Work_hours_per_week INTEGER DEFAULT 40,
                    Free_time INTEGER DEFAULT 40,
                    Monday_classes INTEGER DEFAULT 0,
                    Tuesday_classes INTEGER DEFAULT 0,
                    Wednesday_classes INTEGER DEFAULT 0,
                    Thursday_classes INTEGER DEFAULT 0,
                    Friday_classes INTEGER DEFAULT 0,
                    Saturday_classes INTEGER DEFAULT 0
                )''')

# Transfer data from the old table to the new table, including columns for each day
cursor.execute('''INSERT INTO instructor (id, Last_name, First_name, Middle_initial, Full_name, Work_hours_per_week, Free_time,
                                           Monday_classes, Tuesday_classes, Wednesday_classes, Thursday_classes, Friday_classes, Saturday_classes)
                  SELECT id, Last_name, First_name, Middle_initial, Full_name, 
                         COALESCE(Work_hours_per_week, 40) AS Work_hours_per_week,
                         Free_time,
                         Monday_classes,
                         Tuesday_classes,
                         Wednesday_classes,
                         Thursday_classes,
                         Friday_classes,
                         Saturday_classes
                  FROM instructor''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database schema updated successfully.")
