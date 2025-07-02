import time
from datetime import datetime
from random import randint

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate

from config import Config


class GPAppointmentChecker:
  def __init__(self):
        self.driver = self.chromedriver() 
  
  @staticmethod
  def chromedriver():
    # Chrome headless config
    chrome_options = Options()

    # chrome_options.add_argument("--headless=new") # Chrome runs in background

    # Disables the Chrome sandbox security feature.
    # This is often necessary in some restricted environments or containerised setups, or to avoid errors on macOS when running ChromeDriver
    chrome_options.add_argument("--no-sandbox")

    # Uses the /tmp directory instead of /dev/shm for shared memory
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Launches Chrome using Selenium’s Chrome WebDriver
    return webdriver.Chrome(options=chrome_options)
  
  def login(self):
    self.driver.get("https://systmonline.tpp-uk.com/")
    time.sleep(1)

    self.driver.find_element(By.NAME, "Username").send_keys(Config.USERNAME)
    self.driver.find_element(By.NAME, "Password").send_keys(Config.PASSWORD)
    self.driver.find_element(By.ID, "button").click()
    time.sleep(randint(1,5))
    return "login"
  
  def appointment_navigation(self):
      self.click_book_appointment()
      initial_appt_data = self.extract_appointments() # Extracts first two weeks appointment data (approx)
      appt_data = self.other_appointment_date_ranges(initial_appt_data)
      return appt_data

  def click_book_appointment(self):
    # Book Appointment hyperlink
    self.driver.find_element(By.ID, "htmlbut").click()
    time.sleep(randint(1,5))
          
  def extract_appointments(self):
    # Find the table names for each table
    # tables = driver.find_elements(By.TAG_NAME, "table")
    # for i, table in enumerate(tables):
    #     print(f"Table {i}:")
    #     print(table.text)
    #     print("-" * 20)

    # Appointments table
    tables = self.driver.find_elements(By.TAG_NAME, "table")
    appt_table = tables[5]
          
    # Extract table rows
    rows = appt_table.find_elements(By.TAG_NAME, "tr")
    
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "th") or row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text.strip() for cell in cells]
        row_data = row_data[:-1] # Remove last column
        data.append(row_data)
    
    return data

  def other_appointment_date_ranges(self, appt_data):
    # Select available appointments for the next set of 2 weeks (approx)
    select = Select(self.driver.find_element(By.NAME, "StartDate"))
    
    # print(f"Number of date drop-down options: {len(select.options)}")
    for i in range(1,len(select.options)):  
      select.select_by_index(i)
      time.sleep(randint(1,5))

      # Show (appointments) button
      self.driver.find_element(By.ID, "button").click()
      time.sleep(randint(1,5))
      
      # Extracts first two weeks appointment data (approx) excluding headers
      appt_data += self.extract_appointments()[1:]
      
    return appt_data
  
  def save_appointment_data(self, appt_data):
    # Separate headers and body
    # print(data_first)
    headers = appt_data[0]
    rows = appt_data[1:]

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # format table (showindex - removes row index numbers)
    formatted_table = (tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    print(formatted_table)

    with open(Config.APPT_FILE, 'w') as file:
      file.write(formatted_table)
    
  # Error log (append)
  def log_error(self, msg):
      with open(Config.LOG_FILE, 'a') as f:
          f.write(f"[{datetime.now()}] {msg}\n")

  def run(self):
    # Skip if out of hours (before 8am or after 6pm) -----------
    hour = datetime.now().hour
    if hour < 8 or hour > 24:  # changed for testing purposes
        print("App is being run outside of configured hours")
        return

    try:
      Config.validate()
      login = self.login()
      appt_data = self.appointment_navigation()     
      self.save_appointment_data(appt_data)
      
    # If no element exists on webpage
    except NoSuchElementException as e:
      if login:
        print("Check username and password. Failed to login")
      else:
        self.log_error(str(e))
        print(f"Error: {e}")
    except Exception as e:
      self.log_error(f"General Exception: {str(e)}")
      print(f"Unexpected error: {e}")
    finally:
      self.driver.quit()

if __name__ == "__main__":
    checker = GPAppointmentChecker()
    checker.run()
