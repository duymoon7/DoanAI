# Script khởi động hệ thống AI-Shop

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   AI-Shop Startup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Starting Backend..." -ForegroundColor Yellow
Write-Host "Backend will run at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the backend" -ForegroundColor Cyan
Write-Host ""

# Khởi động backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --reload"

# Đợi 3 giây để backend khởi động
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Step 2: Starting Frontend..." -ForegroundColor Yellow
Write-Host "Frontend will run at: http://localhost:3000" -ForegroundColor Green
Write-Host ""

# Khởi động frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "   System Started!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "Admin:    http://localhost:3000/admin" -ForegroundColor Green
Write-Host ""
Write-Host "Default Admin Account:" -ForegroundColor Yellow
Write-Host "  Email: admin@example.com" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
