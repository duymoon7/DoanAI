# Docker Environment Verification Script for Windows

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🔍 Docker Environment Verification" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "1️⃣  Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "   ✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if containers are running
Write-Host ""
Write-Host "2️⃣  Checking containers..." -ForegroundColor Yellow
$containers = docker-compose ps
if ($containers -match "Up") {
    Write-Host "   ✅ Containers are running" -ForegroundColor Green
    docker-compose ps
} else {
    Write-Host "   ⚠️  No containers running. Start with: docker-compose up" -ForegroundColor Yellow
}

# Check backend health
Write-Host ""
Write-Host "3️⃣  Checking backend health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "   ✅ Backend is healthy" -ForegroundColor Green
    $health | ConvertTo-Json
} catch {
    Write-Host "   ⚠️  Backend not responding at http://localhost:8000" -ForegroundColor Yellow
}

# Check database tables
Write-Host ""
Write-Host "4️⃣  Checking database tables..." -ForegroundColor Yellow
try {
    $tables = Invoke-RestMethod -Uri "http://localhost:8000/debug/tables" -Method Get
    Write-Host "   ✅ Database tables endpoint accessible" -ForegroundColor Green
    Write-Host "   Tables: $($tables.actual_count)" -ForegroundColor Cyan
    Write-Host "   Status: $($tables.status)" -ForegroundColor Cyan
    Write-Host "   Message: $($tables.message)" -ForegroundColor Cyan
} catch {
    Write-Host "   ⚠️  Cannot check database tables" -ForegroundColor Yellow
}

# Check products
Write-Host ""
Write-Host "5️⃣  Checking products..." -ForegroundColor Yellow
try {
    $products = Invoke-RestMethod -Uri "http://localhost:8000/api/san-pham" -Method Get
    Write-Host "   ✅ Found $($products.Count) products" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Cannot fetch products" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "📊 Summary" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "pgAdmin: http://localhost:5050" -ForegroundColor White
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host "==================================" -ForegroundColor Cyan
