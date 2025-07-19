
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