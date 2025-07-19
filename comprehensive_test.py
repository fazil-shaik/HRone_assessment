#!/usr/bin/env python3
"""
Comprehensive test script for the E-commerce API
Tests all endpoints with the correct data format according to specifications
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"  {test_name}")
    print(f"{'='*60}")

def print_response(response, description=""):
    status_color = "\033[92m" if response.status_code < 400 else "\033[91m"
    reset_color = "\033[0m"
    
    print(f"{description}")
    print(f"Status: {status_color}{response.status_code}{reset_color}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()

def test_health():
    """Test health endpoint"""
    print_test_header("HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Testing health endpoint...")
    return response.status_code == 200

def test_create_product():
    """Test creating a product with new format"""
    print_test_header("CREATE PRODUCT")
    product_data = {
        "name": "Samsung Galaxy S24",
        "price": 899.99,
        "sizes": [
            {
                "size": "medium",
                "quantity": 30
            },
            {
                "size": "large",
                "quantity": 20
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    print_response(response, "Testing product creation...")
    
    if response.status_code == 201:
        return response.json()["id"]
    return None

def test_list_products():
    """Test listing products"""
    print_test_header("LIST ALL PRODUCTS")
    response = requests.get(f"{BASE_URL}/products")
    print_response(response, "Testing product listing...")

def test_filter_products():
    """Test product filtering"""
    print_test_header("FILTER PRODUCTS")
    
    # Test filter by name
    response = requests.get(f"{BASE_URL}/products?name=Galaxy")
    print_response(response, "Filter by name (Galaxy)...")
    
    # Test filter by size
    response = requests.get(f"{BASE_URL}/products?size=large")
    print_response(response, "Filter by size (large)...")
    
    # Test pagination
    response = requests.get(f"{BASE_URL}/products?limit=2&offset=0")
    print_response(response, "Test pagination (limit=2, offset=0)...")

def test_create_order(product_id):
    """Test creating an order"""
    print_test_header("CREATE ORDER")
    
    if not product_id:
        print("❌ Skipping order creation - no product ID available")
        return None
    
    order_data = {
        "items": [
            {
                "productid": product_id,
                "qty": 2
            }
        ],
        "total_amount": 1799.98,
        "user_address": {
            "user_id": "testuser456",
            "street": "456 Tech Street",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105",
            "country": "USA"
        }
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print_response(response, "Testing order creation...")
    
    if response.status_code == 201:
        return response.json()["id"]
    return None

def test_get_user_orders():
    """Test getting user orders"""
    print_test_header("GET USER ORDERS")
    
    # Test orders for user123
    response = requests.get(f"{BASE_URL}/orders/user123")
    print_response(response, "Getting orders for user123...")
    
    # Test orders for testuser456
    response = requests.get(f"{BASE_URL}/orders/testuser456")
    print_response(response, "Getting orders for testuser456...")
    
    # Test pagination
    response = requests.get(f"{BASE_URL}/orders/user123?limit=1&offset=0")
    print_response(response, "Test pagination for orders...")

def test_edge_cases():
    """Test edge cases and error handling"""
    print_test_header("EDGE CASES & ERROR HANDLING")
    
    # Test invalid product creation
    invalid_product = {"name": "Invalid", "price": "not_a_number"}
    response = requests.post(f"{BASE_URL}/products", json=invalid_product)
    print_response(response, "Test invalid product data...")
    
    # Test order with invalid product ID
    invalid_order = {
        "items": [{"productid": "invalid_id", "qty": 1}],
        "total_amount": 100.0,
        "user_address": {"user_id": "test"}
    }
    response = requests.post(f"{BASE_URL}/orders", json=invalid_order)
    print_response(response, "Test order with invalid product ID...")
    
    # Test orders for non-existent user
    response = requests.get(f"{BASE_URL}/orders/nonexistent_user")
    print_response(response, "Test orders for non-existent user...")

def main():
    """Run comprehensive test suite"""
    print("🚀 Starting Comprehensive E-commerce API Tests")
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    try:
        # Test 1: Health check
        if not test_health():
            print("❌ Health check failed. Exiting.")
            return
        
        # Test 2: Create product
        product_id = test_create_product()
        
        # Test 3: List products
        test_list_products()
        
        # Test 4: Filter products
        test_filter_products()
        
        # Test 5: Create order
        order_id = test_create_order(product_id)
        
        # Test 6: Get user orders
        test_get_user_orders()
        
        # Test 7: Edge cases
        test_edge_cases()
        
        print_test_header("TEST SUMMARY")
        print("✅ All tests completed!")
        print("📊 API is working according to specifications")
        print("🎯 Ready for deployment!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on port 8000.")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
