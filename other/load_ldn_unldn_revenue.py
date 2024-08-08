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
csv_file_path = '/Users/kartiktripathi/terminal_dashboard/data/ldn_unldn_revenue.csv'

# Define a function to handle empty strings and convert dates
def handle_empty(value, is_date=False):
    if value == '':
        return None
    if is_date:
        return f"{value}-01"  # Convert YYYY-MM to YYYY-MM-01
    return value

# Define a function to insert data
def insert_data(row):
    cur.execute(
        """
        INSERT INTO ldn_unldn_revenue (month, zone, division, station_code, loading_in_mt, earning_in_rs_cr, unloading_in_mt)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        [
            handle_empty(row[0], is_date=True),  # month
            handle_empty(row[1]),  # zone
            handle_empty(row[2]),  # division
            handle_empty(row[3]),  # station_code
            handle_empty(row[4]),  # loading_in_mt
            handle_empty(row[5]),  # earning_in_rs_cr
            handle_empty(row[6])   # unloading_in_mt
        ]
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
