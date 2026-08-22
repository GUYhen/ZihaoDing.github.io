# PowerShell script to compile jemdoc files to HTML
# Usage: Run ".\build.ps1" in PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compiling jemdoc files..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$files = @("index.jemdoc", "publications.jemdoc", "awards.jemdoc", "blog.jemdoc")
$successCount = 0
$failCount = 0

foreach ($file in $files) {
    Write-Host "Compiling $file..." -ForegroundColor Yellow

    try {
        python ..\jemdoc -c mysite.conf $file

        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Successfully compiled $file" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "[ERROR] Failed to compile $file" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "[ERROR] Failed to compile $file`: $_" -ForegroundColor Red
        $failCount++
    }

    Write-Host ""
}

# Blog posts live one level down and use blog\MENU + ..\jemdoc.css
$posts = Get-ChildItem -Path "blog" -Filter "*.jemdoc" | Where-Object { $_.Name -notlike "_*" }
foreach ($post in $posts) {
    Write-Host "Compiling blog/$($post.Name)..." -ForegroundColor Yellow
    Push-Location "blog"
    python ..\..\jemdoc -c ..\mysite.conf $post.Name
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Successfully compiled blog/$($post.Name)" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "[ERROR] Failed to compile blog/$($post.Name)" -ForegroundColor Red
        $failCount++
    }
    Pop-Location
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compilation Summary:" -ForegroundColor Cyan
Write-Host "Success: $successCount files" -ForegroundColor Green
Write-Host "Failed: $failCount files" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan

