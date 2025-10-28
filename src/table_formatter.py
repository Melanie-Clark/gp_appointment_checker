import pandas as pd
from tabulate import tabulate
     
     
# Formats tables and logs to file and tabular formatting
class TableFormatter:
  def table_formatter(self, appt_data):
    headers = appt_data[0]
    rows = appt_data[1:]

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Print a readable version to terminal    
    # Format table (showindex - removes row index numbers)
    formatted_table = (tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    print(formatted_table)

    return self.html_table_formatter(df)

  # HTML version - table for e-mail body
  @staticmethod
  def html_table_formatter(df):
    html_table = df.to_html(index=False)

    # HTML left-align headers
    html_table = html_table.replace('<th>', '<th style="text-align:left;">')
    return html_table
