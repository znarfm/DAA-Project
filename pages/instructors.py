import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Synchllabus",
    page_icon="🗓️",
    layout="wide",
)

st.page_link(page="main.py", label="Home", icon="🏠")

st.header("List of instructors")

# SQLite database file path
db_file = 'synchllabus_database.db'

# Establishing a SQLite connection
conn = sqlite3.connect(db_file)

instructor_data = pd.read_sql_query("SELECT * FROM instructor", conn)

st.dataframe(instructor_data, use_container_width=True, hide_index=True)