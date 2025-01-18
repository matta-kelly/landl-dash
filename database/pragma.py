import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data_app.db')  # Update with your DB file path
cursor = conn.cursor()

# Run PRAGMA to get table schema
cursor.execute("PRAGMA table_info(master_sku);")

# Fetch all rows
columns = cursor.fetchall()

# Print column details
for column in columns:
    print(column)

# Close the connection
conn.close()
