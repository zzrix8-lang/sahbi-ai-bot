import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from handlers.start import start

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("🔥 SAHBI AI STARTED")

app.run_polling()
