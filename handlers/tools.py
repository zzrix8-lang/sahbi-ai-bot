import random
import string

from telegram import Update
from telegram.ext import ContextTypes

# =========================
# PASSWORD GENERATOR
# =========================

async def generate_password(update: Update):

    chars = string.ascii_letters + string.digits

    password = "".join(
        random.choice(chars)
        for _ in range(12)
    )

    await update.message.reply_text(
        f"🔐 كلمة المرور:\n\n{password}"
    )

# =========================
# COIN FLIP
# =========================

async def flip_coin(update: Update):

    result = random.choice([
        "🪙 صورة",
        "🪙 كتابة"
    ])

    await update.message.reply_text(result)

# =========================
# RANDOM NUMBER
# =========================

async def random_number(update: Update):

    number = random.randint(1, 100)

    await update.message.reply_text(
        f"🎲 الرقم العشوائي:\n{number}"
    )

# =========================
# HANDLE TOOLS
# =========================

async def handle_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # باسورد
    if text == "🔐 توليد كلمة سر":

        await generate_password(update)

    # قرعة
    elif text == "🪙 قرعة":

        await flip_coin(update)

    # رقم عشوائي
    elif text == "🎲 رقم عشوائي":

        await random_number(update)
