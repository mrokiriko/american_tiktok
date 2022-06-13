from dotenv import load_dotenv
import os
import telebot
import vk_api
import time
import re
import requests

load_dotenv()

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_API_KEY'))

access_token = os.getenv('VK_ACCESS_TOKEN')
group_id = str(os.getenv('VK_GROUP_ID'))

vk_session = vk_api.VkApi(token=access_token)

upload = vk_api.VkUpload(vk_session)



def download_tiktok(link, message):

    ml = int(time.time() * 1000)
    video_file = './vids/'+str(ml)+'.mp4'

    params = {
      "link": link
    }
    headers = {
      'x-rapidapi-host': os.getenv('RAPIDAPI_HOST'),
      'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
      'User-Agent': 'Mozilla/5.0'
    }
    
    ### Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
    #Using the default one can stop working any moment 
    
    api = f"https://tiktok-info.p.rapidapi.com/dl/"
    r = requests.get(api, params=params, headers=headers).json()['videoLinks']['download']
    directory = str(round(time.time()))
    filename = str(int(time.time()))+'.mp4'

    print(r)
    print(requests.head(r))
    print(requests.head(r).headers)

    size = int(requests.head(r).headers['Content-length'])
    total_size = "{:.2f}".format(int(size) / 1048576)
    try:
        os.mkdir(directory)
    except:
        pass
    with requests.get(r, timeout=(50, 10000), stream=True) as r:
        r.raise_for_status()
        with open(video_file, 'wb') as f:
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
                        # bot.edit(f'__**URL :**__ __{message.text}__\n'
                        #        f'__**Total Size :**__ __{total_size} MB__\n'
                        #        f'__**Downloaded :**__ __{percent}%__\n',
                        #        disable_web_preview=False)

                        bot.edit_message_text(f'__**URL :**__ __{message.text}__\n'
                               f'__**Total Size :**__ __{total_size} MB__\n'
                               f'__**Downloaded :**__ __{percent}%__\n',
                               message.chat.id, message.message_id)
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

    return video_file

def publish_video(video_file):
    f = open('inc.txt', 'r')
    inc = int(f.read()) + 1
    f.close()

    f = open("inc.txt", "w")
    f.write(str(inc))
    f.close()


    video_name = 'американ тикток #' + str(inc)


    video = upload.video(
        video_file=video_file,
        name=video_name,
        group_id=group_id
    )


    video_desc = 'video' + str(video['owner_id']) + '_' + str(video['video_id'])

    vk = vk_session.get_api()

    print('vk.wall.post response')
    print(vk.wall.post(owner_id='-'+group_id, from_group=1, attachments=video_desc))
    return video_name


def is_tiktok_url(url):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def download(message):
    print('message')
    print(message)
    print(message.text)

    video_file = ''
    if is_tiktok_url(message.text):
        bot.send_message(message.chat.id, "Starts downloading")

        video_file = download_tiktok(message.text, message)

        bot.send_message(message.chat.id, "Video uploaded as " + video_file)

        r = publish_video(video_file)

        bot.send_message(message.chat.id, "Video published to https://vk.com/us_tiktok")
    else:
        bot.send_message(message.chat.id, "Incorrect url")


# bot.remove_webhook()

print('start polling ...')
bot.infinity_polling()