import pandas as pd
import matplotlib.pyplot as plt

# Define the file path
file_path = '/Users/kartiktripathi/Desktop/CRIS/dashboard_app/first_project_django/pandas_test/trains.xlsx'

# Load the Excel file
df = pd.read_excel(file_path, sheet_name='Sheet 1')

# Clean up the dataframe and set appropriate column headers
df.columns = df.iloc[0].str.strip()  # Strip any leading/trailing spaces from column names
df = df.drop(0).reset_index(drop=True)

# Convert 'capacity' column to numeric (if not already)
df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce')

# Drop rows with NaN values in 'capacity' and 'trainname'
df = df.dropna(subset=['capacity', 'trainname'])

# Display the dataframe
print(df)

# Plot bar plot for 'trainname' vs. 'capacity'
plt.figure(figsize=(12, 8))
plt.bar(df['trainname'], df['capacity'], color='purple', edgecolor='black')
plt.title('Train Name vs Capacity')
plt.xlabel('Train Name')
plt.ylabel('Capacity')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.tight_layout()
plt.show()