import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# ------ CONFIGURATION ------

USERNAME = 'username'
PASSWORD = 'password'

EMAIL_FROM = 'from email'
EMAIL_TO = 'to email'
EMAIL_SUBJECT = '🩺 New GP Appointment Available!'
EMAIL_PASSWORD = 'app password'

APPT_FILE = '/tmp/last_appointments.txt'
LOG_FILE = '/tmp/systm_log.err'

# Skip if out of hours (before 8am or after 6pm) -----------
hour = datetime.now().hour
if hour < 8 or hour > 21:  # 21 for testing purposes
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



        # Add available appointments 6 week list, if none...no entry



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
        print(appt_data)

        # remove additional View lines
        # align headers



    except Exception as e:
        log_error(str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
