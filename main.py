import os
import telebot
import my_types
from pytube import YouTube
from pytube import exceptions as pytube_e

DIR_PATH = os.getcwd()
with open("key.txt", "r") as file:
    BOT_KEY = file.read()

bot = telebot.TeleBot(BOT_KEY)    
    
#=================\FUNCTIONS/===============
def download(download_obj):
    stream = download_obj.stream
    chat_id = download_obj.chat_id
    info_message = download_obj.info_message

    if(stream.includes_video_track):
        fname = f"{chat_id}_video.mp4"
        stream.download(output_path = f"{DIR_PATH}/downloads",filename = fname)
        bot.send_video(chat_id, video = open(f"{DIR_PATH}/downloads/{fname}", "rb"))
    else:
        fname = f"{chat_id}_audio.mp3"
        stream.download(output_path = f"{DIR_PATH}/downloads",filename = fname)
        bot.send_audio(chat_id, audio = open(f"{DIR_PATH}/downloads/{fname}", "rb"),title = stream.title, thumb= open("logo.jpg", "rb"))
    
    if(info_message is not None): 
        bot.delete_message(chat_id, info_message.message_id)
    os.remove(f"{DIR_PATH}/downloads/{fname}")

#=================\BOT HANDLERS/=================
@bot.message_handler(commands=['start', 'help'])   
def start(message):
    bot.send_message(message.chat.id ,"This is a downloader bot. \nPlease send a YouTube link to download.")

@bot.message_handler()
def get_link(message):
    mtext = message.text.strip()
    chat_id = message.chat.id

    try:
        yt = YouTube(mtext)
        img_data = yt.thumbnail_url
    except pytube_e.RegexMatchError:
        bot.send_message(message.chat.id ,"Not a link. Please send a valid link")
        return
    except pytube_e.AgeRestrictedError:
        bot.send_message(message.chat.id ,"Sorry, the video is age restricted")
        return


    mp3_button = telebot.types.InlineKeyboardButton("audio(mp3)", callback_data= f"{mtext}_0_*format")
    mp4_button = telebot.types.InlineKeyboardButton("video(mp4)", callback_data= f"{mtext}_1_*format")
    keyboard = telebot.types.InlineKeyboardMarkup([[mp3_button, mp4_button]])
    bot.send_photo(chat_id, img_data, f"{yt.title} \nWhich format would you like to download in?", reply_to_message_id= message.message_id, reply_markup= keyboard )


@bot.callback_query_handler(lambda call: "_*format" in call.data)
def format_callback(call):
    
    data_list = call.data.split("_") #splits callback string into list of data
    chat_id = call.message.chat.id
    url = data_list[0]
    # 0 - audio , 1 - video
    format = int(data_list[1])

    yt = YouTube(url)
    print(f"Request for {yt.title}") #debug
    info_message = bot.send_message(chat_id, "Downloading...")

    if(format == 0):
        stream = yt.streams.get_audio_only()
    elif(format == 1):
        stream = yt.streams.get_highest_resolution()
    
    download_obj = my_types.Download(chat_id, stream, info_message=info_message)
    download(download_obj)
        
#=============================================
if __name__ == '__main__':
    bot.polling()