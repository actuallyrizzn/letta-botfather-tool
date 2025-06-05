# Activate virtual environment if it exists
if (Test-Path "venv") {
    Write-Host "Activating virtual environment..."
    .\venv\Scripts\Activate.ps1
}

# Install test dependencies if needed
Write-Host "Installing test dependencies..."
pip install -r requirements.txt

# Run tests with coverage
Write-Host "Running tests..."
pytest tests/ -v --cov=botfather_relay --cov-report=term-missing --cov-report=html --no-cov-on-fail

# Check if tests passed
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAll tests passed successfully! 🎉" -ForegroundColor Green
} else {
    Write-Host "`nSome tests failed. Please check the output above. ❌" -ForegroundColor Red
    exit 1
} 