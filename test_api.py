#!/usr/bin/env python3
"""
Simple test script for the E-commerce API
Run this after starting the FastAPI server to test the endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_product():
    """Test creating a product"""
    print("Testing product creation...")
    product_data = {
        "name": "iPhone 14 Pro",
        "price": 999.99,
        "sizes": [
            {
                "size": "large",
                "quantity": 50
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()["id"]
    return None

def test_list_products():
    """Test listing products"""
    print("\nTesting product listing...")
    response = requests.get(f"{BASE_URL}/products")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search_products():
    """Test product search"""
    print("Testing product search...")
    # Search by name
    response = requests.get(f"{BASE_URL}/products?name=iPhone")
    print(f"Search by name - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Search by size
    response = requests.get(f"{BASE_URL}/products?size=large")
    print(f"Search by size - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_order(product_id):
    """Test creating an order"""
    if not product_id:
        print("Skipping order creation - no product ID available")
        return None
        
    print("Testing order creation...")
    order_data = {
        "items": [
            {
                "productid": product_id,
                "qty": 2
            }
        ],
        "total_amount": 1999.98,
        "user_address": {
            "user_id": "user123",
            "street": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "USA"
        }
    }
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()
    return None

def test_get_user_orders():
    """Test getting user orders"""
    print("\nTesting user orders retrieval...")
    user_id = "user123"
    response = requests.get(f"{BASE_URL}/orders/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("Starting API Tests...")
    print("=" * 50)
    
    # Test health
    test_health()
    
    # Test product creation
    product_id = test_create_product()
    
    # Test product listing
    test_list_products()
    
    # Test product search
    test_search_products()
    
    # Test order creation
    order = test_create_order(product_id)
    
    # Test user orders
    test_get_user_orders()
    
    print("Tests completed!")

if __name__ == "__main__":
    main()
