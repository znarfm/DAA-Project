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
    num_classes = st.number_input("Number of Classes (Sections):", min_value=1, max_value=6, step=1)
    # st.write(f"Selected number of classes: {num_classes}")

    st.subheader("Section Names")
    for i in range(1, num_classes + 1):
        st.write(f"BSCS 2-{i}")

    # st.write("### BS Information Technology")

# Function to fetch data from SQLite database
def fetch_subject_data():
    conn = sqlite3.connect('synchllabus_database.db')
    c = conn.cursor()
    c.execute("SELECT Meeting_type, Subject FROM subjects")
    rows = c.fetchall()
    c.close()
    conn.close()
    return rows

def show_subject_data():
    rows = fetch_subject_data()
    
    # Convert fetched data into a DataFrame
    df = pd.DataFrame(rows, columns=['Meeting_type', 'Subject'])
    
    # Display data using Streamlit
    st.title('Meeting Type and Subject Data')
    st.dataframe(df)


# Submit button
if st.button("Start Scheduling Algorithm"):
    show_subject_data();
    
    # Clear Table
    
    # Function to create tables

    # Display Empty Schedule

    # Algorithm Proper


    # Display Final Schedules

    st.success("Algorithm Finished")



# Horizontal divider
st.markdown("<hr>", unsafe_allow_html=True)

# st.title("Schedules:")


# Close the SQLite connection
conn.close()
