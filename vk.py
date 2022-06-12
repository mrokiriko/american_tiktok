from dotenv import load_dotenv
import os
import vk_api
from os import walk
import time

load_dotenv()

access_token = os.getenv('VK_ACCESS_TOKEN')
group_id = str(os.getenv('VK_GROUP_ID'))

vk_session = vk_api.VkApi(token=access_token)

upload = vk_api.VkUpload(vk_session)


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, '1655039463/1.txt')



ml = int(time.time() * 1000)
video_file = './vids/'+str(ml)+'.mp4'


video_file = './vids/vid.mp4'

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

print(vk.wall.post(owner_id='-'+group_id, from_group=1, attachments=video_desc))