from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserManager:
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
