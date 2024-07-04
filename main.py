import streamlit as st
import sqlite3
import pandas as pd
import math

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
    layout="wide",
    # initial_sidebar_state="collapsed",
)

conn = sqlite3.connect("synchllabus_database.db")

st.title("Welcome to Synchlabbus!")
instructor_subject_df = pd.read_sql_query("SELECT Instructor, Subject FROM instructor_subject", conn)

# Layout for displaying the tables side by side
col1, col_spacer, col2 = st.columns([1, 0.1, 1])

with col1:
    st.write("## Instructors and Their Subjects")
    st.dataframe(instructor_subject_df.set_index('Instructor'), # Set 'Instructor' column as index
                 use_container_width=True)  

with col2:
    st.write("# 2nd Year")
    st.write("## 2nd Semester")
    st.write("### BS Computer Science")
    # Editable input for number of classes with constraints
    num_classes = st.number_input("Number of Classes (Sections):", min_value=1, max_value=10, step=1)
    # st.write(f"Selected number of classes: {num_classes}")

    st.subheader("Section Names")
    for i in range(1, num_classes + 1):
        st.write(f"BSCS 2-{i}")

    # st.write("### BS Information Technology")
    

# Function to create or clear existing table
def create_or_clear_table(conn, table_name, columns):
    try:
        c = conn.cursor()
        # Drop the table if it exists
        c.execute(f"DROP TABLE IF EXISTS {table_name};")
        # Create new table
        c.execute(f"CREATE TABLE {table_name} ({', '.join(columns)});")
        conn.commit()
        st.success(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        st.error(f"Error creating or clearing table {table_name}: {e}")

# Function to populate table with data
def populate_table(conn, table_name, data):
    try:
        data.to_sql(table_name, conn, if_exists='append', index=False)
        # st.success(f"Successfully populated data into table {table_name}")
    except sqlite3.Error as e:
        st.error(f"Error populating data into table {table_name}: {e}")

# Function to clear data from table
def clear_table_data(conn, table_name):
    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table_name};")
        conn.commit()
        # st.success(f"Successfully cleared data in table {table_name}")
    except sqlite3.Error as e:
        st.error(f"Error clearing data in table {table_name}: {e}")

# Function to delete all previous BSCS tables
def delete_other_tables(conn, num_classes):
    try:
        c = conn.cursor()
        # Get all existing tables in the database
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        
        # Iterate through each table and drop if it's a BSCS table and not in num_classes
        for table in tables:
            table_name = table[0]
            if table_name.startswith("BSCS_2_") and not any(f"BSCS_2_{i}_schedule" == table_name for i in range(1, num_classes + 1)):
                c.execute(f"DROP TABLE IF EXISTS {table_name};")
                st.success(f"Table '{table_name}' deleted successfully.")
        
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error deleting tables: {e}")

# Function to display schedules for each section
def display_schedules(conn, num_classes):
    st.title("Schedules:")
    st.markdown("<hr>", unsafe_allow_html=True)

    for i in range(1, num_classes + 1):
        table_name = f"BSCS_2_{i}_schedule"
        st.subheader(f"Schedules for BSCS 2-{i}")
        schedule_data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        st.dataframe(schedule_data)

# Function to handle table creation, clearing, and population
def process_schedule_table(conn, num_classes):
    for i in range(1, num_classes + 1):
        table_name = f"BSCS_2_{i}_schedule"
        columns = [
            "Class_Name TEXT",
            "Subjects TEXT",
            "Instructor TEXT",
            "Scheduled_Day TEXT",
            "Meeting_Start TEXT",
            "Meeting_End TEXT",
            "Number_of_Hours INTEGER",
            "Meeting_Type TEXT"
        ]

        # Placeholder data (can be replaced with actual data)
        data = {
            'Class_Name': [f"BSCS 2-{i}"] * 11,
            'Subjects': [
                "COMP 007: Operating Systems",
                "COMP 007: Operating Systems",
                "COMP 008: Data Communications and Networking",
                "COMP 008: Data Communications and Networking",
                "COMP 010: Information Management",
                "COMP 010: Information Management",
                "PATHFIT 4: Physical Activity Towards Health and Fitness 4",
                "COMP 011: Technical Documentation and Presentation Skills in ICT",
                "COSC 203: Design and Analysis of Algorithms",
                "ELEC CS-FE2: BSCS Free Elective 2",
                "GEED 010: People and the Earth's Ecosystem"
            ],
            'Instructor': ['', '', '', '', '', '', '', '', '', '', ''],
            'Scheduled_Day': ['', '', '', '', '', '', '', '', '', '', ''],
            'Meeting_Start': ['', '', '', '', '', '', '', '', '', '', ''],
            'Meeting_End': ['', '', '', '', '', '', '', '', '', '', ''],
            'Number_of_Hours': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'Meeting_Type': ['F2F', 'Online', 'F2F', 'Online', 'F2F', 'Online', 'F2F', 'Online', 'Online', 'Online', 'Online']
        }
        schedule_df = pd.DataFrame(data)

        # Clear existing table data
        clear_table_data(conn, table_name)

        # Create or clear table structure
        create_or_clear_table(conn, table_name, columns)

        # Populate table with data
        populate_table(conn, table_name, schedule_df)

# Function to reset No_of_classes in instructor_subject table
def reset_no_of_classes(conn):
    try:
        c = conn.cursor()
        c.execute("UPDATE instructor_subject SET No_of_classes = 0;")
        conn.commit()
        st.success("No_of_classes reset successfully.")
    except sqlite3.Error as e:
        st.error(f"Error resetting No_of_classes: {e}")

# Function to calculate instructor class threshold
def calculate_instructor_threshold(conn, num_classes):
    try:
        c = conn.cursor()

        # SQL query to calculate number of instructors per subject
        query = """
            SELECT Subject,
                COUNT(DISTINCT Instructor) AS Number_of_Instructors,
                CEIL(:num_classes * 1.0 / COUNT(DISTINCT Instructor)) AS Instructor_Class_Threshold
            FROM instructor_subject
            GROUP BY Subject
        """

        # Execute the query with parameter substitution
        instructor_class_threshold = pd.read_sql_query(query, conn, params={'num_classes': num_classes})

        # Convert Instructor_Class_Threshold to integer
        instructor_class_threshold['Instructor_Class_Threshold'] = instructor_class_threshold['Instructor_Class_Threshold'].astype(int)

        return instructor_class_threshold

    except sqlite3.Error as e:
        st.error(f"Error calculating instructor class threshold: {e}")
        return None

# Function to assign instructors to classes based on subject match and free time availability
def assign_instructors(conn, num_classes):
    try:
        c = conn.cursor()

        # Reset No_of_classes to 0 before assigning instructors
        reset_no_of_classes(conn)

        # Calculate instructor class threshold
        instructor_threshold_df = calculate_instructor_threshold(conn, num_classes)
        instructor_threshold_df.set_index('Subject', inplace=True)
        
    except Exception as e:
        print(f"Error assigning instructors: {e}")


# Submit button
if st.button("Start Scheduling Algorithm"):
    # Delete other BSCS tables not selected in num_classes
    delete_other_tables(conn, num_classes)
    
    # Function to create tables
    process_schedule_table(conn, num_classes)

    # Display Empty Schedule
    # display_schedules(conn, num_classes)

    # Algorithm Proper
    # Assign instructors to all classes
    assign_instructors(conn, num_classes)


    # Display Final Schedules
    display_schedules(conn, num_classes)

    st.success("Algorithm Finished")



# Horizontal divider
st.markdown("<hr>", unsafe_allow_html=True)

# st.title("Schedules:")


# Close the SQLite connection
conn.close()
