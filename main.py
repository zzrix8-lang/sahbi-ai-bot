from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from handlers.start import start

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # START
    app.add_handler(CommandHandler("start", start))

    print("🔥 SAHBI AI BOT STARTED")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
