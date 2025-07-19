"""
Order-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from database import db_manager
from models import OrderCreate, OrdersResponse
from utils import prepare_order_response

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", status_code=201, response_model=dict)
async def create_order(order: OrderCreate):
    """
    Create a new order
    
    - **items**: List of products and quantities to order
    - **total_amount**: Total amount for the order
    - **user_address**: User address information including user_id
    """
    if not db_manager.is_connected():
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Validate that all products exist and have sufficient inventory
        for item in order.items:
            try:
                product_object_id = ObjectId(item.productid)
            except InvalidId:
                raise HTTPException(status_code=400, detail=f"Invalid product ID format: {item.productid}")
            
            product = db_manager.products_collection.find_one({"_id": product_object_id})
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.productid} not found")
            
            # Check inventory across all sizes
            total_inventory = sum(size_info["quantity"] for size_info in product.get("sizes", []))
            if total_inventory < item.qty:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient inventory for product {item.productid}. Available: {total_inventory}, Requested: {item.qty}"
                )
        
        # Create order
        order_dict = order.model_dump()
        order_dict["created_at"] = datetime.now()
        
        result = db_manager.orders_collection.insert_one(order_dict)
        
        # Update product inventories (decrease from first available size)
        for item in order.items:
            product = db_manager.products_collection.find_one({"_id": ObjectId(item.productid)})
            remaining_qty = item.qty
            
            for i, size_info in enumerate(product["sizes"]):
                if remaining_qty <= 0:
                    break
                    
                available = size_info["quantity"]
                to_deduct = min(available, remaining_qty)
                
                # Update the specific size quantity
                db_manager.products_collection.update_one(
                    {"_id": ObjectId(item.productid)},
                    {"$inc": {f"sizes.{i}.quantity": -to_deduct}}
                )
                
                remaining_qty -= to_deduct
        
        # Return just the ID as per specification
        return {"id": str(result.inserted_id)}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@router.get("/{user_id}", response_model=dict)
async def get_user_orders(
    user_id: str,
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of documents to skip")
):
    """
    Get orders for a specific user
    
    - **user_id**: The user ID to fetch orders for
    - **limit**: Number of orders to return (1-100)
    - **offset**: Number of orders to skip for pagination
    """
    if not db_manager.is_connected():
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Filter by user_id in user_address
        query_filter = {"user_address.user_id": user_id}
        
        # Get total count for the query
        total_count = db_manager.orders_collection.count_documents(query_filter)
        
        # Execute query with pagination
        cursor = (db_manager.orders_collection
                 .find(query_filter)
                 .sort("_id", 1)
                 .skip(offset)
                 .limit(limit))
        
        orders = list(cursor)
        
        # Prepare response - need to enrich with product details
        processed_orders = []
        for order in orders:
            processed_order = prepare_order_response(order)
            if processed_order:
                # Enrich items with product details
                for item in processed_order.get("items", []):
                    try:
                        product = db_manager.products_collection.find_one({"_id": ObjectId(item["productid"])})
                        if product:
                            item["productDetails"] = {
                                "name": product.get("name", "Unknown Product"),
                                "id": str(product["_id"])
                            }
                    except:
                        item["productDetails"] = {
                            "name": "Unknown Product",
                            "id": item["productid"]
                        }
                
                processed_orders.append(processed_order)
        
        # Calculate pagination info
        next_offset = offset + limit if offset + limit < total_count else None
        prev_offset = max(0, offset - limit) if offset > 0 else None
        
        return {
            "data": processed_orders,
            "page": {
                "next": str(next_offset) if next_offset is not None else None,
                "limit": limit,
                "previous": str(prev_offset) if prev_offset is not None else None
            }
        }
        
    except Exception as e:
        print(f"Error fetching orders: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")
