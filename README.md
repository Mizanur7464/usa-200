# 🤖 Telegram Welcome Bot

An automated Telegram bot that sends welcome messages to new group members.

## ✨ Features

- 🎯 Automatic welcome messages for new members
- 💬 Private message delivery (when possible)
- 🔄 Fallback to group message if private messaging fails
- 🛠️ Easy configuration
- 📱 Full English language support
- 🔧 Multiple command support

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### 2. Create Bot

1. Go to [@BotFather](https://t.me/BotFather)
2. Use `/newbot` command
3. Enter bot name (e.g., "My Welcome Bot")
4. Enter username (e.g., "my_welcome_bot")
5. Copy the bot token

### 3. Project Setup

```bash
# 1. Navigate to project folder
cd "C:\Users\User\Desktop\Project\welcome message group bot"

# 2. Install required packages
pip install -r requirements.txt

# 3. Edit configuration file
# Add your bot token in config.json
```

### 4. Configuration

**Option 1: Using .env file (Recommended)**
```bash
python setup_env.py
```

**Option 2: Manual .env setup**
Create a `.env` file with your information:

```env
# Telegram Bot Configuration
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Group Information
GROUP_CHAT_ID=@YourGroupUsername
GROUP_LINK=https://t.me/YourGroupUsername

# Welcome Message
WELCOME_MESSAGE=Your welcome message here

# Bot Settings
BOT_NAME=Your Bot Name
BOT_USERNAME=@your_bot_username
```

**Example:**
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GROUP_CHAT_ID=@BarbwireSmoke
GROUP_LINK=https://t.me/BarbwireSmoke
WELCOME_MESSAGE=Welcome to our group!
```

### 5. Run Bot

```bash
python telegram_welcome_bot.py
```

## 🔧 Group Setup

### 1. Add Bot to Group

1. Go to your Telegram group
2. Group Settings → Admins → Add Admin
3. Find your bot and add it

### 2. Give Required Permissions

- ✅ **Add new members** - Permission to add new members
- ✅ **Delete messages** - Permission to delete messages (optional)
- ✅ **Ban users** - Permission to ban users (optional)

### 3. Activate Bot

Once you run the bot, it will automatically start sending welcome messages to new members.

## 📋 Commands

You can use these commands by chatting with the bot:

- `/start` - Start the bot
- `/help` - Show help
- `/status` - Check bot status

## ⚙️ Customization

### Change Welcome Message

Edit the `welcome_message` in `config.json`:

```json
{
  "welcome_message": "Your new welcome message"
}
```

### HTML Formatting

You can use HTML tags in your welcome message:

- `<b>Bold Text</b>` - Bold
- `<i>Italic Text</i>` - Italic
- `<u>Underline Text</u>` - Underline
- `\n` - New line

**Example:**
```json
{
  "welcome_message": "🎉 <b>Welcome!</b> 🎉\n\nThanks for <i>joining our group!</i>\n\n📋 <b>Rules:</b>\n• Respect everyone\n• No spam"
}
```

## 🐛 Troubleshooting

### Bot Not Working

1. **Check if bot token is correct**
2. **Check if bot is admin in group**
3. **Check if "Add new members" permission is given**
4. **Check internet connection**

### Private Messages Not Working

- This is normal! Many users have private messages disabled
- Bot will automatically send message to group instead

### View Logs

You can see log messages in the console. Check logs if there are issues.

## 📁 File Structure

```
welcome message group bot/
├── telegram_welcome_bot.py    # Main bot code
├── config.json                # Configuration file
├── requirements.txt           # Python packages
├── setup.py                   # Easy setup script
└── README.md                  # This file
```

## 🔒 Security

- Never share your bot token
- Add `config.json` to `.gitignore`
- Update with new token if bot token changes

## 📞 Help

If you have issues:
1. Read this README again
2. Check log messages
3. Check bot permissions

## 🎉 Success!

Your Telegram Welcome Bot is now ready! New members will automatically receive welcome messages when they join the group.

---

**Like it? Give it a ⭐!**