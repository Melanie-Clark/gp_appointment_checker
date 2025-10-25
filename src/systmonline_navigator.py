import time
from random import randint

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from config import Config


# Navigates from the login screen to the 1st and 2nd available appointments data
class SystmOnlineNavigator:
  def __init__(self, driver, extractor):
    self.driver = driver
    self.extractor = extractor
  
  def login(self, file_manager, email_manager):
    self.driver.get("https://systmonline.tpp-uk.com/")
    time.sleep(1)

    self.driver.find_element(By.NAME, "Username").send_keys(Config.USERNAME)
    self.driver.find_element(By.NAME, "Password").send_keys(Config.PASSWORD)
    self.driver.find_element(By.ID, "button").click()
    time.sleep(randint(1,5))

    # checks for login error
    error_span = self.driver.find_elements(By.ID, "errorText")
    if error_span:
        file_manager.log_error(error_span[0].text.strip())
        self.driver.quit()
        email_manager.send_email("", "There has been a failed login attempt to SystmOnline. Please check your username and password in the .env file", "SystmOnline failed login attempt")
        raise Exception("Failed login attempt. Please check your username and password in the .env file")

  def appointment_navigation(self):
      # print("B: Appt navigation") # DEBUGGING
      appt_status = self.extractor.extract_appointments() # Extracts first date range appointment data (approx. two weeks)
      appt_data = self.other_appointment_date_ranges(appt_status)
      
      # print("Appt status:", appt_status) # DEBUGGING
      # print("Appt data:", appt_data) # DEBUGGING
      
      # No available appointments
      if not appt_data:
          return []
      return appt_data
  
  def click_book_appointment(self):
    visible_button = next(btn for btn in self.driver.find_elements(By.XPATH, "//button[normalize-space(text())='Book Appointment']") if btn.is_displayed())
    visible_button.click()
    # print("A: click book appt") # DEBUGGING
    time.sleep(randint(1,5))

  # Select available appointments for the next set of 2 weeks (approx)  
  def other_appointment_date_ranges(self, appt_data):
    # print("D: Other date ranges") # DEBUGGING
    # return 0 if no appointments
    try:
      select = Select(self.driver.find_element(By.NAME, "StartDate"))
    
      # print(f"Number of date drop-down options: {len(select.options)}")
      for i in range(1,len(select.options)):  
        select.select_by_index(i)
        time.sleep(randint(1,5))

        # Show (appointments) button
        self.driver.find_element(By.ID, "button").click()
        time.sleep(randint(1,5))
        
        # Extracts first two weeks appointment data (approx) excluding headers
        appt_data += self.extractor.extract_appointments()
      
      # print("Extract appt data (C)", appt_data) # DEBUGGING
      
      # Return to first date range
      select = Select(self.driver.find_element(By.NAME, "StartDate"))
      select.select_by_index(0)      
      time.sleep(randint(1, 2))
      self.driver.find_element(By.ID, "button").click()
      time.sleep(randint(1, 2))
      
      # print("D: Return to 2nd half of D: 1st date range re-selected") # DEBUGGING
      return appt_data
    
    except NoSuchElementException:
      # print("E: Other - No element exception") # DEBUGGING
      return []
