import streamlit as st
import pandas as pd
import sqlite3

st.header("List of instructors")

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

st.dataframe(instructor_data)