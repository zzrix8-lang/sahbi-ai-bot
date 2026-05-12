import os
import yt_dlp
import random
import asyncio
from datetime import datetime

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

# ====================================
# معلومات البوت
# ====================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

BOT_NAME = "SAHBI AI"
DEVELOPER = "@n5w_n"

CHANNEL_URL = "https://t.me/awes_anshed"

# ====================================
# القائمة الرئيسية
# ====================================

def main_menu():

    keyboard = [

        [InlineKeyboardButton("📥 قسم التحميل", callback_data="download")],

        [InlineKeyboardButton("📁 قسم الملفات", callback_data="files")],

        [InlineKeyboardButton("📚 قسم الدراسة", callback_data="study")],

        [InlineKeyboardButton("🛠️ قسم الأدوات", callback_data="tools")],

        [InlineKeyboardButton("🎮 قسم الترفيه", callback_data="fun")],

        [InlineKeyboardButton("🖨️ صانع المستندات", callback_data="docs")],

        [
            InlineKeyboardButton(
                "📢 اشترك بالقناة",
                url=CHANNEL_URL
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

# ====================================
# START
# ====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
🔥 أهلاً بك في {BOT_NAME}

━━━━━━━━━━━━━━━

📥 تحميل فيديوهات
📁 أدوات ملفات
📚 أدوات دراسة
🛠️ أدوات يومية
🎮 ترفيه وألعاب
🖨️ إنشاء مستندات

━━━━━━━━━━━━━━━

👨‍💻 المطور:
{DEVELOPER}
"""

    await update.message.reply_text(
        text=text,
        reply_markup=main_menu()
    )

# ====================================
# الأزرار
# ====================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    # ====================================
    # التحميل
    # ====================================

    if query.data == "download":

        text = """
📥 قسم التحميل

✅ TikTok
✅ Instagram
✅ YouTube
✅ Facebook
✅ Twitter / X

📌 أرسل الرابط مباشرة للتحميل.
"""

        await query.message.reply_text(text)

    # ====================================
    # الملفات
    # ====================================

    elif query.data == "files":

        text = """
📁 قسم الملفات

📄 PDF ↔ Word
🖼️ PNG ↔ JPG
📦 فك ضغط ZIP
🗜️ ضغط ملفات
📚 دمج PDF

📌 أرسل الملف المطلوب.
"""

        await query.message.reply_text(text)

    # ====================================
    # الدراسة
    # ====================================

    elif query.data == "study":

        text = """
📚 قسم الدراسة

📸 حل أسئلة
📝 تلخيص دروس
📖 ترجمة
🧮 حاسبة
🎤 صوت → نص
🔊 نص → صوت
📅 خطة دراسة
🧠 اختبارات قصيرة
"""

        await query.message.reply_text(text)

    # ====================================
    # الأدوات
    # ====================================

    elif query.data == "tools":

        text = """
🛠️ قسم الأدوات

🌦️ الطقس
💱 تحويل العملات
🔗 اختصار روابط
🔐 توليد كلمات سر
📅 التاريخ الهجري
🧾 QR Code

📌 أوامر:
- باسورد
- وقت
- نكتة
"""

        await query.message.reply_text(text)

    # ====================================
    # الترفيه
    # ====================================

    elif query.data == "fun":

        text = """
🎮 قسم الترفيه

😂 نكت
🎲 ألعاب
🧠 ألغاز
🪙 قرعة
🎁 مكافآت
"""

        await query.message.reply_text(text)

    # ====================================
    # المستندات
    # ====================================

    elif query.data == "docs":

        text = """
🖨️ صانع المستندات

📅 جدول حصص
📝 ورقة امتحان
📊 كشف علامات
📋 حضور وغياب
📄 أوراق واجبات

📌 أرسل النص المطلوب.
"""

        await query.message.reply_text(text)

# ====================================
# تحميل الفيديو
# ====================================

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
                    caption=f"""
✅ تم التحميل بنجاح

👨‍💻 المطور:
{DEVELOPER}

📢 القناة:
{CHANNEL_URL}
"""
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

# ====================================
# الأدوات
# ====================================

async def tools_system(update: Update, text: str):

    # ====================================
    # باسورد
    # ====================================

    if text.lower() == "باسورد":

        password = ''.join(
            random.choice(
                "abcdefghijklmnopqrstuvwxyz123456789"
            ) for _ in range(12)
        )

        await update.message.reply_text(
            f"🔐 كلمة السر:\n{password}"
        )

    # ====================================
    # نكتة
    # ====================================

    elif text.lower() == "نكتة":

        jokes = [

            "😂 المدرس: أين الواجب؟ الطالب: في مرحلة انتقالية.",

            "😂 طالب قال للمعلم: القلم ما يكتب. قاله: جرب تدرسه.",

            "😂 واحد فتح الثلاجة شاف اللبن زعلان قاله: منتهي الصلاحية."
        ]

        await update.message.reply_text(
            random.choice(jokes)
        )

    # ====================================
    # الوقت
    # ====================================

    elif text.lower() == "وقت":

        now = datetime.now().strftime("%H:%M:%S")

        await update.message.reply_text(
            f"🕓 الوقت الآن:\n{now}"
        )

    # ====================================
    # قرعة
    # ====================================

    elif text.lower() == "قرعة":

        result = random.choice([
            "✅ نعم",
            "❌ لا"
        ])

        await update.message.reply_text(
            f"🪙 النتيجة:\n{result}"
        )

    # ====================================
    # رسالة افتراضية
    # ====================================

    else:

        await update.message.reply_text(
            """
❌ الأمر غير معروف.

📌 جرّب:
- نكتة
- باسورد
- وقت
- قرعة
"""
        )

# ====================================
# استقبال الرسائل
# ====================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if not update.message.text:
        return

    text = update.message.text

    # ====================================
    # روابط تحميل
    # ====================================

    if any(keyword in text for keyword in [

        "tiktok.com",
        "instagram.com",
        "youtube.com",
        "youtu.be",
        "facebook.com",
        "twitter.com",
        "x.com"

    ]):

        await download_video(update, text)

    else:

        await tools_system(update, text)

# ====================================
# HELP
# ====================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
📌 أوامر البوت

/start - تشغيل البوت
/help - المساعدة

━━━━━━━━━━━━━━━

📥 أرسل رابط فيديو للتحميل

🛠️ أوامر مفيدة:
- نكتة
- وقت
- باسورد
- قرعة

━━━━━━━━━━━━━━━

👨‍💻 المطور:
{DEVELOPER}
"""

    await update.message.reply_text(text)

# ====================================
# الأخطاء
# ====================================

async def error_handler(update, context):

    print(f"ERROR: {context.error}")

# ====================================
# MAIN
# ====================================

def main():

    if not BOT_TOKEN:

        print("❌ BOT_TOKEN غير موجود")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ====================================
    # HANDLERS
    # ====================================

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CallbackQueryHandler(buttons)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_error_handler(error_handler)

    print("🔥 SAHBI AI BOT STARTED")

    app.run_polling(drop_pending_updates=True)

# ====================================

if __name__ == "__main__":
    main()
