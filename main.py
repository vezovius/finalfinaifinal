
 HEAD
from keep_alive import keep_alive
import telebot
from telebot import types
import os

keep_alive()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}

    audio = open("welcome_turkish.ogg", "rb")
    bot.send_voice(chat_id, audio)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Köpek", "Kedi", "Kuş")
    bot.send_message(chat_id, "Hayvanın türünü seçiniz:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Köpek", "Kedi", "Kuş"])
def handle_animal_type(message):
    chat_id = message.chat.id
    user_data[chat_id]["Tür"] = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Erkek", "Dişi")
    bot.send_message(chat_id, "Cinsiyeti seçiniz:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Erkek", "Dişi"])
def handle_gender(message):
    chat_id = message.chat.id
    user_data[chat_id]["Cinsiyet"] = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Yavru", "Genç", "Yetişkin", "Yaşlı")
    bot.send_message(chat_id, "Lütfen yaşı seçin:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Yavru", "Genç", "Yetişkin", "Yaşlı"])
def handle_age(message):
    chat_id = message.chat.id
    user_data[chat_id]["Yaş"] = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Evet, kısır", "Hayır, değil")
    bot.send_message(chat_id, "Hayvan kısır mı?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Evet, kısır", "Hayır, değil"])
def handle_neuter(message):
    chat_id = message.chat.id
    user_data[chat_id]["Kısır mı"] = message.text
    bot.send_message(chat_id, "Lütfen ana şikayeti yazınız:")

@bot.message_handler(func=lambda message: "şikayet" not in user_data.get(message.chat.id, {}))
def handle_complaint(message):
    chat_id = message.chat.id
    user_data[chat_id]["şikayet"] = message.text
    bot.send_message(chat_id, "Şu ana kadar kullanılan ilaçları yazınız:")

@bot.message_handler(func=lambda message: "ilaçlar" not in user_data.get(message.chat.id, {}))
def handle_drugs(message):
    chat_id = message.chat.id
    user_data[chat_id]["ilaçlar"] = message.text

    summary = "\n".join([f"{k}: {v}" for k, v in user_data[chat_id].items()])
    bot.send_message(chat_id, f"Teşekkürler. Alınan bilgiler:\n{summary}")

bot.polling()
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
=======
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
>>>>>>> 5d776aea62a13e35e0aa578dec1455e0e69966b6
