import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

spreadsheet = client.open("ASIN_Report")
report_sheet = spreadsheet.worksheet("Report")

st.set_page_config(
    page_title="Amazon ASIN Tracker",
    page_icon="📱"
)

creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

client = gspread.authorize(creds)

st.title("Amazon ASIN Tracker")

asin = st.text_input("Enter ASIN")

if asin:

    data = report_sheet.get_all_records()

    result = None

    for row in data:

        if row["ASIN"] == asin:

            result = row

            break
        if result:

        st.success("ASIN Found")

        st.write("### Product")
        st.write(result["Product"])

        st.write("### Current Price")
        st.write(f"₹ {result['Current Selling Price']}")

        st.write("### Seller")
        st.write(result["Store Name"])

        st.write("### Partner Type")
        st.write(result["Partner Type"])

        st.write("### Official B2B Partner")
        st.write(result["Official B2B Partner"])

    else:

        st.error("ASIN Not Found")
