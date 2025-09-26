import traceback
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException

from config import Config
from browser_manager import BrowserManager
from appointment_extractor import AppointmentExtractor
from so_appt_nav import SystmOnlineNavigator
from file_manager import FileManager
from email_manager import EmailManager


# Main file to run the SystmOnline GP Appointment Checker
class GPAppointmentChecker:
  def __init__(self):
    self.config = Config()
    self.browser = BrowserManager()
    self.driver = self.browser.driver
    self.extractor = AppointmentExtractor(self.driver)
    self.so_appt_nav = SystmOnlineNavigator(self.driver, self.extractor)
    self.file_manager = FileManager()
    self.email_manager = EmailManager()
    
  def run(self):
    # Skip if out of hours (before 8am or after 6pm) -----------
    hour = datetime.now().hour
    if hour < 8 or hour > 23:  # changed for testing purposes
        print("App is being run outside of configured hours")
        return

    try:
      self.config.validate()
      self.so_appt_nav.login(self.file_manager)
      appt_data = self.so_appt_nav.appointment_navigation()     
      html_table = self.file_manager.save_appointment_data(appt_data)
      self.email_manager.send_email(html_table)
    except Exception as e:
      self.file_manager.log_error(f"General Exception: {str(e)}")
      traceback.print_exc()
    finally:
      self.driver.quit()


if __name__ == "__main__":
    checker = GPAppointmentChecker()
    checker.run()
