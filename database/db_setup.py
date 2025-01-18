import sqlite3
import logging
from database.db_schema import CREATE_TABLES  # Import schema definitions

# Configure logging
logger = logging.getLogger(__name__)

# Define the database file
DB_FILE = "data_app.db"

def initialize_db():
    """
    Initialize the SQLite database and create tables if they don't exist.
    """
    try:
        # Connect to the database (creates the file if it doesn't exist)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Execute each table creation statement from the schema
        for table_name, table_sql in CREATE_TABLES.items():
            cursor.execute(table_sql)
            logger.debug(f"Executed SQL for table '{table_name}': {table_sql}")
        
        # Commit and close the connection
        conn.commit()
        conn.close()
        
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    initialize_db()
