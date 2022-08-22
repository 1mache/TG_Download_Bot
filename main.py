import telebot
import requests

with open("key.txt", "r") as file:
    BOT_KEY = file.read()

bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id ,"Please send Youtube/Spotify link")

@bot.message_handler()
def get_link(message):
    mtext = message.text
    if(mtext.startswith("https://www.youtube.com/watch?") or mtext.startswith("https://youtu.be/")):
        print(requests.get(mtext).text)
    else:
        bot.send_message(message.chat.id ,"Please send a valid Youtube/Spotify link")
        
bot.infinity_polling()