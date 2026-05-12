import os
import yt_dlp
import asyncio
import google.generativeai as genai

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# التوكنات
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# إعداد Gemini
# =========================

genai.configure(api_key=GEMINI_API_KEY)

# ✅ الموديل الجديد
model = genai.GenerativeModel("gemini-2.0-flash")

# =========================
# معلومات البوت
# =========================

BOT_NAME = "Sahbi AI"
DEVELOPER = "@n5w_n"

# =========================
# /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🤖 الذكاء الاصطناعي", callback_data="ai")],
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="download")],
        [InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")],
        [
            InlineKeyboardButton(
                "👨‍💻 المطور",
                url=f"https://t.me/{DEVELOPER.replace('@', '')}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""
🔥 أهلاً بك في {BOT_NAME}

مساعدك العربي الذكي 🚀

━━━━━━━━━━━━━━━

✅ ذكاء اصطناعي
✅ تحميل فيديو

━━━━━━━━━━━━━━━

👨‍💻 المطور:
{DEVELOPER}
"""

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )

# =========================
# الأزرار
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "ai":

        await query.message.reply_text(
            "🤖 أرسل أي سؤال وسأجيبك مباشرة."
        )

    elif query.data == "download":

        await query.message.reply_text(
            "📥 أرسل رابط TikTok أو Instagram أو YouTube."
        )

    elif query.data == "help":

        await query.message.reply_text(
            f"""
ℹ️ طريقة الاستخدام:

• أرسل أي سؤال للذكاء الاصطناعي
• أو أرسل رابط فيديو للتحميل

👨‍💻 المطور:
{DEVELOPER}
"""
        )

# =========================
# الذكاء الاصطناعي
# =========================

async def ai_response(update: Update, text: str):

    try:

        loading = await update.message.reply_text(
            "🤖 جاري التفكير..."
        )

        response = model.generate_content(text)

        answer = response.text

        await loading.delete()

        if not answer:
            answer = "❌ لم يتم الحصول على رد."

        # تقسيم الرد إذا كان طويل
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await update.message.reply_text(answer[i:i+4000])
        else:
            await update.message.reply_text(answer)

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ:\n{str(e)}"
        )

# =========================
# تحميل الفيديو
# =========================

async def download_video(update: Update, url: str):

    try:

        msg = await update.message.reply_text(
            "⏳ جاري تحميل الفيديو..."
        )

        ydl_opts = {
            "format": "mp4",
            "outtmpl": "video.%(ext)s",
            "quiet": True,
            "noplaylist": True
        }

        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(download)

        video_file = None

        for file in os.listdir():
            if file.endswith(".mp4"):
                video_file = file
                break

        if video_file:

            await msg.delete()

            with open(video_file, "rb") as video:

                await update.message.reply_video(
                    video=video,
                    caption=f"✅ تم التحميل بواسطة {BOT_NAME}"
                )

            os.remove(video_file)

        else:

            await update.message.reply_text(
                "❌ لم يتم العثور على الفيديو."
            )

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ أثناء التحميل:\n{str(e)}"
        )

# =========================
# استقبال الرسائل
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text

    if any(keyword in text for keyword in [
        "tiktok.com",
        "instagram.com",
        "youtube.com",
        "youtu.be"
    ]):

        await download_video(update, text)

    else:

        await ai_response(update, text)

# =========================
# /help
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"""
🔥 {BOT_NAME}

🤖 ذكاء اصطناعي
📥 تحميل فيديو

👨‍💻 المطور:
{DEVELOPER}
"""
    )

# =========================
# الأخطاء
# =========================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    print(f"ERROR: {context.error}")

# =========================
# تشغيل البوت
# =========================

def main():

    if not BOT_TOKEN:
        print("❌ BOT_TOKEN غير موجود")
        return

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY غير موجود")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CallbackQueryHandler(buttons))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_error_handler(error_handler)

    print("🔥 SAHBI AI BOT STARTED")

    app.run_polling(drop_pending_updates=True)

# =========================

if __name__ == "__main__":
    main()
