import csv
import psycopg2

# Database connection parameters
dbname = 'terminals'
user = 'kt'
password = 'ktsdb1'
host = 'localhost'
port = '5432'

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Path to the CSV file
csv_file_path = '/Users/kartiktripathi/terminal_dashboard/data/TERMINAL_DATA.csv'

# Define a function to handle empty strings
def handle_empty(value):
    if value == '':
        return None
    return value

# Define a function to insert data
def insert_data(row):
    cur.execute(
        """
        INSERT INTO terminal_data (station_code, station_name, division, zone, district, state, working_hours_from, 
        working_hours_to, terminal_type, avg_rakes_handling, line_count, handling_type, warehouse_available_yes_no, 
        owner, associated_weighbridge, alternate_weighbridge, tank_handling_yes_no, latitude, longitude) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [handle_empty(value) for value in row]
    )

# Open the CSV file and load data
with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        insert_data(row)

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()
