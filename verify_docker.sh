#!/bin/bash

echo "=================================="
echo "🔍 Docker Environment Verification"
echo "=================================="
echo ""

# Check if Docker is running
echo "1️⃣  Checking Docker..."
if docker info > /dev/null 2>&1; then
    echo "   ✅ Docker is running"
else
    echo "   ❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if containers are running
echo ""
echo "2️⃣  Checking containers..."
if docker-compose ps | grep -q "Up"; then
    echo "   ✅ Containers are running"
    docker-compose ps
else
    echo "   ⚠️  No containers running. Start with: docker-compose up"
fi

# Check backend health
echo ""
echo "3️⃣  Checking backend health..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Backend is healthy"
    curl -s http://localhost:8000/health | python -m json.tool
else
    echo "   ⚠️  Backend not responding at http://localhost:8000"
fi

# Check database tables
echo ""
echo "4️⃣  Checking database tables..."
if curl -s http://localhost:8000/debug/tables > /dev/null 2>&1; then
    echo "   ✅ Database tables endpoint accessible"
    curl -s http://localhost:8000/debug/tables | python -m json.tool | grep -E "(actual_count|status|message)"
else
    echo "   ⚠️  Cannot check database tables"
fi

# Check products
echo ""
echo "5️⃣  Checking products..."
PRODUCT_COUNT=$(curl -s http://localhost:8000/api/san-pham | python -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ ! -z "$PRODUCT_COUNT" ]; then
    echo "   ✅ Found $PRODUCT_COUNT products"
else
    echo "   ⚠️  Cannot fetch products"
fi

echo ""
echo "=================================="
echo "📊 Summary"
echo "=================================="
echo "Backend API: http://localhost:8000/docs"
echo "pgAdmin: http://localhost:5050"
echo "Health Check: http://localhost:8000/health"
echo "=================================="
