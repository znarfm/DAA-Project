import streamlit as st
import pandas as pd
import sqlite3

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

# Function to fetch subject data
def fetch_subject_data():
    cursor = conn.cursor()
    cursor.execute("SELECT Subject FROM subjects")
    rows = cursor.fetchall()
    return [row[0] for row in rows]

# Main Streamlit app
def main():
    # Fetch existing instructor data
    instructor_data = fetch_instructor_data()

    # Fetch subject data
    subjects = fetch_subject_data()

    # Display header
    st.header("Add a new instructor")

    # Create a form
    with st.form(key='new_instructor_form'):
        # Form fields
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            last_name = st.text_input("Last Name*", key='last_name')
        with col2:
            first_name = st.text_input("First Name*", key='first_name')
        with col3:
            middle_initial = st.text_input("Middle Initial", key='middle_initial')

        # Concatenate last name, first name, and middle initial
        full_name = f"{last_name}, {first_name} {middle_initial}" if middle_initial else f"{last_name}, {first_name}"

        # Mark mandatory fields
        st.markdown("**required**")

        selected_subjects = st.multiselect("Subjects Taught*", subjects, key='selected_subjects')

        # Submit button within the form
        submitted = st.form_submit_button("Submit")

        # If the form is submitted
        if submitted:
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
                    cursor.execute('''INSERT INTO instructor (Last_name, First_name, Middle_initial, Full_name, Work_hours_per_week, Free_time)
                                      VALUES (?, ?, ?, ?, 40, 40)''',  # Default work hours set to 40, Free_time set to 0 by default
                                   (last_name, first_name, middle_initial, full_name))
                    
                    # Insert subjects taught into instructor_subject table
                    for subject in selected_subjects:
                        cursor.execute('''INSERT INTO instructor_subject (Instructor, Subject, Class)
                                          VALUES (?, ?, ?)''', (full_name, subject, ""))  # Class can be added later if needed

                    conn.commit()
                    st.success("Instructor details successfully submitted!")

    # Close the SQLite connection
    conn.close()

# Run the main function
if __name__ == "__main__":
    main()
