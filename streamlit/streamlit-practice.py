import streamlit as st

st.title("Streamlit Practice")

name = st.text_input("Enter your name:")

if st.button("Say Hello"):
     if name:
         st.write(f"Hello, {name}! , Hurray! You have successfully run Streamlit.")
     else:
         st.warning("Please enter your name.")