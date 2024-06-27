import streamlit as st

st.title("DAA Project")

st.write("## Add a new class")

st.text_input("Program")
st.selectbox("Level", ("Freshman", "Sophomore", "Junior", "Senior"))
st.text_input("Class Name")
st.multiselect("Subjects Taught", ("Math", "Science", "History"))

st.button("Submit")