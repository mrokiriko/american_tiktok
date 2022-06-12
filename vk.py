import os
import vk_api

access_token = os.getenv('VK_ACCESS_TOKEN')
group_id = '-'+str(os.getenv('VK_GROUP_ID'))

vk_session = vk_api.VkApi(token=access_token)

vk = vk_session.get_api()

print(vk.wall.post(owner_id=group_id, message='Hello world!', from_group=1))