import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
    page_title="Amazon ASIN Tracker",
    page_icon="📱"
)

st.title("Amazon ASIN Tracker")

asin = st.text_input("Enter ASIN")

if asin:
    st.write(f"Searching for: {asin}")
