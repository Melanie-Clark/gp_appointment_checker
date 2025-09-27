import traceback
from datetime import datetime

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
    self.no_appts = "There are currently no available appointments."
    
  def run(self):
    try:
      # Skip if out of hours (before 8am or after 6pm) -----------
      hour = datetime.now().hour
      if hour < 8 or hour > 18:  # changed for testing purposes
        print("GP Appointment Checker has been run outside of configured hours. Update the hours in main.py or run during configured hours.")
        return
    
      self.config.validate()
      self.so_appt_nav.login(self.file_manager, self.email_manager)
      appt_data = self.so_appt_nav.appointment_navigation()     
      appt_content = self.file_manager.save_appointment_data(appt_data)
      if appt_data == 0:
        self.email_manager.send_email("", self.no_appts, self.no_appts)
      else:
        self.email_manager.send_email(appt_content)
    except Exception as e:
      self.file_manager.log_error(f"General Exception: {str(e)}")
      traceback.print_exc()
    finally:
      self.driver.quit()


if __name__ == "__main__":
    checker = GPAppointmentChecker()
    checker.run()
