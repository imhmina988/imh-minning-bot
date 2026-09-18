import os
import time
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# Temporary in-memory data
users = {}

MINING_RATE_PER_HOUR = 10


def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "mining": False,
            "started_at": None,
        }
    return users[user_id]


def calculate_balance(user):
    balance = user["balance"]

    if user["mining"] and user["started_at"]:
        elapsed = time.time() - user["started_at"]
        hours = elapsed / 3600
        balance += hours * MINING_RATE_PER_HOUR

    return balance


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)

    await update.message.reply_text(
        "⛏️ Welcome to IMH MINNING!\n\n"
        "💰 Mining rate: +10 coins/hour\n\n"
        "Use /mining to start mining.\n"
        "Use /balance to check your balance."
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    current_balance = calculate_balance(user)

    await update.message.reply_text(
        f"💰 Your Balance\n\n"
        f"🪙 {current_balance:.2f} Coins"
    )


async def mining(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if user["mining"]:
        current_balance = calculate_balance(user)

        await update.message.reply_text(
            f"⛏️ Mining is already active!\n\n"
            f"🪙 Balance: {current_balance:.2f} Coins\n"
            f"⚡ Rate: +10 coins/hour"
        )
        return

    user["mining"] = True
    user["started_at"] = time.time()

    await update.message.reply_text(
        "⛏️ Mining started!\n\n"
        "⚡ Rate: +10 coins/hour\n"
        "💰 Keep mining to earn coins."
    )


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 Deposit\n\n"
        "Deposit system will be added soon."
    )


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 Withdraw\n\n"
        "Withdrawal system will be added soon."
    )


async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👥 Referral\n\n"
        "Referral system will be added soon."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 IMH MINNING Help\n\n"
        "/start - Start bot\n"
        "/balance - Check balance\n"
        "/mining - Start mining\n"
        "/deposit - Deposit\n"
        "/withdraw - Withdraw\n"
        "/referral - Referral\n"
        "/help - Help"
    )


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("mining", mining))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("help", help_command))

    print("IMH MINNING bot is running...")

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
