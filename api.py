from flask import Flask, jsonify, request, abort
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('ecommerce.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# API endpoints
@app.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        
        # Get total count for pagination metadata
        total_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        
        # Get customers with pagination
        customers = conn.execute(
            '''
            SELECT id, first_name, last_name, email, city, country 
            FROM users 
            ORDER BY id 
            LIMIT ? OFFSET ?
            ''', 
            (per_page, offset)
        ).fetchall()
        
        # Convert to list of dictionaries
        customer_list = []
        for customer in customers:
            customer_dict = dict(customer)
            # Add order count for each customer
            order_count = conn.execute(
                'SELECT COUNT(*) FROM orders WHERE user_id = ?', 
                (customer['id'],)
            ).fetchone()[0]
            customer_dict['order_count'] = order_count
            customer_list.append(customer_dict)
        
        conn.close()
        
        # Prepare pagination metadata
        total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
        
        return jsonify({
            'data': customer_list,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages
            }
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        conn = get_db_connection()
        
        # Get customer details
        customer = conn.execute(
            'SELECT * FROM users WHERE id = ?', 
            (customer_id,)
        ).fetchone()
        
        if customer is None:
            conn.close()
            return jsonify({'error': 'Customer not found'}), 404
        
        # Convert to dictionary
        customer_dict = dict(customer)
        
        # Get order count
        order_count = conn.execute(
            'SELECT COUNT(*) FROM orders WHERE user_id = ?', 
            (customer_id,)
        ).fetchone()[0]
        
        # Get order details
        orders = conn.execute(
            '''
            SELECT order_id, status, created_at, shipped_at, delivered_at, num_of_item 
            FROM orders 
            WHERE user_id = ? 
            ORDER BY created_at DESC
            ''', 
            (customer_id,)
        ).fetchall()
        
        # Convert orders to list of dictionaries
        order_list = [dict(order) for order in orders]
        
        # Add order statistics
        order_stats = {}
        if order_count > 0:
            # Get status distribution
            status_counts = conn.execute(
                '''
                SELECT status, COUNT(*) as count 
                FROM orders 
                WHERE user_id = ? 
                GROUP BY status
                ''', 
                (customer_id,)
            ).fetchall()
            
            status_dict = {status['status']: status['count'] for status in status_counts}
            order_stats['status_distribution'] = status_dict
            
            # Get total items ordered
            total_items = conn.execute(
                '''
                SELECT SUM(num_of_item) as total 
                FROM orders 
                WHERE user_id = ?
                ''', 
                (customer_id,)
            ).fetchone()['total']
            
            order_stats['total_items'] = total_items
        
        conn.close()
        
        # Prepare response
        response = {
            'customer': customer_dict,
            'order_count': order_count,
            'order_stats': order_stats,
            'recent_orders': order_list[:5] if order_list else []  # Include only 5 most recent orders
        }
        
        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        
        # Get total customers
        total_customers = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        
        # Get total orders
        total_orders = conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
        
        # Get orders by status
        status_counts = conn.execute(
            '''
            SELECT status, COUNT(*) as count 
            FROM orders 
            GROUP BY status 
            ORDER BY count DESC
            '''
        ).fetchall()
        
        status_dict = {status['status']: status['count'] for status in status_counts}
        
        # Get top countries by user count
        top_countries = conn.execute(
            '''
            SELECT country, COUNT(*) as count 
            FROM users 
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 5
            '''
        ).fetchall()
        
        countries_dict = {country['country']: country['count'] for country in top_countries}
        
        conn.close()
        
        return jsonify({
            'total_customers': total_customers,
            'total_orders': total_orders,
            'orders_by_status': status_dict,
            'top_countries': countries_dict
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check if database exists and is accessible
        if not os.path.exists('ecommerce.db'):
            return jsonify({'status': 'error', 'message': 'Database file not found'}), 500
        
        # Try to connect to the database
        conn = get_db_connection()
        conn.execute('SELECT 1').fetchone()
        conn.close()
        
        return jsonify({'status': 'healthy', 'message': 'API is running and database is accessible'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)