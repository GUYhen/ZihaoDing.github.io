# PowerShell script to compile jemdoc files to HTML
# Usage: Run ".\build.ps1" in PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compiling jemdoc files..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$files = @("index.jemdoc", "publications.jemdoc", "awards.jemdoc")
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

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compilation Summary:" -ForegroundColor Cyan
Write-Host "Success: $successCount files" -ForegroundColor Green
Write-Host "Failed: $failCount files" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan

