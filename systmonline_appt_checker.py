import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import pandas as pd
from tabulate import tabulate

# ------ CONFIGURATION --------

load_dotenv(override=True)  # loads variables from .env file

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

EMAIL_SUBJECT = '🩺 New GP Appointment Available!'

APPT_FILE = '/tmp/last_appointments.txt'
LOG_FILE = '/tmp/systm_log.err'

# Skip if out of hours (before 8am or after 6pm) -----------
hour = datetime.now().hour
if hour < 8 or hour > 24:  # changed for testing purposes
    print("App is being run outside of configured hours")
    exit(0)

# Chrome headless config
chrome_options = Options()

# chrome_options.add_argument("--headless") # Chrome runs in background

# Disables the Chrome sandbox security feature.
# This is often necessary in some restricted environments or containerised setups, or to avoid errors on macOS when running ChromeDriver
chrome_options.add_argument("--no-sandbox")

# Uses the /tmp directory instead of /dev/shm for shared memory
chrome_options.add_argument("--disable-dev-shm-usage")

# Launches Chrome using Selenium’s Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Error log (append)
def log_error(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def main():
    try:
        driver.get("https://systmonline.tpp-uk.com/")
        time.sleep(1)

        # Completes login screen
        driver.find_element(By.NAME, "Username").send_keys(USERNAME)
        driver.find_element(By.NAME, "Password").send_keys(PASSWORD)
        driver.find_element(By.ID, "button").click()
        time.sleep(1)

        # Book Appointment hyperlink
        driver.find_element(By.ID, "htmlbut").click()
        time.sleep(1)

        # Select available weeks for the next 3 weeks - TBC
        driver.find_element(By.ID, "button").click()
        time.sleep(1)



        # ----------- Add 1st 3 week available appointments to a complete 6 week list, if no appts...no entry--------------------



        # Select available weeks for 3-6 weeks - TBC
        select = Select(driver.find_element(By.NAME, "StartDate"))
        select.select_by_index(1)
        time.sleep(1)

        # Show (appointments) button
        driver.find_element(By.ID, "button").click()
        time.sleep(1)

        # Used to find the table names for each table
        # tables = driver.find_elements(By.TAG_NAME, "table")
        # for i, table in enumerate(tables):
        #     print(f"Table {i}:")
        #     print(table.text)
        #     print("-" * 20)

        # Appointments table
        tables = driver.find_elements(By.TAG_NAME, "table")
        appt_table = tables[5]
        appt_data = appt_table.text.strip()
        # print(appt_data)

        # Extract table rows
        rows = appt_table.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "th") or row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text.strip() for cell in cells]

            # Remove last column
            row_data = row_data[:-1]
            data.append(row_data)

        # Separate headers and body
        headers = data[0]
        rows = data[1:]

        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)

        # format table to remove row index numbers
        # df_formatted = df.to_string(index=False)
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

    except Exception as e:
        log_error(str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
