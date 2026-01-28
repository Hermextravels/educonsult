#!/bin/bash

# EduLearn Platform - Quick Start Script
# This script helps you get started with the EduLearn platform

set -e

echo "========================================"
echo "   EduLearn Platform - Quick Start"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
    echo ""
    echo "⚠️  Please edit backend/.env with your configuration:"
    echo "   - DATABASE_URL"
    echo "   - SECRET_KEY"
    echo "   - Payment gateway keys"
    echo "   - Email settings"
    echo ""
    read -p "Press Enter once you've configured backend/.env..."
fi

# Build containers
echo "🔨 Building Docker containers..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo ""
echo "⏳ Waiting for database to be ready..."
sleep 5

# Run migrations
echo "📊 Running database migrations..."
docker-compose exec -T backend alembic upgrade head

echo ""
echo "✅ All services are running!"
echo ""
echo "========================================"
echo "   Access Points"
echo "========================================"
echo ""
echo "Frontend:          http://localhost:3000"
echo "Backend API:       http://localhost:8000"
echo "API Docs:          http://localhost:8000/api/v1/docs"
echo ""
echo "========================================"
echo "   Quick Commands"
echo "========================================"
echo ""
echo "View logs:         docker-compose logs -f"
echo "Stop services:     docker-compose down"
echo "Restart services:  docker-compose restart"
echo "SSH to backend:    docker-compose exec backend bash"
echo ""
echo "========================================"
echo ""
echo "🎓 Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Create a new account or login"
echo "3. Start exploring the platform!"
echo ""
echo "For more information, see README.md"
echo ""
