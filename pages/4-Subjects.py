# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1HrokIWU955H19G-24cIgiYkLyDz9N64JeVAIEGKtrrs/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url)
st.dataframe(data)