from dotenv import load_dotenv
import os
import vk_api
from os import walk
import time
import re

# load_dotenv()

# access_token = os.getenv('VK_ACCESS_TOKEN')
# group_id = str(os.getenv('VK_GROUP_ID'))

# vk_session = vk_api.VkApi(token=access_token)

# upload = vk_api.VkUpload(vk_session)







# video_file = './vids/vid.mp4'

# f = open('inc.txt', 'r')
# inc = int(f.read()) + 1
# f.close()

# f = open("inc.txt", "w")
# f.write(str(inc))
# f.close()


# video_name = 'американ тикток #' + str(inc)


# video = upload.video(
#     video_file=video_file,
#     name=video_name,
#     group_id=group_id
# )


# video_desc = 'video' + str(video['owner_id']) + '_' + str(video['video_id'])


# vk = vk_session.get_api()

# print(vk.wall.post(owner_id='-'+group_id, from_group=1, attachments=video_desc))



# regex = re.compile(
#         r'^(?:http|ftp)s?://' # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
#         r'localhost|' #localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
#         r'(?::\d+)?' # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)


regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)



string = "https://www.tiktok.com/@thep00lguy/video/7098382184716717317"
# string = "asdasd"

print(re.match(regex, string) is not None ) 