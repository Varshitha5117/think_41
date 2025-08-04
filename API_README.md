# E-commerce RESTful API

This is a RESTful API that provides access to customer data and basic order statistics from the e-commerce database.

## Setup

1. Make sure you have Python installed on your system
2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Ensure the database has been created by running the data loading script first (if not already done):

```
python load_data.py
```

4. Start the API server:

```
python api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check

```
GET /api/health
```

Returns the health status of the API and database connection.

### List All Customers

```
GET /api/customers
```

Returns a paginated list of customers with basic information and order count.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Number of customers per page (default: 10)

**Example Response:**
```json
{
  "data": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "city": "New York",
      "country": "United States",
      "order_count": 3
    },
    ...
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total_count": 100000,
    "total_pages": 10000
  }
}
```

### Get Customer Details

```
GET /api/customers/{customer_id}
```

Returns detailed information about a specific customer, including order statistics.

**Example Response:**
```json
{
  "customer": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "age": 35,
    "gender": "M",
    "state": "New York",
    "street_address": "123 Main St",
    "postal_code": "10001",
    "city": "New York",
    "country": "United States",
    "latitude": 40.7128,
    "longitude": -74.006,
    "traffic_source": "Search",
    "created_at": "2022-01-01 12:00:00+00:00"
  },
  "order_count": 3,
  "order_stats": {
    "status_distribution": {
      "Complete": 2,
      "Shipped": 1
    },
    "total_items": 7
  },
  "recent_orders": [
    {
      "order_id": 1001,
      "status": "Complete",
      "created_at": "2022-03-15 14:30:00+00:00",
      "shipped_at": "2022-03-16 10:15:00+00:00",
      "delivered_at": "2022-03-18 09:45:00+00:00",
      "num_of_item": 3
    },
    ...
  ]
}
```

### Get Overall Statistics

```
GET /api/stats
```

Returns overall statistics about customers and orders.

**Example Response:**
```json
{
  "total_customers": 100000,
  "total_orders": 125000,
  "orders_by_status": {
    "Complete": 50000,
    "Shipped": 30000,
    "Processing": 25000,
    "Cancelled": 15000,
    "Returned": 5000
  },
  "top_countries": {
    "United States": 30000,
    "China": 25000,
    "Brazil": 15000,
    "United Kingdom": 10000,
    "Germany": 5000
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Request successful
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a JSON object with an error message:

```json
{
  "error": "Customer not found"
}
```

## CORS Support

The API includes CORS headers to allow cross-origin requests from any domain, making it easy to integrate with frontend applications.

### List All Orders

```
GET /api/orders
```

Returns a paginated list of orders with basic information including customer details.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Number of orders per page (default: 10)

**Example Response:**
```json
{
  "data": [
    {
      "order_id": 1001,
      "user_id": 42,
      "status": "Complete",
      "created_at": "2022-03-15 14:30:00+00:00",
      "shipped_at": "2022-03-16 10:15:00+00:00",
      "delivered_at": "2022-03-18 09:45:00+00:00",
      "num_of_item": 3,
      "first_name": "John",
      "last_name": "Doe"
    },
    ...
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total_count": 125000,
    "total_pages": 12500
  }
}
```

### Get Order Details

```
GET /api/orders/{order_id}
```

Returns detailed information about a specific order, including customer information.

**Example Response:**
```json
{
  "order_id": 1001,
  "user_id": 42,
  "status": "Complete",
  "gender": "M",
  "created_at": "2022-03-15 14:30:00+00:00",
  "returned_at": null,
  "shipped_at": "2022-03-16 10:15:00+00:00",
  "delivered_at": "2022-03-18 09:45:00+00:00",
  "num_of_item": 3,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

### Get Customer Orders

```
GET /api/customers/{customer_id}/orders
```

Returns all orders for a specific customer with pagination and order statistics.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Number of orders per page (default: 10)

**Example Response:**
```json
{
  "customer_id": 42,
  "order_count": 5,
  "order_stats": {
    "status_distribution": {
      "Complete": 3,
      "Shipped": 1,
      "Processing": 1
    },
    "total_items": 12
  },
  "orders": [
    {
      "order_id": 1001,
      "status": "Complete",
      "created_at": "2022-03-15 14:30:00+00:00",
      "shipped_at": "2022-03-16 10:15:00+00:00",
      "delivered_at": "2022-03-18 09:45:00+00:00",
      "returned_at": null,
      "num_of_item": 3
    },
    ...
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total_count": 5,
    "total_pages": 1
  }
}
```

## Testing

You can test the API using tools like:

1. **Browser**: Simply navigate to the endpoints in your web browser
2. **Postman**: Import the API endpoints and test with different parameters
3. **curl**: Use command-line requests to test the API

## Example curl Commands

```bash
# Health check
curl http://localhost:5000/api/health

# List customers (first page)
curl http://localhost:5000/api/customers

# Get customer details
curl http://localhost:5000/api/customers/1

# List all orders for a customer
curl http://localhost:5000/api/customers/1/orders

# List all orders (first page)
curl http://localhost:5000/api/orders

# Get order details
curl http://localhost:5000/api/orders/1001

# Get overall statistics
curl http://localhost:5000/api/stats
```