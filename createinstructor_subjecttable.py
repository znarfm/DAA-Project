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

# Sample data to insert into the table
data = [
    ("Santos, Dustin O.", "CS-101: Operating Systems", "BSCS 2-1"),
    ("Santos, Dustin O.", "CS-101: Operating Systems", "BSCS 2-2")
]

# Insert data into the table
insert_query = '''INSERT INTO instructor_subject (Instructor, Subject, Class) VALUES (?, ?, ?)'''

cursor.executemany(insert_query, data)

# Commit the transaction
conn.commit()

# Close the SQLite connection
conn.close()

print("Table 'instructor_subject' created successfully and data inserted.")
