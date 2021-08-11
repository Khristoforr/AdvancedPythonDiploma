import requests

VK_GROUP_TOKEN = '3977a45b624825964b800e805a06ad8f95678fb33de8052648358112f975dc3e717ec0f7dcf7c4458b736'


class API_VK_SERVER():

    def get_data_session(self):
        url = 'https://api.vk.com/method/groups.getLongPollServer'
        params = {
            'group_id': 47378589,
            'access_token': VK_GROUP_TOKEN,
            'v': '5.131',
            }
        response = requests.get(url, params=params).json()
        return response['response']

    def get_message_from_user(self):
        data = self.get_data_session()
        response = requests.get(
                '{server}?act=a_check&key={key}&ts={ts}&wait=25'
                    .format(server=data['server'], key=data['key'], ts=data['ts'])).json()
        text = response['updates'][0]['object']['message']['text']
        user_id = response['updates'][0]['object']['message']['from_id']
        return [text, user_id]

    def make_an_answer(self, message, user_id):
        url = 'https://api.vk.com/method/messages.send'
        params = {'groud_id': 47378589,
                  'peer_id': user_id,
                  'access_token': VK_GROUP_TOKEN,
                  'message': message,
                  'v': '5.131',
                  'random_id': 0}
        response = requests.post(url=url, params=params).json()
        return response

    def send_photo_to_user(self, photo_id, user_id, photo_owner):
        url = 'https://api.vk.com/method/messages.send'
        params = {'groud_id': 47378589,
                  'peer_id': user_id,
                  'access_token': VK_GROUP_TOKEN,
                  'attachment': f'photo{photo_owner}_{photo_id}',
                  'v': '5.131',
                  'random_id': 0}
        response = requests.post(url=url, params=params).json()
        return response
