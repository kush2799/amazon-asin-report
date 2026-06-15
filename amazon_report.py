import gspread
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import os
import smtplib
from email.mime.text import MIMEText
from openpyxl import Workbook
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ==================================
# SELLER MAPPING
# ==================================

seller_mapping = {
    "The Pop Market": ("Official", "SMG"),
    "Novus Retail": ("Official", "Bathla")
}

# ==================================
# GOOGLE SHEETS CONNECTION
# ==================================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

spreadsheet = client.open("ASIN_Report")

master_sheet = spreadsheet.worksheet("ASIN_Master")
report_sheet = spreadsheet.worksheet("Report")
# ==================================
# HEADERS
# ==================================
report_sheet.clear()
report_sheet.update(
    "A1:H1",
    [[
        "Date",
        "Partner Type",
        "Official B2B Partner",
        "Store Name",
        "ASIN",
        "Link",
        "Product",
        "Current Selling Price"
    ]]
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.amazon.in/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

# ==================================
# READ ASINS FROM COLUMN E
# ==================================

asins = []

row_num = 2

while True:

    asin = master_sheet.cell(row_num, 1).value

    if not asin:
        break

    asins.append((row_num, asin))

    row_num += 1

# ==================================
# PROCESS
# ==================================

today = datetime.today().strftime("%d/%m/%Y")

for row, asin in asins:

    try:

        url = f"https://www.amazon.in/dp/{asin}"

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print(f"\nProcessing: {asin}")
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")

        if "robot check" in response.text.lower():
            print("ROBOT CHECK DETECTED")

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Product Name

        title = (
            soup.select_one("#productTitle")
            or soup.select_one("span#productTitle")
            or soup.find("h1")
        )

        if title:
            product = title.get_text(strip=True)
        else:
            product = "Not Found"

        print(f"Product: {product}")

        if product == "Not Found":

            filename = f"{asin}.html"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)

            print(f"Saved HTML: {filename}")

        # Price

        price = (
            soup.select_one(".a-price-whole")
            or soup.select_one("span.a-price span.a-offscreen")
        )

        if price:

            current_price = price.get_text(strip=True)

            current_price = (
                current_price
                .replace("₹", "")
                .replace(",", "")
                .replace(".", "")
                .strip()
            )

        else:

            current_price = "Not Found"

        print(f"Price: {current_price}")

        # Seller

        seller = soup.find(id="sellerProfileTriggerId")

        seller_name = (
            seller.get_text(strip=True)
            if seller else "Unknown Seller"
        )

        print(f"Seller: {seller_name}")

        # Mapping

        if seller_name in seller_mapping:

            partner_type, official_partner = seller_mapping[seller_name]

        else:

            partner_type = "Unofficial"
            official_partner = "N/A"

        # Update Sheet

        report_sheet.update_cell(row, 1, today)
        report_sheet.update_cell(row, 2, partner_type)
        report_sheet.update_cell(row, 3, official_partner)
        report_sheet.update_cell(row, 4, seller_name)
        report_sheet.update_cell(row, 5, asin)
        report_sheet.update_cell(row, 6, url)
        report_sheet.update_cell(row, 7, product)
        report_sheet.update_cell(row, 8, current_price)

        print(f"Updated: {asin}")

        time.sleep(2)

    except Exception as e:

        print(f"Error: {asin} - {e}")

print("\nCompleted Successfully")

today_report = datetime.today().strftime("%d-%m-%Y")

excel_file = f"Amazon_ASIN_Report_{today_report}.xlsx"

wb = Workbook()
ws = wb.active

ws.title = "Amazon Report"

all_rows = report_sheet.get_all_values()

for row_data in all_rows:
    ws.append(row_data)

wb.save(excel_file)

print(f"Excel Created: {excel_file}")

# EMAIL REPORT

sender_email = os.environ.get("EMAIL_USER")
sender_password = os.environ.get("EMAIL_PASSWORD")

receiver_email = "v-kushagra.bachhil@realmeindia.com"

subject = f"Amazon ASIN Daily Report - {today_report}"

body = f"""
Hi Kushagra,

Please find attached the Amazon ASIN report for {today}.

Regards,
GitHub Automation
"""

msg = MIMEMultipart()

msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

msg.attach(MIMEText(body, "plain"))

# Attach Excel File
attachment = open(excel_file, "rb")

part = MIMEBase("application", "octet-stream")

part.set_payload(attachment.read())

attachment.close()

encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename={excel_file}"
)

msg.attach(part)
try:

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.sendmail(
        sender_email,
        receiver_email,
        msg.as_string()
    )

    server.quit()

    print("Email with attachment sent successfully")

except Exception as e:

    print(f"Email Error: {e}")
