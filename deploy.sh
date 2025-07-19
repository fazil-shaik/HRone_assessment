#!/bin/bash
# Deployment script for E-commerce API

echo "🚀 E-commerce API Deployment Script"
echo "===================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "shaik" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv shaik
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source shaik/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables (for production)
echo "🔐 Setting up environment variables..."
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=ecommerce

# For production deployment, replace with your MongoDB Atlas connection string
# MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
EOL
fi

# Check if MongoDB is accessible
echo "🗄️ Checking database connection..."
python3 -c "
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

try:
    client = MongoClient(os.getenv('MONGODB_URL'), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('✅ Database connection successful!')
except Exception as e:
    print(f'⚠️ Database connection failed: {e}')
    print('💡 Make sure to update MONGODB_URL in .env for production')
"

echo ""
echo "🎯 Deployment completed!"
echo ""
echo "To start the server:"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Or for development:"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "API Documentation:"
echo "  http://localhost:8000/docs"
echo "  http://localhost:8000/redoc"
echo ""
