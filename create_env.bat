@echo off
echo Creating .env file with updated message format...
copy env_config.txt .env
echo .env file created successfully!
echo.
echo The message format has been fixed with proper HTML formatting.
echo Now run: python telegram_welcome_bot.py
echo.
echo Test the bot with /test command to see the updated format.
pause
