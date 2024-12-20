from config import token, username
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import time
import os
from PIL import Image


bot_token: Final = token
bot_username: Final = username


TEMP_DIR = "temp"
PROCESSED_DIR = "processed"


os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def compress_image(input_path: str, output_path: str, quality: int = 70):
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", quality=quality)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        
        photo = update.message.photo[-1]

        photo_file = await photo.get_file()
        filename = time.strftime("%Y-%m-%d_%H-%M-%S")
        temp_path = os.path.join(TEMP_DIR, f"{filename}.jpg")
        processed_path = os.path.join(PROCESSED_DIR, f"{filename}_compressed.jpg")
        
        await photo_file.download_to_drive(temp_path)
        await update.message.reply_text("Image received. Processing...")


        compress_image(temp_path, processed_path)


        os.remove(temp_path)

        await update.message.reply_text("Image processed and saved successfully!")
    else:
        await update.message.reply_text("Please send an image.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me an image, and I'll process and save it.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")


def main():
    print("Starting ...")

    application = Application.builder().token(bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_error_handler(error)

    print("Polling ...")
    application.run_polling()

if __name__ == '__main__':
    main()
