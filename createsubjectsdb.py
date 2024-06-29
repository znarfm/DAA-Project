import sqlite3
import pandas as pd

# Provided data
data = {
    "Program": [
        "BS Computer Science", "BS Computer Science", "BS Computer Science",
        "BS Computer Science", "BS Computer Science", "BS Computer Science",
        "BS Computer Science", "BS Computer Science"
    ],
    "Level": [
        "2nd Year", "2nd Year", "2nd Year", "2nd Year",
        "2nd Year", "2nd Year", "2nd Year", "2nd Year"
    ],
    "Subject": [
        "COMP 007: Operating Systems", "COMP 008: Data Communications and Networking",
        "COMP 010: Information Management", "COMP 011: Technical Documentation and Presentation Skills in ICT",
        "COSC 203: Design and Analysis of Algorithms", "ELEC CS-FE2: BSCS Free Elective 2",
        "GEED 010: People and the Earth's Ecosystem", "PATHFIT 4: Physical Activity Towards Health and Fitness 4"
    ],
    "Required_weekly_hours": [5, 5, 5, 3, 3, 3, 3, 2],
    "F2F_hours": [3, 3, 2, 0, 0, 0, 0, 0],
    "Online_hours": [2, 2, 3, 3, 3, 3, 3, 2]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# SQLite database file path
db_file = 'synchllabus_database.db'

# Connect to SQLite database (will create if not exists)
conn = sqlite3.connect(db_file)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY,
                    Program TEXT,
                    Level TEXT,
                    Subject TEXT,
                    Required_weekly_hours INTEGER,
                    F2F_hours INTEGER,
                    Online_hours INTEGER
                )''')

# Convert DataFrame to SQLite table
df.to_sql('subjects', conn, if_exists='append', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into SQLite database.")