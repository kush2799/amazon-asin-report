import streamlit as st
import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Amazon ASIN Tracker",
    page_icon="📱"
)

st.title("Amazon ASIN Tracker")


# ==========================================
# GOOGLE SHEETS CONNECTION
# ==========================================

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

report_data = report_sheet.get_all_records()

total_asins = len(report_data)

official_count = len([
    row for row in report_data
    if row["Partner Type"] == "Official"
])

unofficial_count = len([
    row for row in report_data
    if row["Partner Type"] == "Unofficial"
])

prices = []

for row in report_data:

    try:
        prices.append(
            float(row["Current Selling Price"])
        )
    except:
        pass

avg_price = (
    sum(prices) / len(prices)
    if prices else 0
)

# ==========================================
# DASHBOARD METRICS
# ==========================================

report_data = report_sheet.get_all_records()

total_asins = len(report_data)

official_count = len([
    row for row in report_data
    if row["Partner Type"] == "Official"
])

unofficial_count = len([
    row for row in report_data
    if row["Partner Type"] == "Unofficial"
])

prices = []

for row in report_data:

    try:

        prices.append(
            float(row["Current Selling Price"])
        )

    except:

        pass

avg_price = (
    sum(prices) / len(prices)
    if prices else 0
)

# ==========================================
# SEARCH
# ==========================================

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

        # ==========================================
        # PRICE HISTORY
        # ==========================================

        st.write("### Price History")

        history_data = price_history_sheet.get_all_values()

        price_data = []

        for history_row in history_data[1:]:

            if history_row[0] == asin:

                headers = history_data[0]

                for i in range(2, len(headers)):

                    if i < len(history_row):

                        st.write(
                            f"{headers[i]} : ₹ {history_row[i]}"
                        )

                        try:

                            price_data.append({
                                "Date": headers[i],
                                "Price": float(history_row[i])
                            })

                        except:

                            pass

                break

        # ==========================================
        # PRICE TREND CHART
        # ==========================================

        if price_data:

            df = pd.DataFrame(price_data)

            st.write("### 📈 Price Trend")

            st.line_chart(
                df.set_index("Date")
            )

    else:

        st.error("ASIN Not Found")
