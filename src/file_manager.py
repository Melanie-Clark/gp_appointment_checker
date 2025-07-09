
from datetime import datetime

import pandas as pd
from tabulate import tabulate

from config import Config
     
     
# Manages saving data/logs to file and tabular formatting
class FileManager:
  def save_appointment_data(self, appt_data):
    html_table = self.table_formatter(appt_data)
    with open(Config.APPT_FILE, 'w') as file:
      file.write(html_table)
    return html_table
  
  def table_formatter(self, appt_data):
    headers = appt_data[0]
    rows = appt_data[1:]

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    
    # Format table (showindex - removes row index numbers)
    formatted_table = (tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    print(formatted_table)

    return self.html_table_formatter(df)

  # HTML table for e-mail body
  @staticmethod
  def html_table_formatter(df):
    html_table = df.to_html(index=False)

    # HTML left-align headers
    html_table = html_table.replace('<th>', '<th style="text-align:left;">')

    # print("****************")
    # print(html_table)
    return html_table
  
  # Error log (append)
  @staticmethod
  def log_error(msg):
      with open(Config.LOG_FILE, 'a') as f:
          f.write(f"[{datetime.now()}] {msg}\n")
          

