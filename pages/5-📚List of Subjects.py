import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
    layout="wide",
)

st.header("📚List of Subjects")

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

# Function to fetch existing instructor data
def fetch_subjects_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)

# Fetch existing instructor data
subjects_data = fetch_subjects_data()

st.dataframe(subjects_data)