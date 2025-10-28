#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Welcome Bot
Automated welcome message bot for new group members
"""

import logging
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import ChatMemberHandler, ChatJoinRequestHandler
from telegram.error import TelegramError
import json
from datetime import datetime
from dotenv import load_dotenv

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class WelcomeBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        # Hardcoded welcome message for Barbwire Delivery
        self.welcome_message = """Welcome to Barbwire Delivery.
Where exclusive drops hit first, and next-day delivery is only a message away.

🚚Follow the steps below to place your first order.

Step 1: Create your account to receive your Customer ID
New Customer Form (https://barbwireba.fillout.com/t/1MwqDfyiZUus)

Step 2: View the menu and choose your products
https://barbwireba.fillout.com/t/7sWZFFiGzPus

Step 3: Pay using one of the options below.
Zelle: @barbwire or 516-774-7077
Venmo: @barbwireshop https://venmo.com/u/Ben-Gross-89
Cashapp: $barbwireshop https://cash.app/$barbwireshop

Once payment is received, your order will be shipped out the next day.
For any questions, reach out to customer service 848-224-3287"""
        
        self.bot = Bot(token=bot_token)
        self.application = Application.builder().token(bot_token).build()
        
        # Setup event handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup event handlers for the bot"""
        # New member join handler
        self.application.add_handler(
            MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_member)
        )
        
        # Chat member update handler (for join request approvals)
        self.application.add_handler(
            ChatMemberHandler(self.handle_chat_member_update)
        )
        
        # Chat join request handler (for auto-approving)
        self.application.add_handler(
            ChatJoinRequestHandler(self.handle_join_request)
        )
        
        # Start command handler
        self.application.add_handler(
            CommandHandler("start", self.start_command)
        )
        
        # Help command handler
        self.application.add_handler(
            CommandHandler("help", self.help_command)
        )
        
        # Status command handler
        self.application.add_handler(
            CommandHandler("status", self.status_command)
        )
        
        # Test command handler
        self.application.add_handler(
            CommandHandler("test", self.test_command)
        )
    
    async def handle_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message when new members join"""
        try:
            logger.info(f"New member event detected!")
            logger.info(f"Update: {update}")
            
            if not update.message or not update.message.new_chat_members:
                logger.warning("No new members found in update")
                return
                
            new_members = update.message.new_chat_members
            logger.info(f"Found {len(new_members)} new members")
            
            for member in new_members:
                logger.info(f"Processing member: {member.first_name} (ID: {member.id})")
                
                # Don't send welcome message to the bot itself
                try:
                    bot_info = await self.bot.get_me()
                    if member.id == bot_info.id:
                        logger.info("Skipping bot itself")
                        continue
                except Exception as e:
                    logger.warning(f"Could not get bot info: {e}")
                
                # Try to send private message first
                try:
                    logger.info(f"Attempting to send private message to {member.first_name}")
                    await context.bot.send_message(
                        chat_id=member.id,
                        text=self.welcome_message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    logger.info(f"✅ Welcome message sent to {member.first_name} (ID: {member.id})")
                    
                except TelegramError as e:
                    logger.warning(f"❌ Could not send private message to {member.first_name}: {e}")
                    
                    # If private message fails, send to group
                    try:
                        logger.info(f"Attempting to send group message for {member.first_name}")
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"Welcome {member.first_name}! 🎉\n\n{self.welcome_message}",
                            parse_mode='HTML',
                            disable_web_page_preview=True
                        )
                        logger.info(f"✅ Welcome message sent to group for {member.first_name}")
                    except TelegramError as group_error:
                        logger.error(f"❌ Could not send welcome message to group: {group_error}")
                        
        except Exception as e:
            logger.error(f"❌ Error handling new member: {e}")
            logger.error(f"Exception details: {str(e)}")
    
    async def handle_chat_member_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle chat member updates (join requests, approvals)"""
        try:
            # Get chat member update from context
            chat_member = update.chat_member
            
            # Check if someone was promoted to member (approved join request)
            new_status = chat_member.new_chat_member.status
            old_status = chat_member.old_chat_member.status
            
            # When join request is approved (was left/restricted, now member)
            if old_status in ['left', 'kicked', 'restricted'] and new_status == 'member':
                user = chat_member.new_chat_member.user
                
                logger.info(f"Join request approved for {user.first_name} (ID: {user.id})")
                
                # Don't send to bot itself
                try:
                    bot_info = await self.bot.get_me()
                    if user.id == bot_info.id:
                        return
                except:
                    pass
                
                # Send welcome message privately
                try:
                    logger.info(f"Sending welcome message to approved member {user.first_name}")
                    await context.bot.send_message(
                        chat_id=user.id,
                        text=self.welcome_message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    logger.info(f"✅ Welcome message sent to {user.first_name} after approval")
                except TelegramError as e:
                    logger.warning(f"❌ Could not send private message to {user.first_name}: {e}")
                    
                    # If private message fails, send to group
                    try:
                        logger.info(f"Attempting to send group message for {user.first_name}")
                        await context.bot.send_message(
                            chat_id=chat_member.chat.id,
                            text=f"Welcome {user.first_name}! 🎉\n\n{self.welcome_message}",
                            parse_mode='HTML',
                            disable_web_page_preview=True
                        )
                        logger.info(f"✅ Welcome message sent to group for {user.first_name}")
                    except TelegramError as group_error:
                        logger.error(f"❌ Could not send welcome message to group: {group_error}")
                    
        except Exception as e:
            logger.error(f"Error handling chat member update: {e}")
    
    async def handle_join_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle join requests and auto-approve them"""
        try:
            chat_join_request = update.chat_join_request
            user = chat_join_request.from_user
            
            logger.info(f"Join request received from {user.first_name} (ID: {user.id})")
            
            # Auto-approve the join request
            try:
                await context.bot.approve_chat_join_request(
                    chat_id=chat_join_request.chat.id,
                    user_id=user.id
                )
                logger.info(f"✅ Auto-approved join request from {user.first_name}")
                
                # Send welcome message after approval
                try:
                    await context.bot.send_message(
                        chat_id=user.id,
                        text=self.welcome_message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    logger.info(f"✅ Welcome message sent to {user.first_name}")
                except TelegramError as e:
                    logger.warning(f"❌ Could not send private message to {user.first_name}: {e}")
                    
            except TelegramError as e:
                logger.error(f"❌ Could not approve join request for {user.first_name}: {e}")
                
        except Exception as e:
            logger.error(f"Error handling join request: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        await update.message.reply_text(
            "🤖 <b>Telegram Welcome Bot</b>\n\n"
            "I automatically send welcome messages to new group members.\n\n"
            "Commands:\n"
            "/help - Help\n"
            "/status - Bot status\n\n"
            "Bot is active! ✅",
            parse_mode='HTML'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        await update.message.reply_text(
            "📋 <b>Help</b>\n\n"
            "This bot automatically sends welcome messages to new group members.\n\n"
            "🔧 <b>Setup:</b>\n"
            "1. Add bot to your group as admin\n"
            "2. Give 'Add new members' permission\n"
            "3. Bot will start working automatically\n\n"
            "💬 <b>Commands:</b>\n"
            "/start - Start the bot\n"
            "/status - Check bot status\n"
            "/help - This help message\n\n"
            "❓ <b>Troubleshooting:</b>\n"
            "• Bot won't work if not admin\n"
            "• If private messages are blocked, will send to group",
            parse_mode='HTML'
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Status command handler"""
        try:
            bot_info = await self.bot.get_me()
            await update.message.reply_text(
                f"🤖 <b>Bot Status</b>\n\n"
                f"Name: {bot_info.first_name}\n"
                f"Username: @{bot_info.username}\n"
                f"ID: {bot_info.id}\n"
                f"Status: Active ✅\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                parse_mode='HTML'
            )
        except Exception as e:
            await update.message.reply_text(f"Error checking status: {e}")
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test command handler"""
        try:
            await update.message.reply_text(
                f"🧪 <b>Bot Test</b>\n\n"
                f"Welcome message preview:\n\n"
                f"{self.welcome_message}",
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            logger.info("Test command executed successfully")
        except Exception as e:
            await update.message.reply_text(f"Test error: {e}")
            logger.error(f"Test command error: {e}")
    
    def run(self):
        """Run the bot"""
        logger.info("Starting bot...")
        self.application.run_polling(drop_pending_updates=True)

def load_config():
    """Load configuration from .env file"""
    try:
        # Load .env file
        load_dotenv()
        
        # Get bot token from environment variables
        bot_token = os.getenv('BOT_TOKEN')
        
        # Check if bot token is set
        if not bot_token:
            logger.error("BOT_TOKEN not found in .env file!")
            return None
            
        return {'bot_token': bot_token}
        
    except Exception as e:
        logger.error(f"Error loading .env file: {e}")
        return None

def main():
    """Main function"""
    print("🤖 Telegram Welcome Bot")
    print("=" * 30)
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Could not load configuration!")
        print("Create .env file with correct information.")
        return
    
    # Check required information
    bot_token = config.get('bot_token')
    
    if not bot_token:
        print("❌ BOT_TOKEN not found in .env file!")
        return
    
    # Create and run bot
    try:
        bot = WelcomeBot(bot_token)
        print("✅ Bot created successfully!")
        print("✅ Welcome message is hardcoded in the bot!")
        print("Starting bot... (Press Ctrl+C to stop)")
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped!")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == "__main__":
    main()
