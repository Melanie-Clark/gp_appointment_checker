import traceback
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException

from browser_manager import BrowserManager
from appointment_extractor import AppointmentExtractor
from so_appt_nav import SystmOnlineGPAppointmentNavigator
from file_manager import FileManager
from config import Config


# Main file to run the SystmOnline GP Appointment Checker
class GPAppointmentChecker:
  def __init__(self):
    self.browser = BrowserManager()
    self.driver = self.browser.driver
    self.extractor = AppointmentExtractor(self.driver)
    self.so_appt_nav = SystmOnlineGPAppointmentNavigator(self.driver, self.extractor)
    self.file_manager = FileManager()
    
  def run(self):
    # Skip if out of hours (before 8am or after 6pm) -----------
    hour = datetime.now().hour
    if hour < 8 or hour > 23:  # changed for testing purposes
        print("App is being run outside of configured hours")
        return

    try:
      Config.validate()
      login = self.so_appt_nav.login()
      appt_data = self.so_appt_nav.appointment_navigation()     
      self.file_manager.save_appointment_data(appt_data)
      
    # If no element exists on webpage
    except NoSuchElementException as e:
      if login:
        print("Check username and password. Failed to login")
      else:
        self.file_manager.log_error(str(e))
        traceback.print_exc()
    except Exception as e:
      self.file_manager.log_error(f"General Exception: {str(e)}")
      traceback.print_exc()
    finally:
      self.driver.quit()

if __name__ == "__main__":
    checker = GPAppointmentChecker()
    checker.run()
