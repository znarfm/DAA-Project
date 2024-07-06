import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
    layout="wide",
)

st.page_link(page="main.py", label="Home", icon="🏠")

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

# Main Streamlit app
def main():
    # Fetch existing instructor data
    instructor_data = pd.read_sql_query("SELECT * FROM instructor", conn)

    # Fetch subject data
    subjects = pd.read_sql_query("SELECT DISTINCT Subject FROM subjects", conn)

    # Display header
    st.header("Add a new instructor")

    # Create a form
    with st.form(key='new_instructor_form'):
        st.info("All field marked with * are required.")
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
                    cursor.execute('''INSERT INTO instructor (Last_name, First_name, Middle_initial, Full_name)
                                      VALUES (?, ?, ?, ?)''',
                                   (last_name, first_name, middle_initial, full_name))
                    
                    # Insert subjects taught into instructor_subject table
                    for subject in selected_subjects:
                        cursor.execute('''INSERT INTO instructor_subject (Instructor, Subject)
                                          VALUES (?, ?)''', (full_name, subject))
                    conn.commit()
                    st.success("Instructor details successfully submitted!")

    st.divider()
    st.header("Assign Subjects to an existing instructor")
    with st.form("assign_subjects"):

        sel_instructor = st.selectbox("Select Instructor", instructor_data["Full_name"])
        sel_subjects = st.multiselect("Select Subjects", subjects)

        submitted = st.form_submit_button("Assign Subjects")

        if submitted:
            cursor = conn.cursor()
            for subject in sel_subjects:
                # Check if the subject is already assigned to the instructor
                cursor.execute('''SELECT COUNT(*) FROM instructor_subject 
                                WHERE Instructor = ? AND Subject = ?''', (sel_instructor, subject))
                count = cursor.fetchone()[0]

                # Insert only if the subject is not already assigned
                if count == 0:
                    cursor.execute('''INSERT INTO instructor_subject (Instructor, Subject)
                                    VALUES (?, ?)''', (sel_instructor, subject))
                    st.success("Subjects assigned successfully!")
                    conn.commit()
                else:
                    st.warning("Subject already assigned to the selected instructor.")

    # Close the SQLite connection
    conn.close()

# Run the main function
if __name__ == "__main__":
    main()
