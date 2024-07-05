import sqlite3

# SQLite database file path
db_file = 'synchllabus_database.db'

# Connect to SQLite database
conn = sqlite3.connect(db_file)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Drop the instructor table if it exists
cursor.execute('''DROP TABLE IF EXISTS instructor''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table 'instructor' deleted successfully from SQLite database.")
