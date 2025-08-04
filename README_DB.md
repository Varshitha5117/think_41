# E-commerce Database Setup

This project sets up a SQLite database for e-commerce data analysis using CSV files from the dataset.

## Database Schema

### Users Table

```sql
CREATE TABLE users (
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
```

### Orders Table

```sql
CREATE TABLE orders (
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
```

## How to Run

1. Make sure you have Python installed on your system
2. The script uses SQLite which is included in Python's standard library
3. Run the script with the following command:

```
python load_data.py
```

4. The script will:
   - Create a SQLite database file named `ecommerce.db`
   - Create tables for users and orders
   - Load data from the CSV files
   - Verify the data was loaded correctly by running sample queries

## Data Verification

The script performs the following verification steps:

1. Counts the total number of users and orders loaded
2. Displays sample data from both tables
3. Shows the top 5 users with the most orders
4. Provides a breakdown of orders by status

## Notes

- The script uses batch processing to efficiently load large CSV files
- Empty values in the CSV are converted to NULL in the database
- The script includes error handling to rollback changes if any issues occur during data loading