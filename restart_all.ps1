# Script restart backend va frontend

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "RESTART BACKEND VA FRONTEND" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan

# Kiem tra thu muc hien tai
$currentDir = Get-Location
Write-Host "`nThu muc hien tai: $currentDir" -ForegroundColor Gray

# Di chuyen den thu muc AI-Shop neu can
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    if (Test-Path "AI-Shop") {
        Set-Location AI-Shop
        Write-Host "Da chuyen den thu muc AI-Shop" -ForegroundColor Gray
    }
}

Write-Host "`n[1/2] KHOI DONG BACKEND..." -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Gray
Write-Host ("=" * 79) -ForegroundColor Gray

# Kiem tra backend co ton tai khong
if (-not (Test-Path "backend")) {
    Write-Host "Loi: Khong tim thay thu muc backend!" -ForegroundColor Red
    exit 1
}

# Khoi dong backend
Set-Location backend
Write-Host "Dang khoi dong backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 3

Write-Host "`n[2/2] KHOI DONG FRONTEND..." -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Gray
Write-Host ("=" * 79) -ForegroundColor Gray

# Quay lai thu muc goc
Set-Location ..

# Kiem tra frontend co ton tai khong
if (-not (Test-Path "frontend")) {
    Write-Host "Loi: Khong tim thay thu muc frontend!" -ForegroundColor Red
    exit 1
}

# Khoi dong frontend
Set-Location frontend
Write-Host "Dang khoi dong frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
Start-Sleep -Seconds 3

# Quay lai thu muc goc
Set-Location ..

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 79) -ForegroundColor Green
Write-Host "HOAN TAT!" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 79) -ForegroundColor Green

Write-Host "`nDa khoi dong thanh cong:" -ForegroundColor Green
Write-Host "  - Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host "`nLuu y:" -ForegroundColor Yellow
Write-Host "  - 2 cua so PowerShell moi da duoc mo" -ForegroundColor Gray
Write-Host "  - Nhan Ctrl+C trong cua so do de dung server" -ForegroundColor Gray
Write-Host "  - Doi 10-15 giay de server khoi dong hoan toan" -ForegroundColor Gray

Write-Host "`nMo trinh duyet:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000/products" -ForegroundColor Cyan

Write-Host "`n"
