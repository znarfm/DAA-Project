import sqlite3

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

# Cursor object creation
cursor = conn.cursor()

# Define the class names
class_names = ['BSCS_2_1', 'BSCS_2_2', 'BSCS_2_3']  # Using underscores instead of hyphens

# Loop through each class name and create a table
for class_name in class_names:
    # Create table with the desired class name
    table_name = f"{class_name}_schedule"

    # SQLite query to create the table
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY,
                            Instructor TEXT,
                            Subject TEXT,
                            Scheduled_Day TEXT,
                            Meeting_Time TEXT,
                            Number_of_Hours INTEGER,
                            Meeting_Type TEXT
                        )'''

    # Execute the query
    cursor.execute(create_table_query)

    print(f"Table '{table_name}' created successfully in SQLite database.")

# Commit the transaction
conn.commit()

# Close the SQLite connection
conn.close()
