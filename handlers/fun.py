import random

from telegram import Update
from telegram.ext import ContextTypes

# =========================
# JOKES
# =========================

jokes = [

    "😂 المدرس: ليه متأخر؟ الطالب: الحلم كان حلو.",

    "😂 مرة طالب جاب صفر، قالوا له ليه؟ قال: أحب الأرقام المستديرة.",

    "😂 المدرس: أين تقع باريس؟ الطالب: في كتاب الجغرافيا."
]

# =========================
# RIDDLES
# =========================

riddles = [

    "🧠 شيء له أسنان ولا يعض؟ الجواب: المشط.",

    "🧠 شيء كلما أخذت منه كبر؟ الجواب: الحفرة.",

    "🧠 ما هو الشيء الذي يمشي بلا أرجل؟ الجواب: الوقت."
]

# =========================
# RANDOM JOKE
# =========================

async def send_joke(update: Update):

    joke = random.choice(jokes)

    await update.message.reply_text(joke)

# =========================
# RANDOM RIDDLE
# =========================

async def send_riddle(update: Update):

    riddle = random.choice(riddles)

    await update.message.reply_text(riddle)

# =========================
# RANDOM GAME
# =========================

async def random_game(update: Update):

    number = random.randint(1, 5)

    await update.message.reply_text(
        f"🎲 رقم الحظ:\n{number}"
    )

# =========================
# HANDLE FUN
# =========================

async def handle_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "😂 نكت":

        await send_joke(update)

    elif text == "🧠 ألغاز":

        await send_riddle(update)

    elif text == "🎲 لعبة الحظ":

        await random_game(update)
