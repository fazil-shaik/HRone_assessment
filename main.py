"""
E-commerce FastAPI Backend Application

A modular FastAPI application for e-commerce platform similar to Flipkart/Amazon.
Built for HROne Backend Intern Hiring Task.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db_manager
from models import HealthResponse
from routers import products, orders

# Create FastAPI app
app = FastAPI(
    title="E-commerce API",
    description="FastAPI backend for ecommerce application - HROne Hiring Task",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(orders.router)

# Root endpoints
@app.get("/", tags=["health"])
async def root():
    """Root endpoint for basic status check"""
    return {
        "message": "E-commerce API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Comprehensive health check endpoint
    
    Returns the status of the API and database connectivity
    """
    return db_manager.health_check()

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Actions to perform on application startup"""
    print("🚀 Starting E-commerce API...")
    print(f"📊 Database status: {'Connected' if db_manager.is_connected() else 'Disconnected'}")

@app.on_event("shutdown")
async def shutdown_event():
    """Actions to perform on application shutdown"""
    print("🛑 Shutting down E-commerce API...")
    if db_manager.client:
        db_manager.client.close()
        print("📊 Database connection closed")

if __name__ == "__main__":
    import uvicorn
    print("🔧 Starting development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )