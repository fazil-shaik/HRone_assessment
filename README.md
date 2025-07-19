# E-commerce Backend API

A FastAPI-based backend application for an e-commerce platform similar to Flipkart/Amazon, built as part of the HROne Backend Intern Hiring Task.

## Features

- **Product Management**: Create and list products with filtering capabilities
- **Order Management**: Create orders and retrieve user orders
- **MongoDB Integration**: Uses MongoDB for data persistence
- **Input Validation**: Pydantic models for request/response validation
- **Pagination**: Support for limit/offset pagination
- **Search & Filtering**: Regex-based product search and size filtering

## Tech Stack

- **Python 3.12**
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: Document database with Pymongo driver
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## API Endpoints

### 1. Create Product
- **Endpoint**: `POST /products`
- **Description**: Create a new product
- **Request Body**:
```json
{
  "name": "iPhone 14 Pro",
  "price": 999.99,
  "sizes": [
    {
      "size": "large",
      "quantity": 50
    }
  ]
}
```
- **Response**: `201 CREATED` 
```json
{
  "id": "1234567890"
}
```

### 2. List Products
- **Endpoint**: `GET /products`
- **Description**: Get a list of products with optional filtering
- **Query Parameters**:
  - `name` (optional): Filter by product name (supports partial/regex search)
  - `size` (optional): Filter by exact size match
  - `limit` (optional): Number of documents to return (default: 10)
  - `offset` (optional): Number of documents to skip (default: 0)
- **Response**: `200 OK`
```json
{
  "data": [
    {
      "id": "12345",
      "name": "Sample Product",
      "price": 100.0,
      "sizes": [
        {
          "size": "large",
          "quantity": 50
        }
      ],
      "created_at": "2025-07-19T10:00:00.000000"
    }
  ],
  "page": {
    "next": "10",
    "limit": 10,
    "previous": null
  }
}
```

### 3. Create Order
- **Endpoint**: `POST /orders`
- **Description**: Create a new order
- **Request Body**:
```json
{
  "items": [
    {
      "productid": "product_object_id",
      "qty": 3
    }
  ],
  "total_amount": 299.97,
  "user_address": {
    "user_id": "user123",
    "street": "123 Main Street",
    "city": "New York",
    "country": "USA"
  }
}
```
- **Response**: `201 CREATED`
```json
{
  "id": "1234567890"
}
```

### 4. Get User Orders
- **Endpoint**: `GET /orders/{user_id}`
- **Description**: Get all orders for a specific user
- **URL Parameters**:
  - `user_id`: The user ID to fetch orders for
- **Query Parameters**:
  - `limit` (optional): Number of documents to return (default: 10)
  - `offset` (optional): Number of documents to skip (default: 0)
- **Response**: `200 OK`
```json
{
  "data": [
    {
      "id": "12345",
      "items": [
        {
          "productid": "123456",
          "qty": 3,
          "productDetails": {
            "name": "Sample Product",
            "id": "123456"
          }
        }
      ],
      "total_amount": 250.0,
      "user_address": {
        "user_id": "user123",
        "street": "123 Main St",
        "city": "NYC",
        "country": "USA"
      },
      "created_at": "2025-07-19T10:00:00.000000"
    }
  ],
  "page": {
    "next": null,
    "limit": 10,
    "previous": null
  }
}
```

## Database Schema

### Products Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "float",
  "sizes": [
    {
      "size": "string",
      "quantity": "int"
    }
  ],
  "created_at": "datetime"
}
```

### Orders Collection
```json
{
  "_id": "ObjectId",
  "items": [
    {
      "productid": "string",
      "qty": "int"
    }
  ],
  "total_amount": "float",
  "user_address": {
    "user_id": "string",
    "street": "string",
    "city": "string",
    "country": "string"
  },
  "created_at": "datetime"
}
```

## Setup Instructions

### Local Development

1. **Clone the repository**:
```bash
git clone <repository-url>
cd HroneAssessment
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv shaik
source shaik/bin/activate  # On Windows: shaik\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Setup MongoDB**:
   - Install MongoDB locally, or
   - Use MongoDB Atlas (recommended for deployment)
   - Update the `MONGODB_URL` in `.env` file

5. **Run the application**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Key Features & Optimizations

1. **Modular Architecture**: Clean separation of concerns with dedicated modules
2. **Data Validation**: All inputs validated using Pydantic models with examples
3. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
4. **Inventory Management**: Automatic inventory updates when orders are created
5. **Efficient Queries**: Optimized MongoDB queries with proper indexing
6. **Pagination**: Implemented for large dataset handling with next/previous links
7. **Search Functionality**: Regex-based search for product names and size filtering
8. **Database Relationships**: Proper handling of product-order relationships with enrichment
9. **Flexible Schema**: Backward compatibility with old data formats
10. **Production Ready**: CORS middleware, health checks, and proper logging

## API Testing

1. **Manual Testing**: Use the interactive docs at `/docs` or `/redoc`
2. **Comprehensive Test**: Run `python comprehensive_test.py`
3. **Quick Tests**:
```bash
# Test health
curl http://localhost:8000/health

# Create product
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 100.0, "sizes": [{"size": "large", "quantity": 10}]}'

# List products
curl http://localhost:8000/products

# Filter products
curl "http://localhost:8000/products?size=large&name=Test"
```

## Testing

The application includes basic health check endpoints:
- `GET /`: Basic status check
- `GET /health`: Database connectivity check

## Code Structure

```
HroneAssessment/
├── main.py                 # Main FastAPI application entry point
├── database.py            # Database connection and management
├── models.py              # Pydantic models for validation
├── utils.py               # Utility functions
├── routers/               # API route modules
│   ├── __init__.py
│   ├── products.py        # Product-related endpoints
│   └── orders.py          # Order-related endpoints
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
├── comprehensive_test.py  # Comprehensive test suite
└── shaik/                # Virtual environment
```

## Future Enhancements

- User authentication and authorization
- Product image upload functionality
- Order status tracking
- Advanced search with Elasticsearch
- Caching with Redis
- Rate limiting
- Comprehensive test suite
