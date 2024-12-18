import subprocess
import requests
import os
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

BOT_TOKEN = "YOUR BOT TOKEN"  # Replace with your bot token
ffmpegPID = None


def startStream(camera, key):
    """
    Starts streaming from an M3U8 URL to YouTube using FFmpeg.
    """
    global ffmpegPID
    print(f"Starting stream from {camera} to YouTube...")
    ffmpegPID = subprocess.Popen(
        [
            "ffmpeg", "-re", "-i", camera, "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-c:a", "aac", "-ab", "128k", "-ar", "44100", "-c:v", "libx264", "-preset", "ultrafast", "-threads", "2",
            "-bufsize", "512k", "-f", "flv", "rtmp://vsu.okcdn.ru/input/" + key, 
            "-abort_on", "empty_output", "-xerror"
        ],
        cwd=os.getcwd()
    )
    print(f"Stream started with PID: {ffmpegPID.pid}")


def checkStream(url):
    """
    Checks if the M3U8 URL is accessible.
    """
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def stopStream():
    """
    Stops the current FFmpeg process.
    """
    global ffmpegPID
    if ffmpegPID:
        ffmpegPID.terminate()
        print("Stream stopped.")
        ffmpegPID = None


# Telegram bot commands
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the Streaming Bot! Use /help to see available commands.")


async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/stream <m3u8_url> <stream_key> - Start streaming\n"
        "/stop - Stop the current stream"
    )


async def stream(update: Update, context: CallbackContext) -> None:
    """
    Handles the /stream command to start streaming from M3U8 to YouTube.
    """
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /stream <m3u8_url> <stream_key>")
        return

    m3u8_url = context.args[0]
    stream_key = context.args[1]

    if not checkStream(m3u8_url):
        await update.message.reply_text("Error: The M3U8 URL is offline or invalid. Please check and try again.")
        return

    threading.Thread(target=startStream, args=(m3u8_url, stream_key), daemon=True).start()
    await update.message.reply_text("Stream started successfully!")


async def stop(update: Update, context: CallbackContext) -> None:
    """
    Handles the /stop command to stop the stream.
    """
    stopStream()
    await update.message.reply_text("Stream stopped successfully.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stream", stream))
    application.add_handler(CommandHandler("stop", stop))

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
