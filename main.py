import telebot

with open("key.txt", "r") as file:
    BOT_KEY = file.read()

if __name__ == "__main__":
    bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id ,"Please send Youtube/Spotify link")