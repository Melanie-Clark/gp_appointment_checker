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

    # We expect the code to raise Exception("Failed login attempt...") because the login “failed”
    with self.assertRaises(Exception) as context:
        self.navigator.login(self.file_manager, self.email_manager)

    # Confirms the exception message is the one we expect, so test passes
    self.assertIn("Failed login attempt", str(context.exception))

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
  # No appointments available
  # other_appt_date_ranges from appointment_navigation() will have a separate test for the i/o, so mock in this scenario
  def test_appointment_navigation_no_appointments(self):
    self.mock_extractor.extract_appointments.return_value = []
    
    # Mock the helper function to avoid Selenium calls
    self.navigator.other_appointment_date_ranges = MagicMock(return_value=[])

    result = self.navigator.appointment_navigation()

    # Assert the result is 0 since no appointments are available
    self.assertEqual(result, 0)

    # Ensure extract_appointments() was called during test
    self.mock_extractor.extract_appointments.assert_called_once()


if __name__ == "__main__":
    unittest.main()
