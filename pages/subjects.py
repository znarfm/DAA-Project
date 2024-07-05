import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
    layout="wide",
)

st.page_link(page="main.py", label="Home", icon="🏠")

st.header("📚List of Subjects")

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

subjects_data = pd.read_sql_query("SELECT * FROM subjects", conn)

st.dataframe(subjects_data, use_container_width=True, hide_index=True)
