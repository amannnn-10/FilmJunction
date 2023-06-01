import streamlit as st

st.title("Movie Recommender System")

option = st.selectbox(
    'How would you like to get contacted',
    ('E-mail', 'Home phone', 'Mobile phone'))
