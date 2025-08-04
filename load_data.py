import sqlite3
import csv
import os

# Database setup for the project
def setup_database():
    # Connect to SQLite database (will be created if it doesn't exist)
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        age INTEGER,
        gender TEXT,
        state TEXT,
        street_address TEXT,
        postal_code TEXT,
        city TEXT,
        country TEXT,
        latitude REAL,
        longitude REAL,
        traffic_source TEXT,
        created_at TEXT
    )
    ''')
    
    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        status TEXT,
        gender TEXT,
        created_at TEXT,
        returned_at TEXT,
        shipped_at TEXT,
        delivered_at TEXT,
        num_of_item INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    return conn, cursor

# Load data from CSV files
def load_users_data(cursor, csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip header row
        
        # Prepare SQL statement
        insert_query = '''
        INSERT OR IGNORE INTO users 
        (id, first_name, last_name, email, age, gender, state, street_address, 
        postal_code, city, country, latitude, longitude, traffic_source, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        # Insert data in batches
        batch_size = 1000
        batch = []
        
        for row in csv_reader:
            # Handle potential empty values
            processed_row = []
            for value in row:
                if value == '':
                    processed_row.append(None)
                else:
                    processed_row.append(value)
            
            batch.append(processed_row)
            
            if len(batch) >= batch_size:
                cursor.executemany(insert_query, batch)
                batch = []
        
        # Insert any remaining records
        if batch:
            cursor.executemany(insert_query, batch)

def load_orders_data(cursor, csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip header row
        
        # Prepare SQL statement
        insert_query = '''
        INSERT OR IGNORE INTO orders 
        (order_id, user_id, status, gender, created_at, returned_at, 
        shipped_at, delivered_at, num_of_item) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        # Insert data in batches
        batch_size = 1000
        batch = []
        
        for row in csv_reader:
            # Handle potential empty values
            processed_row = []
            for value in row:
                if value == '':
                    processed_row.append(None)
                else:
                    processed_row.append(value)
            
            batch.append(processed_row)
            
            if len(batch) >= batch_size:
                cursor.executemany(insert_query, batch)
                batch = []
        
        # Insert any remaining records
        if batch:
            cursor.executemany(insert_query, batch)

# Verify data was loaded correctly
def verify_data(cursor):
    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    print(f"Total users loaded: {users_count}")
    
    # Sample users data
    cursor.execute("SELECT * FROM users LIMIT 5")
    print("\nSample users data:")
    users_sample = cursor.fetchall()
    for user in users_sample:
        print(user)
    
    # Check orders table
    cursor.execute("SELECT COUNT(*) FROM orders")
    orders_count = cursor.fetchone()[0]
    print(f"\nTotal orders loaded: {orders_count}")
    
    # Sample orders data
    cursor.execute("SELECT * FROM orders LIMIT 5")
    print("\nSample orders data:")
    orders_sample = cursor.fetchall()
    for order in orders_sample:
        print(order)
    
    # Additional verification queries
    print("\nAdditional verification:")
    
    # Users with most orders
    cursor.execute("""
    SELECT u.id, u.first_name, u.last_name, COUNT(o.order_id) as order_count 
    FROM users u 
    JOIN orders o ON u.id = o.user_id 
    GROUP BY u.id 
    ORDER BY order_count DESC 
    LIMIT 5
    """)
    print("\nTop 5 users with most orders:")
    top_users = cursor.fetchall()
    for user in top_users:
        print(user)
    
    # Orders by status
    cursor.execute("""
    SELECT status, COUNT(*) as count 
    FROM orders 
    GROUP BY status 
    ORDER BY count DESC
    """)
    print("\nOrders by status:")
    status_counts = cursor.fetchall()
    for status in status_counts:
        print(status)

def main():
    # File paths
    users_csv = os.path.join('archive', 'users.csv')
    orders_csv = os.path.join('archive', 'orders.csv')
    
    # Setup database
    conn, cursor = setup_database()
    
    try:
        # Load data
        print("Loading users data...")
        load_users_data(cursor, users_csv)
        conn.commit()
        
        print("Loading orders data...")
        load_orders_data(cursor, orders_csv)
        conn.commit()
        
        # Verify data
        print("\nVerifying data...")
        verify_data(cursor)
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()