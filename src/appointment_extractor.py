from selenium.webdriver.common.by import By

# Extracts appointment data from SystmOnline website
class AppointmentExtractor:       
  def __init__(self, driver):
    self.driver = driver

  def extract_appointments(self):
    # Find the table names for each table
    # tables = self.driver.find_elements(By.TAG_NAME, "table")
    # for i, table in enumerate(tables):
    #     print(f"Table {i}:")
    #     print(table.text)
    #     print("-" * 20)

    # Appointments table
    tables = self.driver.find_elements(By.TAG_NAME, "table")
    # If there's available appointments, save appointment data
    if len(tables) >= 6:
      appt_table = tables[5]
      # Extract table rows
      rows = appt_table.find_elements(By.TAG_NAME, "tr")
      
      data = []
      for row in rows:
          cells = row.find_elements(By.TAG_NAME, "th") or row.find_elements(By.TAG_NAME, "td")
          row_data = [cell.text.strip() for cell in cells]
          row_data = row_data[:-1] # Remove last column
          data.append(row_data)
      return data
    return []
