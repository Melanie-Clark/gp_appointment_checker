import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unittest.mock import MagicMock
from systmonline_navigator import SystmOnlineNavigator


class TestSystmOnlineNavigator(unittest.TestCase):
  def setUp(self):
    """
    This runs before every test, avoiding object creation repeition in each test - creates fresh mock objects for the 
    driver, file_manager, and email_manager to isolate tests from real browser or emails.
    """
    self.mock_driver = MagicMock()         # MagicMock fakes the driver
    self.file_manager = MagicMock()
    self.email_manager = MagicMock()      # Prevents live e-mails being sent
    self.mock_extractor = MagicMock()
    self.navigator = SystmOnlineNavigator(self.mock_driver, self.mock_extractor)

  # ---------------LOGIN----------------------
  # Test wrong username/password - failed login
  def test_login_failure(self):
    # Fakes the HTML element that would appear on login failure
    error_element = MagicMock() 
    # Login just checks if error_span exists, not the actual text - error_span[0].text.strip()
    # MagicMock needs a .text attribute (any text) to avoid errors
    error_element.text = "Invalid username or password"

    # Mock Selenium driver.find_elements(By.ID, "errorText") - check if the login function thinks a failed login element exists
    self.mock_driver.find_elements.return_value = [error_element]

    # Expect an exception - raise Exception("Failed login attempt...") because the login “failed”
    with self.assertRaises(Exception) as context:
        self.navigator.login(self.file_manager, self.email_manager)

    # Confirms the exception message is as expected - test passes
    self.assertIn("Failed login attempt", str(context.exception))

  # Test correct username/password - successful login
  def test_login_successful(self):
    # Mock Selenium driver.find_elements(By.ID, "errorText") - check the login function thinks a successful login element exists
    self.mock_driver.find_elements.return_value = []

    try:
      # Run the login function. If login() runs without raising an exception => success.
      self.navigator.login(self.file_manager, self.email_manager)
    except Exception as e:
      # Fail the test if ANY exception is raised
      self.fail(f"login() raised an unexpected exception: {e}")

  # ---------------BOOK APPOINTMENTS----------------------
  # Simulates no visible 'Book Appointment' button
  def test_click_book_appointment_no_visible_button(self):
    self.mock_driver.find_elements.return_value = []

    # If there’s no visible button, next() will automatically raise StopIteration
    with self.assertRaises(StopIteration):
        self.navigator.click_book_appointment()

  # Simulating visible click book appointment
  def test_click_book_appointment_success(self):
    mock_button = MagicMock()
    mock_button.is_displayed.return_value = True
    self.mock_driver.find_elements.return_value = [mock_button]

    # This should run without errors
    self.navigator.click_book_appointment()
    # Verify click() was called on the button
    mock_button.click.assert_called_once()
    
  # ---------------APPOINTMENT NAVIGATION----------------------
  # mock appointments for appointment_navigation() tests
  @staticmethod
  def _mock_appointments(date1="Saturday 25th Oct 2025", date2 = "Thursday 30th Oct 2025"):
    return [
      {"Date": date1, "Earliest Time": "17:00", "Latest Time": "17:00", "Location": "Test location", "Clinician": "Dr. Smith", "Session Type": "Test session"},
      {"Date": date2, "Earliest Time": "18:05", "Latest Time": "18:05", "Location": "Test location", "Clinician": "Dr. Jones", "Session Type": "Test session"}
    ]
    
  # FAIL: No appointments available
  # other_appt_date_ranges from appointment_navigation() will have a separate test for the i/o, so mock in this scenario
  def test_appointment_navigation_no_appointments(self):
    self.mock_extractor.extract_appointments.return_value = []
    self.navigator.other_appointment_date_ranges = MagicMock(return_value=[])

    result = self.navigator.appointment_navigation()

    # Assert the result as [] since no appointments are available
    self.assertEqual(result, [])

    # Ensure extract_appointments() and other_appointment_date_ranges() were called during test
    self.mock_extractor.extract_appointments.assert_called_once()
    self.navigator.other_appointment_date_ranges.assert_called_once_with([])

  # SUCCESS: Extract initial appointments, no other appointments
  def test_appointment_navigation_with_initial_appointments_only(self):
    mock_result = self._mock_appointments()
    self.mock_extractor.extract_appointments.return_value = mock_result
    self.navigator.other_appointment_date_ranges = MagicMock(return_value=mock_result)

    result = self.navigator.appointment_navigation()
    
    self.assertEqual(result, mock_result)

    self.mock_extractor.extract_appointments.assert_called_once()
    self.navigator.other_appointment_date_ranges.assert_called_once_with(mock_result)

  # SUCCESS: No initial appointments, other available appointments at later date
  def test_appointment_navigation_with_no_initial_appointments_with_other_appointments(self):    
    self.mock_extractor.extract_appointments.return_value = []
    mock_result = self._mock_appointments()
    self.navigator.other_appointment_date_ranges = MagicMock(return_value=mock_result)

    result = self.navigator.appointment_navigation()
    
    self.assertEqual(result, mock_result)

    self.mock_extractor.extract_appointments.assert_called_once()
    self.navigator.other_appointment_date_ranges.assert_called_once_with([])

  # SUCCESS: Extract both initial appointments and other available appointments at later date
  def test_appointment_navigation_with_both_initial_and_other_appointments(self):
    mock_result1 = self._mock_appointments()
    mock_result2 = self._mock_appointments("Saturday 15th Nov 2025", "Thursday 20th Nov 2025")
    self.mock_extractor.extract_appointments.return_value = mock_result1
    mock_result_total = mock_result1 + mock_result2
    self.navigator.other_appointment_date_ranges = MagicMock(return_value=mock_result_total)

    result = self.navigator.appointment_navigation()
    
    self.assertEqual(result, mock_result_total)

    self.mock_extractor.extract_appointments.assert_called_once()
    self.navigator.other_appointment_date_ranges.assert_called_once_with(mock_result1)
    

if __name__ == "__main__":
    unittest.main()
