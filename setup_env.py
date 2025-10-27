#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Welcome Bot Setup Script with .env file
"""

import os
import subprocess
import sys

def print_banner():
    """Print banner"""
    print("🤖" + "="*50)
    print("    Telegram Welcome Bot Setup (.env)")
    print("="*52)
    print()

def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file"""
    print("\n⚙️ Setting up .env file...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("📄 .env file already exists!")
        return True
    
    # Create .env file from template
    env_content = """# Telegram Bot Configuration
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Group Information
GROUP_CHAT_ID=@BarbwireSmoke
GROUP_LINK=https://t.me/BarbwireSmoke

# Welcome Message
WELCOME_MESSAGE=Welcome to Barbwire Delivery.
Where exclusive drops hit first, and next-day delivery is only a message away.

🚚Follow the steps below to place your first order.

Step 1: Create your account to receive your Customer ID
New Customer Form

Step 2: View the menu and choose your products
https://barbwireba.fillout.com/t/7sWZFFiGzPus

Step 3: Pay using one of the options from the link below.
Once payment is received, your order will be shipped out the next day.

For any questions, reach out to customer service 848-224-3287

# Bot Settings
BOT_NAME=Barbwire Welcome Bot
BOT_USERNAME=@barbwire_welcome_bot
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def setup_bot_token():
    """Setup bot token"""
    print("\n🔑 Bot token setup...")
    
    # Check if bot token is already set
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'YOUR_BOT_TOKEN_HERE' not in content:
        print("✅ Bot token already set!")
        return True
    
    print("Bot token setup required!")
    print("1. Go to @BotFather")
    print("2. Use /newbot command")
    print("3. Enter bot name and username")
    print("4. Copy the bot token")
    
    new_token = input("\nEnter bot token: ").strip()
    if new_token:
        # Replace token in .env file
        content = content.replace('YOUR_BOT_TOKEN_HERE', new_token)
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Bot token saved!")
        return True
    else:
        print("❌ No bot token provided!")
        return False

def show_next_steps():
    """Show next steps"""
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Add bot to your Telegram group")
    print("2. Make bot admin")
    print("3. Give 'Add new members' permission")
    print("4. Run bot: python telegram_welcome_bot.py")
    print("\n💡 Read README.md for help!")

def main():
    """Main function"""
    print_banner()
    
    # Check Python version
    if not check_python():
        return
    
    # Install packages
    if not install_requirements():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Setup bot token
    if not setup_bot_token():
        return
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled!")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
