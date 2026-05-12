from telegram import Update
from telegram.ext import ContextTypes

# =========================
# STUDY PLAN
# =========================

async def study_plan(update: Update):

    text = """
📚 خطة دراسة يومية:

08:00 - 10:00 ➜ دراسة المادة الأولى
10:00 - 10:30 ➜ استراحة
10:30 - 12:00 ➜ حل واجبات
12:00 - 01:00 ➜ مراجعة
01:00 - 02:00 ➜ راحة
02:00 - 04:00 ➜ دراسة المادة الثانية
"""

    await update.message.reply_text(text)

# =========================
# POMODORO
# =========================

async def pomodoro(update: Update):

    text = """
⏰ نظام Pomodoro:

25 دقيقة دراسة 📚
5 دقائق راحة ☕

كررها 4 مرات ثم خذ راحة طويلة 😎
"""

    await update.message.reply_text(text)

# =========================
# QUICK TEST
# =========================

async def quick_test(update: Update):

    text = """
🧠 اختبار سريع:

1️⃣ كم ناتج 5 × 5 ؟

A) 20
B) 25
C) 30
"""

    await update.message.reply_text(text)

# =========================
# HANDLE STUDY
# =========================

async def handle_study(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📅 خطة دراسة":

        await study_plan(update)

    elif text == "⏰ Pomodoro":

        await pomodoro(update)

    elif text == "🧠 اختبار سريع":

        await quick_test(update)
