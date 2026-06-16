import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Page Config

st.set_page_config(
    page_title="Amazon ASIN Tracker",
    page_icon="📱"
)

st.title("Amazon ASIN Tracker")

# Google Sheets Connection

creds_dict = json.loads(
    st.secrets["GOOGLE_CREDENTIALS"]
)

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

spreadsheet = client.open("ASIN_Report")

report_sheet = spreadsheet.worksheet("Report")
price_history_sheet = spreadsheet.worksheet("Price_History")

# Search Box

asin = st.text_input("Enter ASIN")

if asin:

    data = report_sheet.get_all_records()

    result = None

    for row in data:

        if str(row["ASIN"]).strip() == asin.strip():

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

        st.write("### Price History")

        history_data = price_history_sheet.get_all_values()
        
        for history_row in history_data[1:]:
        
            if history_row[0] == asin:
        
                headers = history_data[0]
        
                for i in range(2, len(headers)):
        
                    if i < len(history_row):
        
                        st.write(
                            f"{headers[i]} : ₹ {history_row[i]}"
                        )
        
                break

    else:

        st.error("ASIN Not Found")
