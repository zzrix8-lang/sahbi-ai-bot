import os
import yt_dlp
import asyncio

from telegram import Update
from telegram.ext import ContextTypes

# =========================
# DOWNLOAD VIDEO
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

        def run_download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(run_download)

        video_file = None

        for file in os.listdir():

            if file.endswith(".mp4"):
                video_file = file
                break

        if not video_file:

            await msg.edit_text(
                "❌ فشل تحميل الفيديو."
            )

            return

        await msg.delete()

        with open(video_file, "rb") as video:

            await update.message.reply_video(
                video=video,
                caption="✅ تم التحميل بنجاح"
            )

        os.remove(video_file)

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ:\n{str(e)}"
        )

# =========================
# HANDLE URL
# =========================

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text

    if any(site in text for site in [

        "tiktok.com",
        "instagram.com",
        "youtube.com",
        "youtu.be",
        "facebook.com",
        "x.com",
        "twitter.com"

    ]):

        await download_video(update, text)
