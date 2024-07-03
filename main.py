import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    st.write("## BSCS 2nd Year: 2nd Semester")
    # Editable input for number of classes with constraints
    num_classes = st.number_input("Number of Classes (Section):", min_value=1, max_value=10, step=1)
    st.write(f"Selected number of classes: {num_classes}")

    st.subheader("Section Names")
    for i in range(1, num_classes + 1):
        st.write(f"BSCS 2-{i}")
    
# Function to populate class tables with instructors and subjects
def populate_class_tables():
    # Fetch all data from instructor_subject table
    query = "SELECT Instructor, Subject FROM instructor_subject"
    df_instructor_subject = pd.read_sql(query, conn)

    # List of class tables
    class_tables = ['BSCS_2_1_schedule', 'BSCS_2_2_schedule', 'BSCS_2_3_schedule']

    # Loop through each class table and insert data
    for table_name in class_tables:
        # Drop existing data from the table
        cursor.execute(f'DELETE FROM {table_name}')
        
        # Insert new data into the table
        df_instructor_subject.to_sql(table_name, conn, if_exists='append', index=False)

    # Commit the transaction
    conn.commit()

# Submit button
if st.button("Start Scheduling Algorithm"):
    populate_class_tables()
    st.success("BSCS_2_1_schedule table populated successfully!")

# Function to fetch and display table data
def fetch_and_display_table(table_name):
    # Query to fetch data from the table
    query = f"SELECT * FROM {table_name}"
    
    # Fetch data into DataFrame
    df = pd.read_sql(query, conn)
    
    # Display table
    st.write(f"### {table_name}")
    st.dataframe(df)

# Display all three tables
st.title("Empty Tables")

# Loop through each class name and display its corresponding table
class_names = ['BSCS_2_1_schedule', 'BSCS_2_2_schedule', 'BSCS_2_3_schedule']

for class_name in class_names:
    fetch_and_display_table(class_name)

# Close the SQLite connection
conn.close()
