import sqlite3
import logging
import os
from database.db_schema import CREATE_TABLES  # Import schema definitions

# Configure logging
logger = logging.getLogger(__name__)

# Define the database file
DB_FILE = "data_app.db"

def initialize_db():
    """
    Initialize the SQLite database by wiping the existing database and creating new tables.
    """
    try:
        # If the database already exists, delete it
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            logger.info(f"Existing database file '{DB_FILE}' has been deleted.")
        
        # Connect to the database (this will create a new file)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Execute each table creation statement from the schema
        for table_name, table_sql in CREATE_TABLES.items():
            cursor.execute(table_sql)
        
        # Commit and close the connection
        conn.commit()
        conn.close()
        
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    initialize_db()
