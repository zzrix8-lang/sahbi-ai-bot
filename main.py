import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# IMPORT HANDLERS
# =========================

from handlers.start import start

from handlers.download import handle_download

from handlers.files import handle_files

from handlers.study import handle_study

from handlers.tools import handle_tools

from handlers.fun import handle_fun

from handlers.documents import handle_documents

# =========================
# TOKEN
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# MAIN MESSAGE HANDLER
# =========================

async def all_messages(update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    # التحميل
    await handle_download(update, context)

    # الملفات
    if update.message.document:
        await handle_files(update, context)

    # الدراسة
    await handle_study(update, context)

    # الأدوات
    await handle_tools(update, context)

    # الترفيه
    await handle_fun(update, context)

    # المستندات
    await handle_documents(update, context)

# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # START
    app.add_handler(
        CommandHandler("start", start)
    )

    # ALL MESSAGES
    app.add_handler(
        MessageHandler(
            filters.ALL,
            all_messages
        )
    )

    print("🔥 SAHBI AI BOT STARTED")

    app.run_polling(drop_pending_updates=True)

# =========================

if __name__ == "__main__":
    main()
