from telegram import Update
from telegram.ext import ContextTypes

# =========================
# CLASS SCHEDULE
# =========================

async def class_schedule(update: Update):

    text = """
📅 جدول حصص:

الأحد:
📚 رياضيات
📖 عربي
🧪 علوم

الاثنين:
📚 إنجليزي
💻 حاسوب
📖 تاريخ
"""

    await update.message.reply_text(text)

# =========================
# EXAM PAPER
# =========================

async def exam_paper(update: Update):

    text = """
📝 نموذج ورقة امتحان

━━━━━━━━━━━━━━━

اسم الطالب: ___________

الصف: ___________

السؤال الأول:
ما هو ناتج 10 × 5 ؟

━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(text)

# =========================
# ATTENDANCE LIST
# =========================

async def attendance_list(update: Update):

    text = """
📋 كشف حضور

1️⃣ أحمد
2️⃣ محمد
3️⃣ خالد
4️⃣ يوسف
"""

    await update.message.reply_text(text)

# =========================
# HANDLE DOCUMENTS
# =========================

async def handle_documents(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📅 جدول حصص":

        await class_schedule(update)

    elif text == "📝 ورقة امتحان":

        await exam_paper(update)

    elif text == "📋 كشف حضور":

        await attendance_list(update)
