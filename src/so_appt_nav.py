import time
from random import randint

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from config import Config


# Navigates from the login screen to the 1st and 2nd available appointments data
class SystmOnlineGPAppointmentNavigator:
  def __init__(self, driver, extractor):
    self.driver = driver
    self.extractor = extractor   
  
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
      initial_appt_data = self.extractor.extract_appointments() # Extracts first two weeks appointment data (approx)
      appt_data = self.other_appointment_date_ranges(initial_appt_data)
      return appt_data

  def click_book_appointment(self):
    # Book Appointment hyperlink
    self.driver.find_element(By.ID, "htmlbut").click()
    time.sleep(randint(1,5))
  
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
      appt_data += self.extractor.extract_appointments()
      
    return appt_data
