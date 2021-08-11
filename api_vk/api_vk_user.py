import requests


class ApiVKuser:
    def __init__(self, vk_id, token):
        self.vk_id = vk_id
        self.token = token

    # метод для проверки корректности токена, который вводит пользователь
    def get_token(self):
        vk_user_token = self.token
        params = {
            'user_id': '1',
            'access_token': vk_user_token,
            'v': '5.130',
        }
        response = requests.get('https://api.vk.com/method/users.get', params=params)
        try:
            if response.json()['response'][0]['first_name'] == "Павел":
                print('Токен прошел проверку и принят для дальнейшего использования!')
                return vk_user_token
        except KeyError:
            print("Ошибка! C токеном что-то не так, попробуйте еще раз")

    def get_user_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': self.vk_id,
            'fields': 'bdate, sex, city, relation',
            'access_token': self.get_token(),
            'v': '5.130',
        }
        response = requests.get(url, params=params).json()
        return response['response'][0]

    def get_user_correct_info(self):
        user_info_dict = {}
        needed_data = self.get_user_info()
        for i in ({'relation', 'sex', 'city', 'bday'} & set(needed_data)):
            user_info_dict[i] = needed_data[i]
        return user_info_dict

    def get_user_absent_info(self):
        user_no_info_dict = {}
        needed_data = self.get_user_info()
        for i in ({'relation', 'sex', 'city', 'bday'} - set(needed_data)):
            user_no_info_dict[i] = ''
        return user_no_info_dict

