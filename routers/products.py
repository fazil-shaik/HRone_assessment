"""
Product-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from database import db_manager
from models import ProductCreate, ProductsResponse
from utils import prepare_product_response, build_product_query_filter

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", status_code=201, response_model=dict)
async def create_product(product: ProductCreate):
    """
    Create a new product
    
    - **name**: Product name
    - **price**: Product price  
    - **sizes**: Array of size objects with size and quantity
    """
    if not db_manager.is_connected():
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Convert to dict and add timestamp
        product_dict = product.model_dump()
        product_dict["created_at"] = datetime.now()
        
        # Insert product
        result = db_manager.products_collection.insert_one(product_dict)
        
        # Return just the ID as per specification
        return {"id": str(result.inserted_id)}
        
    except Exception as e:
        print(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@router.get("", response_model=dict)
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name (supports partial/regex search)"),
    size: Optional[str] = Query(None, description="Filter by product size"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of documents to skip")
):
    """
    List products with optional filtering and pagination
    
    - **name**: Filter by product name (case-insensitive, supports partial matches)
    - **size**: Filter by exact size match (searches within sizes array)
    - **limit**: Number of products to return (1-100)
    - **offset**: Number of products to skip for pagination
    """
    if not db_manager.is_connected():
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        # Build query filter
        query_filter = {}
        
        if name:
            # Support partial/regex search for name (case-insensitive)
            query_filter["name"] = {"$regex": name, "$options": "i"}
        
        if size:
            # Search for size within the sizes array OR old format
            query_filter["$or"] = [
                {"sizes.size": size},
                {"size": size}  # Support old format
            ]
        
        # Get total count for the query
        total_count = db_manager.products_collection.count_documents(query_filter)
        
        # Execute query with pagination
        cursor = (db_manager.products_collection
                 .find(query_filter)
                 .sort("_id", 1)
                 .skip(offset)
                 .limit(limit))
        
        products = list(cursor)
        
        # Prepare response - convert old format to new format if needed
        processed_products = []
        for product in products:
            processed_product = prepare_product_response(product)
            if processed_product:
                # Convert old format to new format if needed
                if "sizes" not in processed_product and "size" in processed_product:
                    processed_product["sizes"] = [{
                        "size": processed_product.pop("size"),
                        "quantity": processed_product.pop("inventory_count", 0)
                    }]
                    # Remove old fields
                    processed_product.pop("description", None)
                    processed_product.pop("category", None)
                
                processed_products.append(processed_product)
        
        # Calculate pagination info
        next_offset = offset + limit if offset + limit < total_count else None
        prev_offset = max(0, offset - limit) if offset > 0 else None
        
        return {
            "data": processed_products,
            "page": {
                "next": str(next_offset) if next_offset is not None else None,
                "limit": limit,
                "previous": str(prev_offset) if prev_offset is not None else None
            }
        }
        
    except Exception as e:
        print(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")
