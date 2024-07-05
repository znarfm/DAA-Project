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
    num_classes = st.number_input("Number of Classes (Sections):", min_value=1, max_value=8, step=1)
    st.write(f"Selected number of classes: {num_classes}")

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

courses = [
    ["F2F", "COMP 007: Operating Systems"],
    ["F2F", "COMP 008: Data Communications and Networking"],
    ["F2F", "COMP 010: Information Management"],
    ["Online", "COMP 011: Technical Documentation and Presentation Skills in ICT"],
    ["Online", "COSC 203: Design and Analysis of Algorithms"],
    ["Online", "ELEC CS-FE2: BSCS Free Elective 2"],
    ["Online", "GEED 010: People and the Earth's Ecosystem"],
    ["F2F", "PATHFIT 4: Physical Activity Towards Health and Fitness 4"],
    ["Online", "COMP 007: Operating Systems"],
    ["Online", "COMP 008: Data Communications and Networking"],
    ["Online", "COMP 010: Information Management"]
]

# Sort courses to place F2F courses before Online courses
courses.sort(key=lambda x: x[0])

# Function to create and display the initial empty schedule
def create_empty_schedule():
    columns = ["9:00 AM - 12:00 PM", "1:00 PM - 4:00 PM", "4:00 PM - 7:00 PM"]
    empty_data = [["" for _ in columns] for _ in range(48)]
    schedule_df = pd.DataFrame(empty_data, columns=columns)
    return schedule_df

# def place_courses(schedule, courses, course_index=0, start_row=0):
#     # print(start_row)
#     if course_index == len(courses):
#         return True

#     for row in schedule.index[start_row:]:
#         for col in schedule.columns:
#             if schedule.at[row, col] == "":
#                 prof = can_place_course(schedule, courses[course_index], row, col)
#                 if prof:
#                     schedule.at[row, col] = f"{courses[course_index][0]} - {courses[course_index][1]} - {prof}"
#                     if place_courses(schedule, courses, course_index + 1, start_row):
#                         return True
#                     schedule.at[row, col] = ""  # Backtrack
#     return False

def place_courses(schedule, courses, course_index=0, start_row=0):
    if course_index == len(courses):
        return True

    for row in schedule.index[start_row:]:
        for col in schedule.columns:
            if schedule.at[row, col] == "":
                prof = can_place_course(schedule, courses[course_index], row, col)
                if prof == "Skip":
                    continue  # Skip this cell and move to the next
                elif prof:
                    schedule.at[row, col] = f"{courses[course_index][0]} - {courses[course_index][1]} - {prof}"
                    if place_courses(schedule, courses, course_index + 1, start_row):
                        return True
                    schedule.at[row, col] = ""  # Backtrack
    return False

def place_courses_for_sections(schedule, courses):
    section_start_rows = [0, 6, 12, 18, 24, 30, 36, 42]
    for start_row in section_start_rows:
        if not place_courses(schedule, courses, start_row=start_row):
            print(f"Could not place all courses starting from row {start_row}")
            return False
    return True


# def can_place_course(schedule, course, row, col):
#     mode, subject = course
    
#     if mode == "F2F" or mode == "Online":
#         # Check all multiples of -6 in the same column
#         for r in range(row, -1, -6):
#             if schedule.loc[r, col] != "" and (mode in schedule.loc[r, col]):
#                 return False
#         return True
    
#     return True

# def can_place_course(schedule, course, row, col):
#     mode, subject = course
#     # Check if the slot is empty
#     if schedule.at[row, col] != "":
#         return False

#     if mode == "F2F":
#         # Check all multiples of -6 in the same column
#         prof1_found = prof2_found = False
#         for r in range(row, -1, -6):
#             if schedule.loc[r, col] != "" and subject in schedule.loc[r, col]:
#                 if "Prof 1" in schedule.loc[r, col]:
#                     prof1_found = True
#                 elif "Prof 2" in schedule.loc[r, col]:
#                     prof2_found = True
#                 if prof1_found and prof2_found:
#                     return "No Prof"  # If both Prof 1 and Prof 2 are found, return "No Prof"
#         return "Prof 2" if prof1_found else "Prof 1"  # Assign Prof 2 if Prof 1 is found, otherwise Prof 1
#     else:  # Online course
#         # Check if there's an F2F course in the same row (day)
#         for c in schedule.columns:
#             if "F2F" in schedule.loc[row, c]:
#                 return False
#         # Check all multiples of -6 in the same column
#         prof1_found = prof2_found = False
#         for r in range(row, -1, -6):
#             if schedule.loc[r, col] != "" and subject in schedule.loc[r, col]:
#                 if "Prof 1" in schedule.loc[r, col]:
#                     prof1_found = True
#                 elif "Prof 2" in schedule.loc[r, col]:
#                     prof2_found = True
#                 if prof1_found and prof2_found:
#                     return "No Prof"  # If both Prof 1 and Prof 2 are found, return "No Prof"
#         return "Prof 2" if prof1_found else "Prof 1"  # Assign Prof 2 if Prof 1 is found, otherwise Prof 1

def can_place_course(schedule, course, row, col):
    mode, subject = course
    # Check if the slot is empty
    if schedule.at[row, col] != "":
        return False

    if mode == "F2F":
        # Check all multiples of -6 in the same column
        prof1_found = prof2_found = False
        for r in range(row, -1, -6):
            if schedule.loc[r, col] != "" and subject in schedule.loc[r, col]:
                if "Prof 1" in schedule.loc[r, col]:
                    prof1_found = True
                elif "Prof 2" in schedule.loc[r, col]:
                    prof2_found = True
                if prof1_found and prof2_found:
                    return "Skip"  # Indicate to skip this cell if both Prof 1 and Prof 2 are found
        return "Prof 2" if prof1_found else "Prof 1"  # Assign Prof 2 if Prof 1 is found, otherwise Prof 1
    else:  # Online course
        # Check if there's an F2F course in the same row (day)
        for c in schedule.columns:
            if "F2F" in schedule.loc[row, c]:
                return False
        # Check all multiples of -6 in the same column
        prof1_found = prof2_found = False
        for r in range(row, -1, -6):
            if schedule.loc[r, col] != "" and subject in schedule.loc[r, col]:
                if "Prof 1" in schedule.loc[r, col]:
                    prof1_found = True
                elif "Prof 2" in schedule.loc[r, col]:
                    prof2_found = True
                if prof1_found and prof2_found:
                    return "Skip"  # Indicate to skip this cell if both Prof 1 and Prof 2 are found
        return "Prof 2" if prof1_found else "Prof 1"  # Assign Prof 2 if Prof 1 is found, otherwise Prof 1

# Display the schedule DataFrame in sections
# def display_schedule_in_sections(schedule_df):
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     section_ranges = [(0, 6), (6, 12), (12, 18), (18, 24), (24, 30), (30, 36), (36, 42), (42, 48)]
#     for i, (start, end) in enumerate(section_ranges):
#         st.write(f"BSCS 2-{i + 1}")
#         section_df = schedule_df.iloc[start:end].copy()
#         section_df.index = days
#         st.dataframe(section_df)

# Display the schedule DataFrame in sections
def display_schedule_in_sections(schedule_df, num_sections):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    section_ranges = [(i * 6, (i + 1) * 6) for i in range(num_sections)]
    for i, (start, end) in enumerate(section_ranges):
        st.write(f"BSCS 2-{i + 1}")
        section_df = schedule_df.iloc[start:end].copy()
        section_df.index = days
        st.dataframe(section_df)

# Submit button
if st.button("Start Scheduling Algorithm"):
    
    # Clear Table: This can be handled by creating a new empty DataFrame
    schedule_df = create_empty_schedule()

    # Algorithm Proper: Place courses using backtracking
    if place_courses_for_sections(schedule_df, courses):
        st.success("Algorithm Finished")
    else:
        st.error("Unable to place all courses in the schedule")
    display_schedule_in_sections(schedule_df, num_classes)
    st.success("Algorithm Finished")

# Horizontal divider
st.markdown("<hr>", unsafe_allow_html=True)

# Close the SQLite connection
conn.close()
