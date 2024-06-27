import streamlit as st

st.title("DAA Project")

st.write("## Add/Edit a new instructor")
st.text_input("Last Name")
st.text_input("First Name")
st.text_input("Middle Initial")
emptype = st.selectbox("Employment Type", ("Full-Time", "Part-Time"))

if emptype == "Part-Time":
    st.multiselect("Available Days", ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))

st.number_input("Weekly Hours", 0, 100)
st.multiselect("Subjects Taught", ("Math", "Science", "History"))

st.button("Submit")
