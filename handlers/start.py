from telegram import ReplyKeyboardMarkup

DEVELOPER = "@n5w_n"

async def start(update, context):

    keyboard = [
        ["📥 قسم التحميل"],
        ["📁 قسم الملفات"],
        ["📚 قسم الدراسة"],
        ["🛠️ قسم الأدوات"],
        ["🎮 قسم الترفيه"],
        ["🖨️ صانع المستندات"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = f"""
🔥 أهلاً بك في SAHBI AI

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
        text,
        reply_markup=reply_markup
    )
