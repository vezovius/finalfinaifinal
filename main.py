
from telegram import ReplyKeyboardMarkup, Update, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import json
from keep_alive import keep_alive

keep_alive()

TOKEN = "SECRETTOKEN"

TYPE, GENDER, AGE, NEUTERED, COMPLAINT, MEDICATION = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("🐶 Köpek")], [KeyboardButton("🐱 Kedi")], [KeyboardButton("🐦 Kuş")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Veteriner botuna hoş geldiniz! Lütfen hayvan türünü seçiniz:", reply_markup=reply_markup)
    return TYPE

async def type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["type"] = update.message.text
    keyboard = [[KeyboardButton("Erkek")], [KeyboardButton("Dişi")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Hayvanın cinsiyetini seçiniz:", reply_markup=reply_markup)
    return GENDER

async def gender_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("Hayvanın yaşını giriniz:")
    return AGE

async def age_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["age"] = update.message.text
    keyboard = [[KeyboardButton("Evet")], [KeyboardButton("Hayır")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Hayvan kısırlaştırılmış mı?", reply_markup=reply_markup)
    return NEUTERED

async def neutered_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["neutered"] = update.message.text
    await update.message.reply_text("Ana şikayeti yazınız:")
    return COMPLAINT

async def complaint_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["complaint"] = update.message.text
    await update.message.reply_text("Şu ana kadar kullanılan ilaçları yazınız:")
    return MEDICATION

async def medication_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["medication"] = update.message.text

    user_id = str(update.message.from_user.id)
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[user_id] = context.user_data

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    await update.message.reply_text("Teşekkürler! Bilgiler kaydedildi.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("İşlem iptal edildi.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, type_handler)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender_handler)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_handler)],
            NEUTERED: [MessageHandler(filters.TEXT & ~filters.COMMAND, neutered_handler)],
            COMPLAINT: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_handler)],
            MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, medication_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
