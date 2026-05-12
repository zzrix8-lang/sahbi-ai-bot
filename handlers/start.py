from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

BOT_NAME = "SAHBI AI"
DEVELOPER = "@n5w_n"

CHANNEL_URL = "https://t.me/awes_anshed"

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = f"""
🔥 أهلاً بك في {BOT_NAME}

━━━━━━━━━━━━━━━

📥 تحميل فيديوهات
📁 أدوات ملفات
📚 أدوات دراسية
🛠️ أدوات يومية
🎮 ترفيه وألعاب
🖨️ إنشاء مستندات

━━━━━━━━━━━━━━━

👨‍💻 المطور:
{DEVELOPER}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "📥 قسم التحميل",
                callback_data="download_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "📁 قسم الملفات",
                callback_data="files_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 قسم الدراسة",
                callback_data="study_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "🛠️ قسم الأدوات",
                callback_data="tools_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "🎮 قسم الترفيه",
                callback_data="fun_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "🖨️ صانع المستندات",
                callback_data="documents_menu"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 اشترك بالقناة",
                url=CHANNEL_URL
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )
