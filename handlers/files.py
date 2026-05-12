import os
import zipfile

from telegram import Update
from telegram.ext import ContextTypes

# =========================
# UNZIP FILE
# =========================

async def unzip_file(update: Update, file_path: str):

    try:

        extract_folder = "extracted"

        os.makedirs(
            extract_folder,
            exist_ok=True
        )

        with zipfile.ZipFile(file_path, "r") as zip_ref:

            zip_ref.extractall(extract_folder)

        files = os.listdir(extract_folder)

        if not files:

            await update.message.reply_text(
                "❌ الملف فارغ."
            )

            return

        for file in files:

            full_path = os.path.join(
                extract_folder,
                file
            )

            if os.path.isfile(full_path):

                with open(full_path, "rb") as f:

                    await update.message.reply_document(f)

        # حذف الملفات بعد الإرسال
        os.remove(file_path)

        for file in files:

            os.remove(
                os.path.join(
                    extract_folder,
                    file
                )
            )

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ:\n{str(e)}"
        )

# =========================
# HANDLE FILES
# =========================

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document:
        return

    file_name = document.file_name.lower()

    # ZIP
    if file_name.endswith(".zip"):

        telegram_file = await document.get_file()

        file_path = file_name

        await telegram_file.download_to_drive(file_path)

        await update.message.reply_text(
            "📦 جاري فك الضغط..."
        )

        await unzip_file(update, file_path)

    else:

        await update.message.reply_text(
            "❌ هذا النوع غير مدعوم حالياً."
        )
