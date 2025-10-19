from selenium.webdriver.common.by import By

# Responsible for extracting surgery details from the web page
class SurgeryInfoExtractor:
  def __init__(self, driver):
    self.driver = driver 

  def extract_address(self):
    try:
      #  PRINTS TABLE NAMES
      tables = self.driver.find_elements(By.TAG_NAME, "table")
      # for i, table in enumerate(tables):
      #     print(f"Table {i}:")
      #     print(table.text)
      #     print("-" * 20)

      # Table selected from findings above
      target_table = tables[2]

      # Get all td elements inside that table
      td_elements = target_table.find_elements(By.TAG_NAME, "td")
      
      #  PRINTS TABLE CONTENT NAMES
      # for i, td in enumerate(td_elements):
      #     print(f"TD {i}: {td.text}")

      # TD 1 contains the surgery name & address
      if len(td_elements) > 1:
        address = td_elements[1].text.strip()
        print("Surgery Address:", address)
        return address
      else:
        print("Could not find surgery name.")
        return None

    except Exception as e:
      print(f"Error extracting address: {e}")
      return None
