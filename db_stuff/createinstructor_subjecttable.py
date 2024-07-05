import sqlite3

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

# Cursor object creation
cursor = conn.cursor()

# Create table for instructors teaching subjects in different classes
create_table_query = '''CREATE TABLE IF NOT EXISTS instructor_subject (
                        id INTEGER PRIMARY KEY,
                        Instructor TEXT,
                        Subject TEXT,
                        Class TEXT
                    )'''

# Execute the query
cursor.execute(create_table_query)

# Commit the transaction
conn.commit()

# Close the SQLite connection
conn.close()

print("Table 'instructor_subject' created successfully and data inserted.")
