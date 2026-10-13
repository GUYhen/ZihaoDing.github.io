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

# One folder per post under blog\. Built from docs\ with blogpost.conf, which
# only differs from mysite.conf in the favicon path. Folders starting with _
# are templates and are skipped.
$posts = Get-ChildItem -Path "blog" -Directory |
         Where-Object { $_.Name -notlike "_*" } |
         ForEach-Object { Get-ChildItem -Path $_.FullName -Filter "*.jemdoc" }
foreach ($post in $posts) {
    $rel = Join-Path "blog" (Join-Path $post.Directory.Name $post.Name)
    Write-Host "Compiling $rel..." -ForegroundColor Yellow
    python ..\jemdoc -c blogpost.conf $rel
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Successfully compiled $rel" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "[ERROR] Failed to compile $rel" -ForegroundColor Red
        $failCount++
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Compilation Summary:" -ForegroundColor Cyan
Write-Host "Success: $successCount files" -ForegroundColor Green
Write-Host "Failed: $failCount files" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan

