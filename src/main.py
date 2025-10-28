import time
from datetime import datetime
import traceback

from config import Config
from browser_manager import BrowserManager
from appointment_extractor import AppointmentExtractor
from systmonline_navigator import SystmOnlineNavigator
from table_formatter import TableFormatter
from email_manager import EmailManager
from surgery_info_extractor import SurgeryInfoExtractor


# Main file to run the SystmOnline GP Appointment Checker
class GPAppointmentChecker:
  def __init__(self):
    self.config = Config()
    self.browser = BrowserManager()
    self.driver = self.browser.driver
    self.extractor = AppointmentExtractor(self.driver)
    self.systmonline_navigator = SystmOnlineNavigator(self.driver, self.extractor)
    self.surgery_info = SurgeryInfoExtractor(self.driver)
    self.table_formatter = TableFormatter()
    self.email_manager = EmailManager()
    self.no_appts = "There are currently no available appointments at "
    self.email_content_title = "Here are the available appointments at "
    
  def run(self):
    try:
      # Skip if out of hours (before 8am or after 6pm) -----------
      # It's recommended to check for short periods frequently, or less frequent over a longer time frame
      hour = datetime.now().hour
      start_time = 8 
      end_time = 23
      if hour < start_time or hour > end_time:  # changed for testing purposes
        print("GP Appointment Checker has been run outside of configured hours. Update the hours in main.py or run during configured hours.")
        return
      
      delay_time = 60
    
      self.config.validate()
      self.systmonline_navigator.login(self.email_manager)
      surgery_address = self.surgery_info.extract_address()

      no_appt_text = self.no_appts + surgery_address
      self.systmonline_navigator.click_book_appointment()
      
      while True:
        appt_data = self.systmonline_navigator.appointment_navigation()     
        if appt_data == []:
          self.email_manager.send_email("", no_appt_text, no_appt_text)
        else:
          appt_content = self.table_formatter.table_formatter(appt_data)
          self.email_manager.send_email(appt_content, self.email_content_title + surgery_address)
        hour = datetime.now().hour
        time.sleep(delay_time)
        if hour < start_time or hour > end_time: 
          return False
        
    except Exception as e:
      print(f"ERROR: {e}")
      traceback.print_exc()
    finally:
      self.driver.quit()


if __name__ == "__main__":
    checker = GPAppointmentChecker()
    checker.run()
