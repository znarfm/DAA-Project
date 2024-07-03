import streamlit as st
import sqlite3
import pandas as pd

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
            "Meeting_Time TEXT",
            "Number_of_Hours INTEGER",
            "Meeting_Type TEXT"
        ]

        # Placeholder data (can be replaced with actual data)
        data = {
            'Class_Name': [f"BSCS 2-{i}"] * 10,
            'Subjects': ['', '', '', '', '', '', '', '', '', ''],
            'Instructor': ['', '', '', '', '', '', '', '', '', ''],
            'Scheduled_Day': ['', '', '', '', '', '', '', '', '', ''],
            'Meeting_Time': ['', '', '', '', '', '', '', '', '', ''],
            'Number_of_Hours': [3, 2, 3, 2, 3, 2, 2, 3, 3, 3],
            'Meeting_Type': ['F2F', 'Online', 'F2F', 'Online', 'F2F', 'Online', 'F2F', 'Online', 'Online', 'Online']
        }
        schedule_df = pd.DataFrame(data)

        # Clear existing table data
        clear_table_data(conn, table_name)

        # Create or clear table structure
        create_or_clear_table(conn, table_name, columns)

        # Populate table with data
        populate_table(conn, table_name, schedule_df)

# Submit button
if st.button("Start Scheduling Algorithm"):
    # Delete other BSCS tables not selected in num_classes
    delete_other_tables(conn, num_classes)
    
    # Function to create tables
    process_schedule_table(conn, num_classes)

    # Display Empty Schedule
    display_schedules(conn, num_classes)

    # Algorithm Proper

    # Display Final Schedules

    st.success("Algorithm Finished")



# Horizontal divider
st.markdown("<hr>", unsafe_allow_html=True)

# st.title("Schedules:")


# Close the SQLite connection
conn.close()
