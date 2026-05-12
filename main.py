import os
import openai
import yt_dlp

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

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

BOT_NAME = "Sahbi AI"
DEVELOPER = "@n5w_n"


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
✅ أدوات يومية

━━━━━━━━━━━━━━━

👨‍💻 المطور:
{DEVELOPER}
"""

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )


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


async def ai_response(update: Update, text: str):

    try:

        loading = await update.message.reply_text(
            "🤖 جاري التفكير..."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد عربي ذكي ومختصر."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        answer = response.choices[0].message.content

        await loading.delete()

        await update.message.reply_text(answer)

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ:\n{e}"
        )


async def download_video(update: Update, url: str):

    try:

        msg = await update.message.reply_text(
            "⏳ جاري تحميل الفيديو..."
        )

        ydl_opts = {
            "format": "mp4",
            "outtmpl": "video.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None

        for file in os.listdir():

            if file.endswith(".mp4"):
                video_file = file
                break

        if video_file:

            await msg.delete()

            await update.message.reply_video(
                video=open(video_file, "rb"),
                caption=f"""
✅ تم التحميل بواسطة {BOT_NAME}

👨‍💻 المطور:
{DEVELOPER}
"""
            )

            os.remove(video_file)

        else:

            await update.message.reply_text(
                "❌ لم يتم العثور على الفيديو."
            )

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ أثناء التحميل:\n{e}"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if (
        "tiktok.com" in text
        or "instagram.com" in text
        or "youtube.com" in text
        or "youtu.be" in text
    ):

        await download_video(update, text)

    else:

        await ai_response(update, text)


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


async def error_handler(update, context):

    print(f"ERROR: {context.error}")


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

app.run_polling()
