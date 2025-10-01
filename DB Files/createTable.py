import sqlite3
import re # Using the regular expression module for validation

def create_table_dynamically():
    """
    Connects to an SQLite database, prompts the user for a table name,
    validates it, and creates the table.
    """
    # This line has been changed to your database file name
    db_file = "dragon.db"
    
    conn = None  # Initialize connection to None

    try:
        # --- 1. Get and Validate User Input ---
        table_name = input("Enter the name for the new table: ")

        # A simple security check for a valid table name
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            print(f"Error: '{table_name}' is not a valid table name. Please use only letters, numbers, and underscores.")
            return

        # --- 2. Connect to the Database ---
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print(f"✅ Successfully connected to '{db_file}'")

        # --- 3. Construct and Execute the SQL Query ---
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        """
        
        cursor.execute(create_table_query)
        print(f"✅ Table '{table_name}' created successfully.")

        # --- 4. Commit the Changes and Close ---
        conn.commit()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if conn:
            conn.close()
            print("🔌 Database connection closed.")

# Run the function when the script is executed
if __name__ == "__main__":
    create_table_dynamically()