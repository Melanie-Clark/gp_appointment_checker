import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unittest.mock import MagicMock
from systmonline_navigator import SystmOnlineNavigator
from file_manager import FileManager
from email_manager import EmailManager


class TestSystmOnlineNavigator(unittest.TestCase):
    def setUp(self):
        """
        This runs before every test, avoiding object creation repeition in each test - creates fresh mock objects for the 
        driver, file_manager, and email_manager to isolate tests from real browser or emails.
        """
        self.mock_driver = MagicMock()         # MagicMock fakes the driver
        self.file_manager = FileManager()
        self.email_manager = EmailManager()
        self.navigator = SystmOnlineNavigator(self.mock_driver, extractor=None)

    # Test wrong username/password - failed login
    def test_login_failure(self):
        # Fakes the HTML element that would appear on login failure
        error_element = MagicMock() 
        # Login just checks if error_span exists, not the actual text - error_span[0].text.strip()
        # MagicMock needs a .text attribute (any text) to avoid errors
        error_element.text = "Invalid username or password"

        # Mock Selenium driver.find_elements(By.ID, "errorText") o the login function thinks a failed login element exists
        self.mock_driver.find_elements.return_value = [error_element]

        # We expect the code to raise Exception("Failed login attempt...") because the login “failed”
        with self.assertRaises(Exception) as context:
            self.navigator.login(self.file_manager, self.email_manager)

        # Confirms the exception message is the one we expect, so test passes
        self.assertIn("Failed login attempt", str(context.exception))


if __name__ == "__main__":
    unittest.main()
