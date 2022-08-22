from fileinput import filename
import telebot
from pytube import YouTube

with open("key.txt", "r") as file:
    BOT_KEY = file.read()

bot = telebot.TeleBot(BOT_KEY)

def download(chat_id, yt_obj):
    stream = yt_obj.streams.get_audio_only()
    stream.download(filename = f"{chat_id}_audio.mp3")
    bot.send_audio(chat_id, audio = open(f"{chat_id}_audio.mp3", "rb"),title = yt_obj.title, thumb= open("audio_pic.jpg", "rb"))

@bot.message_handler(commands=['start', 'help'])   
def start(message):
    bot.send_message(message.chat.id ,"This is a downloader bot. \n Please send a YouTube link to download")

@bot.message_handler()
def get_link(message):
    mtext = message.text.strip()
    chat_id = message.chat.id

    try:
        yt = YouTube(mtext)
        img_data = yt.thumbnail_url
    except:
        bot.send_message(message.chat.id ,"Not a link. Please send a valid link")
        return

    bot.send_photo(chat_id, img_data, f"Downloading: {yt.title}", reply_to_message_id= message.message_id)

    download(message.chat.id, yt)

if __name__ == '__main__':
    bot.polling()