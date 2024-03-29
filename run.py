from dotenv import load_dotenv
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
import shutil
import requests
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from progress_bar import progress, TimeFormatter, humanbytes


load_dotenv()

username = os.environ.get('TELEGRAM_BOT_USERNAME')
bot_token = os.environ.get('TELEGRAM_BOT_API_KEY')
workers = 4 # int(os.environ.get('WORKERS'))

api_id = int(os.environ.get('API_KEY'))
api_hash = os.environ.get('API_HASH')

chnnl = os.environ.get('CHANNEL_URL')
# BOT_URL = os.environ.get('BOT_URL')


# app = Client("JayBee", bot_token=bot_token, api_id=api, api_hash=hash, workers=workers)
app = Client(username, bot_token=bot_token, api_id=api_id, api_hash=api_hash, workers=workers)


@app.on_message(filters.command('help'))
def help(client, message):
    kb = [[InlineKeyboardButton('Channel 🛡', url=chnnl),InlineKeyboardButton('Repo 🔰', url="https://github.com/TerminalWarlord/TikTok-Downloader-Bot/")]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"Hello there, I am **TikTok Downloader Bot**.\nI can download any TikTok video from a given link.\n\n"
                                            "__Send me a TikTok video link__",
                     parse_mode='md',
                     reply_markup=reply_markup)


@app.on_message((filters.regex("http://")|filters.regex("https://")) & (filters.regex('tiktok')|filters.regex('douyin')))
def tiktok_download(link):
    
    params = {
      "link": link
    }
    headers = {
      'x-rapidapi-host': os.getenv('RAPIDAPI_HOST'),
      'x-rapidapi-key': os.getenv('RAPIDAPI_KEY')
    }
    
    ### Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
    #Using the default one can stop working any moment 
    
    api = f"https://tiktok-info.p.rapidapi.com/dl/"
    r = requests.get(api, params=params, headers=headers).json()['videoLinks']['download']
    directory = str(round(time.time()))
    filename = str(int(time.time()))+'.mp4'
    print(requests.head(r))
    size = int(requests.head(r).headers['Content-length'])
    total_size = "{:.2f}".format(int(size) / 1048576)
    try:
        os.mkdir(directory)
    except:
        pass
    with requests.get(r, timeout=(50, 10000), stream=True) as r:
        r.raise_for_status()
        with open(f'./{directory}/{filename}', 'wb') as f:
            chunk_size = 1048576
            dl = 0
            show = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                dl = dl + chunk_size
                percent = round(dl * 100 / size)
                if percent > 100:
                    percent = 100
                if show == 1:
                    try:
                        # a.edit(f'__**URL :**__ __{message.text}__\n'
                        #        f'__**Total Size :**__ __{total_size} MB__\n'
                        #        f'__**Downloaded :**__ __{percent}%__\n',
                        #        disable_web_preview=False)
                        print(total_size)
                        print(percent, '%')
                    except:
                        pass
                    if percent == 100:
                        show = 0

        print(f'__Downloaded to the server!\n'
               f'Uploading to Telegram Now ⏳__')
        start = time.time()
        title = filename

        # app.send_document(chat_id=message.chat.id,
        #                   document=f"./{directory}/{filename}",
        #                   caption=f"**File :** __{filename}__\n"
        #                   f"**Size :** __{total_size} MB__\n\n"
        #                   f"__Uploaded by @{username}__",
        #                   file_name=f"{directory}",
        #                   parse_mode='md',
        #                   progress=progress,
        #                   progress_args=(a, start, title))

        print(start)
        print(title)

        print('finish downloading')

        # ToDo remove directory after finishing
        # try:
        #     shutil.rmtree(directory)
        # except:
        #     pass


app.run()

# print('start')
# print(tiktok_download('https://www.tiktok.com/@thep00lguy/video/7098382184716717317'))
# print('end')