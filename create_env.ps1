Write-Host "Creating .env file..." -ForegroundColor Green
Copy-Item "env_config.txt" ".env"
Write-Host ".env file created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Now run: python telegram_welcome_bot.py" -ForegroundColor Yellow
