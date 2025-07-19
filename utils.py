"""
Utility functions for data processing
"""
from bson import ObjectId
from typing import Any, Dict, List, Union

def serialize_doc(doc: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Convert MongoDB ObjectId to string recursively
    """
    if doc is None:
        return None
        
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
        
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, (dict, list)):
                serialized[key] = serialize_doc(value)
            else:
                serialized[key] = value
        return serialized
        
    return doc

def prepare_product_response(product_doc: Dict) -> Dict:
    """
    Prepare product document for API response
    """
    if not product_doc:
        return None
        
    product = serialize_doc(product_doc)
    product["id"] = product.pop("_id")
    return product

def prepare_order_response(order_doc: Dict) -> Dict:
    """
    Prepare order document for API response
    """
    if not order_doc:
        return None
        
    order = serialize_doc(order_doc)
    order["id"] = order.pop("_id")
    return order

def build_product_query_filter(name: str = None, size: str = None) -> Dict:
    """
    Build MongoDB query filter for product search
    """
    query_filter = {}
    
    if name:
        # Support partial/regex search for name (case-insensitive)
        query_filter["name"] = {"$regex": name, "$options": "i"}
    
    if size:
        # Search for size within the sizes array
        query_filter["sizes.size"] = size
        
    return query_filter
