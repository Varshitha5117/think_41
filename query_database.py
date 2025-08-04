import sqlite3
import sys

def connect_to_db():
    """Connect to the SQLite database"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        sys.exit(1)

def execute_query(conn, query, params=()):
    """Execute a query and return results"""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Query execution error: {e}")
        return []

def print_results(results, query_name):
    """Print query results in a formatted way"""
    print(f"\n=== {query_name} ===")
    if not results:
        print("No results found.")
        return
    
    # Get column names from the first row
    columns = results[0].keys()
    
    # Calculate column widths
    col_widths = {col: max(len(col), max([len(str(row[col])) for row in results])) for col in columns}
    
    # Print header
    header = " | ".join(col.ljust(col_widths[col]) for col in columns)
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in results:
        print(" | ".join(str(row[col]).ljust(col_widths[col]) for col in columns))
    
    print(f"Total results: {len(results)}")

def main():
    conn = connect_to_db()
    
    # Example queries
    queries = [
        {
            "name": "User Demographics by Gender",
            "sql": """
            SELECT gender, COUNT(*) as count, 
                   ROUND(AVG(age), 2) as avg_age,
                   MIN(age) as min_age,
                   MAX(age) as max_age
            FROM users
            GROUP BY gender
            """
        },
        {
            "name": "Order Status Distribution",
            "sql": """
            SELECT status, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
            FROM orders
            GROUP BY status
            ORDER BY count DESC
            """
        },
        {
            "name": "Top 10 Countries by User Count",
            "sql": """
            SELECT country, COUNT(*) as user_count
            FROM users
            GROUP BY country
            ORDER BY user_count DESC
            LIMIT 10
            """
        },
        {
            "name": "Traffic Source Analysis",
            "sql": """
            SELECT traffic_source, COUNT(*) as user_count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as percentage
            FROM users
            GROUP BY traffic_source
            ORDER BY user_count DESC
            """
        },
        {
            "name": "Order Fulfillment Time Analysis",
            "sql": """
            SELECT 
                status,
                COUNT(*) as order_count,
                ROUND(AVG(JULIANDAY(shipped_at) - JULIANDAY(created_at)), 2) as avg_days_to_ship,
                ROUND(AVG(JULIANDAY(delivered_at) - JULIANDAY(shipped_at)), 2) as avg_days_in_transit
            FROM orders
            WHERE status IN ('Complete', 'Shipped')
            GROUP BY status
            """
        },
        {
            "name": "User Registration Trend by Year",
            "sql": """
            SELECT 
                SUBSTR(created_at, 1, 4) as year,
                COUNT(*) as new_users
            FROM users
            GROUP BY year
            ORDER BY year
            """
        },
        {
            "name": "Users with Most Orders",
            "sql": """
            SELECT 
                u.id, 
                u.first_name || ' ' || u.last_name as full_name,
                u.email,
                COUNT(o.order_id) as order_count,
                SUM(o.num_of_item) as total_items
            FROM users u
            JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            ORDER BY order_count DESC, total_items DESC
            LIMIT 10
            """
        }
    ]
    
    # Execute and print results for each query
    for query in queries:
        results = execute_query(conn, query["sql"])
        print_results(results, query["name"])
    
    conn.close()

if __name__ == "__main__":
    main()