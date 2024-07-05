import sqlite3

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

# Cursor object creation
cursor = conn.cursor()

# Define the class names and their respective data
class_data = {
    'BSCS_2_1': [
        ('BSCS 2-1', 'COMP 007: Operating Systems', '', '', '', 3, 'F2F'),
        ('BSCS 2-1', 'COMP 007: Operating Systems', '', '', '', 2, 'Online'),
        ('BSCS 2-1', 'COMP 008: Data Communications and Networking', '', '', '', 3, 'F2F'),
        ('BSCS 2-1', 'COMP 008: Data Communications and Networking', '', '', '', 2, 'Online'),
        ('BSCS 2-1', 'COMP 010: Information Management', '', '', '', 3, 'F2F'),
        ('BSCS 2-1', 'COMP 010: Information Management', '', '', '', 2, 'Online'),
        ('BSCS 2-1', 'PATHFIT 4: Physical Activity Towards Health and Fitness 4', '', '', '', 2, 'F2F'),
        ('BSCS 2-1', 'COMP 011: Technical Documentation and Presentation Skills in ICT', '', '', '', 3, 'Online'),
        ('BSCS 2-1', 'COSC 203: Design and Analysis of Algorithms', '', '', '', 3, 'Online'),
        ('BSCS 2-1', 'ELEC CS-FE2: BSCS Free Elective 2', '', '', '', 3, 'Online'),
        ('BSCS 2-1', 'GEED 010: People and the Earth\'s Ecosystem', '', '', '', 3, 'Online')
    ],
    'BSCS_2_2': [
        ('BSCS 2-2', 'COMP 007: Operating Systems', '', '', '', 3, 'F2F'),
        ('BSCS 2-2', 'COMP 007: Operating Systems', '', '', '', 2, 'Online'),
        ('BSCS 2-2', 'COMP 008: Data Communications and Networking', '', '', '', 3, 'F2F'),
        ('BSCS 2-2', 'COMP 008: Data Communications and Networking', '', '', '', 2, 'Online'),
        ('BSCS 2-2', 'COMP 010: Information Management', '', '', '', 3, 'F2F'),
        ('BSCS 2-2', 'COMP 010: Information Management', '', '', '', 2, 'Online'),
        ('BSCS 2-2', 'PATHFIT 4: Physical Activity Towards Health and Fitness 4', '', '', '', 2, 'F2F'),
        ('BSCS 2-2', 'COMP 011: Technical Documentation and Presentation Skills in ICT', '', '', '', 3, 'Online'),
        ('BSCS 2-2', 'COSC 203: Design and Analysis of Algorithms', '', '', '', 3, 'Online'),
        ('BSCS 2-2', 'ELEC CS-FE2: BSCS Free Elective 2', '', '', '', 3, 'Online'),
        ('BSCS 2-2', 'GEED 010: People and the Earth\'s Ecosystem', '', '', '', 3, 'Online')
    ],
    'BSCS_2_3': [
        ('BSCS 2-3', 'COMP 007: Operating Systems', '', '', '', 3, 'F2F'),
        ('BSCS 2-3', 'COMP 007: Operating Systems', '', '', '', 2, 'Online'),
        ('BSCS 2-3', 'COMP 008: Data Communications and Networking', '', '', '', 3, 'F2F'),
        ('BSCS 2-3', 'COMP 008: Data Communications and Networking', '', '', '', 2, 'Online'),
        ('BSCS 2-3', 'COMP 010: Information Management', '', '', '', 3, 'F2F'),
        ('BSCS 2-3', 'COMP 010: Information Management', '', '', '', 2, 'Online'),
        ('BSCS 2-3', 'PATHFIT 4: Physical Activity Towards Health and Fitness 4', '', '', '', 2, 'F2F'),
        ('BSCS 2-3', 'COMP 011: Technical Documentation and Presentation Skills in ICT', '', '', '', 3, 'Online'),
        ('BSCS 2-3', 'COSC 203: Design and Analysis of Algorithms', '', '', '', 3, 'Online'),
        ('BSCS 2-3', 'ELEC CS-FE2: BSCS Free Elective 2', '', '', '', 3, 'Online'),
        ('BSCS 2-3', 'GEED 010: People and the Earth\'s Ecosystem', '', '', '', 3, 'Online')
    ]
}

# Loop through each class name and create a table and insert data
for class_name, data in class_data.items():
    # Create table with the desired class name
    table_name = f"{class_name}_schedule"

    # SQLite query to create the table
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY,
                            Class_Name TEXT,
                            Subject TEXT,
                            Instructor TEXT,
                            Scheduled_Day TEXT,
                            Meeting_Time TEXT,
                            Number_of_Hours INTEGER,
                            Meeting_Type TEXT
                        )'''

    # Execute the query
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully in SQLite database.")

    # Insert data into the schedule table
    for class_name, subject, instructor, scheduled_day, meeting_time, number_of_hours, meeting_type in data:
        insert_query = f'''INSERT INTO {table_name} (Class_Name, Subject, Instructor, Scheduled_Day, Meeting_Time, Number_of_Hours, Meeting_Type)
                           VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insert_query, (class_name, subject, instructor, scheduled_day, meeting_time, number_of_hours, meeting_type))

    print(f"Data inserted successfully into '{table_name}' table.")

# Commit the transaction
conn.commit()

# Close the SQLite connection
conn.close()
