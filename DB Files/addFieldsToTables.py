import sqlite3

# --- Configuration ---
DB_FILE = "dragon.db"
TABLE_NAME = "CUSTOMER"

def view_customers():
    """Reads and prints all records from the CUSTOMER table."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("\n--- Current Customers ---")
        
        cursor.execute(f"SELECT id, name, email FROM {TABLE_NAME}")
        all_customers = cursor.fetchall()

        if not all_customers:
            print("No customers found in the table.")
            return False
        
        for customer in all_customers:
            print(f"ID: {customer[0]} | Name: {customer[1]} | Email: {customer[2]}")
        
        return True

    except sqlite3.OperationalError:
        print(f"❌ Error: The table '{TABLE_NAME}' does not seem to exist in '{DB_FILE}'.")
        return False
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_customer():
    """Selects a customer by ID and updates their name and email."""
    if not view_customers():
        return

    try:
        customer_id = input("\nEnter the ID of the customer you want to edit: ")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(f"SELECT id, name, email FROM {TABLE_NAME} WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()

        if customer is None:
            print(f"❌ No customer found with ID: {customer_id}")
            return

        print("\nEnter the new information (press Enter to keep current value).")
        current_name = customer[1]
        current_email = customer[2]

        new_name = input(f"New name (current is '{current_name}'): ") or current_name
        new_email = input(f"New email (current is '{current_email}'): ") or current_email

        update_query = f"UPDATE {TABLE_NAME} SET name = ?, email = ? WHERE id = ?"
        cursor.execute(update_query, (new_name, new_email, customer_id))
        
        conn.commit()
        print(f"\n✅ Customer with ID {customer_id} has been updated successfully!")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

# --- NEW FUNCTION ---
def add_customer():
    """Prompts for user details and adds a new record to the CUSTOMER table."""
    try:
        print("\n--- Add a New Customer ---")
        name = input("Enter the customer's name: ")
        email = input("Enter the customer's email: ")

        # A simple check to ensure inputs are not empty
        if not name or not email:
            print("❌ Name and email cannot be empty.")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Construct and execute the INSERT query
        insert_query = f"INSERT INTO {TABLE_NAME} (name, email) VALUES (?, ?)"
        cursor.execute(insert_query, (name, email))
        
        conn.commit()
        print(f"\n✅ Customer '{name}' added successfully!")

    except sqlite3.IntegrityError:
        # This error occurs if the email already exists, due to the 'UNIQUE' constraint
        print(f"❌ Error: A customer with the email '{email}' already exists.")
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

def main():
    """Displays the main menu and handles user choices."""
    while True:
        print("\n=============================")
        print("  Customer Database Manager")
        print("=============================")
        print("1. View all customers")
        print("2. Update a customer")
        # --- MENU UPDATED ---
        print("3. Add a new customer")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_customers()
        elif choice == '2':
            update_customer()
        # --- NEW OPTION HANDLER ---
        elif choice == '3':
            add_customer()
        elif choice == '4':
            print("Exiting program. Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()