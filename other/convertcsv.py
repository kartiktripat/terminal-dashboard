import pandas as pd

# Load the Excel file
file_path = "/Users/kartiktripathi/terminal_dashboard/data/excel/ldn_unldn_revenue.xlsx"
excel_data = pd.read_excel(file_path)

# Convert Excel data to CSV
csv_file_path = "/Users/kartiktripathi/terminal_dashboard/data/ldn_unldn_revenue.csv"
excel_data.to_csv(csv_file_path, index=False)

csv_file_path
