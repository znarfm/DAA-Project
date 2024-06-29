import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
)

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

# Function to fetch existing instructor data
def fetch_instructor_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM instructor")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)

# Fetch existing instructor data
instructor_data = fetch_instructor_data()

# Function to fetch subject data
def fetch_subject_data():
    cursor = conn.cursor()
    cursor.execute("SELECT Subject FROM subjects")
    rows = cursor.fetchall()
    return [row[0] for row in rows]

# Form fields
st.header("Add a new instructor")
last_name = st.text_input("Last Name*")
first_name = st.text_input("First Name*")
middle_initial = st.text_input("Middle Initial")

# Concatenate last name, first name, and middle initial
full_name = f"{last_name}, {first_name} {middle_initial}" if middle_initial else f"{last_name}, {first_name}"
emptype = st.selectbox("Employment Type*", ("Full-Time", "Part-Time"))

if emptype == "Part-Time":
    available_days = st.multiselect("Available Days*", ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))
    weekly_hours = st.number_input("Available Hours (Weekly)*", min_value=20, max_value=100)
else:  # Full-Time
    available_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]  # All days selected by default for Full-Time
    weekly_hours = 80  # Fixed weekly hours for Full-Time

# Fetch subject data
subjects = fetch_subject_data()

selected_subjects = st.multiselect("Subjects Taught*", subjects)

# Mark mandatory fields
st.markdown("**required*")

# Submit button
submit_button = st.button("Submit", type="primary")

# If the submit button is pressed
if submit_button:
    # Check if all mandatory fields are filled
    if not first_name or not last_name:
        st.warning("Ensure all mandatory fields are filled.")
    else:
        # Check if instructor already exists in the database
        if full_name in instructor_data["Full_name"].tolist():
            st.warning("This instructor already exists in the database.")
        else:
            # Insert new instructor data into the SQLite table
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO instructor (Last_name, First_name, Middle_initial, Full_name, Employment_type,
                              Work_hours_per_week, Days_available)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (last_name, first_name, middle_initial, full_name, emptype,
                            80 if emptype == "Full-Time" else weekly_hours,
                            ", ".join(available_days) if emptype == "Part-Time" else ", ".join(available_days)))
            
            # Insert subjects taught into instructor_subject table
            for subject in selected_subjects:
                cursor.execute('''INSERT INTO instructor_subject (Instructor, Subject, Class)
                                  VALUES (?, ?, ?)''', (full_name, subject, ""))  # Class can be added later if needed

            conn.commit()
            st.success("Instructor details successfully submitted!")

# Close the SQLite connection
conn.close()
