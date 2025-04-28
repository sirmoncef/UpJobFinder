from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from datetime import time
from scraper import get_latest_jobs  # Only Upwork jobs
from typing import List, Dict

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message"""
    await update.message.reply_text(
        "🐍 Python Jobs Bot (Upwork Only)\n\n"
        "Commands:\n"
        "/jobs - Get latest Upwork Python jobs\n"
        
    )

async def jobs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /jobs command with optional keyword"""
    try:
        search_query = "python"  # default
        if context.args:
            search_query = " ".join(context.args)  # if user typed something after /jobs
        
        await update.message.reply_text(f"🔍 Searching Upwork for jobs: {search_query}...")
        jobs = await get_latest_jobs(search_query)
        
        if not jobs:
            await update.message.reply_text("⚠️ No jobs found on Upwork")
            return
            
        await update.message.reply_text(
            format_jobs_message(jobs),
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def format_jobs_message(jobs: List[Dict]) -> str:
    message = "💼 Latest Upwork Python Jobs:\n\n"
    for i, job in enumerate(jobs[:10], 1):
        message += (
            f"{i}. <b>{job['title']}</b>\n"
            f"   ⏳ Posted: {job['posted']}\n"
            f"   💰 Budget: {job['budget']}\n"
            f"   ⏱ Duration: {job['duration']}\n"
            f"   🔗 <a href='{job['link']}'>View Job</a>\n\n"
        )
    return message

def main() -> None:
    """Start the bot"""
    app = Application.builder().token(TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", jobs_command))
   
    app.run_polling()


if __name__ == '__main__':
    main()