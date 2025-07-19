"""
Database configuration and connection management
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
        self.database_name = os.getenv("DATABASE_NAME", "ecommerce")
        self.client = None
        self.db = None
        self.products_collection = None
        self.orders_collection = None
        self._connect()

    def _connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(
                self.mongodb_url, 
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.database_name]
            self.products_collection = self.db.products
            self.orders_collection = self.db.orders
            
            # Create indexes for better performance
            self._create_indexes()
            
            print("✅ Connected to MongoDB successfully!")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB connection error: {e}")
            print("Running without MongoDB - database endpoints will not work")
        except Exception as e:
            print(f"❌ Unexpected database error: {e}")

    def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Index on product name for search
            self.products_collection.create_index([("name", "text")])
            
            # Index on product size
            self.products_collection.create_index("size")
            
            # Index on user_id in orders for faster user order queries
            self.orders_collection.create_index("user_address.user_id")
            
            print("✅ Database indexes created successfully!")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not create indexes: {e}")

    def is_connected(self):
        """Check if database is connected and available"""
        return (self.client is not None and 
                self.products_collection is not None and 
                self.orders_collection is not None)

    def health_check(self):
        """Perform a health check on the database connection"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return {"status": "healthy", "database": "connected"}
            else:
                return {"status": "degraded", "database": "disconnected", "message": "Running without database"}
        except Exception as e:
            return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Global database manager instance
db_manager = DatabaseManager()
