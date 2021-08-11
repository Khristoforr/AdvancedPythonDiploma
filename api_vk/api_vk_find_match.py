import requests
import random

class ApiVKmatch():
    # экземпляр класса на вход будет принимать словарь с данными пользователя, для которого ищем пару
    def __init__(self, user_features, token):
        self.user_features = user_features
        self.token = token

    def find_a_people(self):
        url = 'https://api.vk.com/method/users.search'
        opposite_sex = lambda x: 1 if x == 2 else 2
        params = {
            'count': 1000,
            'city': self.user_features['city']['id'],
            'sex': opposite_sex(self.user_features['sex']),
            'status': 1 or 5 or 6,
            'age_from': (int(self.user_features['bday']) - 3),
            'age_to': (int(self.user_features['bday']) + 5),
            'access_token':self.token,
            'fields': 'photo_400',
            'v': '5.130',
            'has_photo': 1
        }
        response = requests.get(url, params=params).json()
        return response['response']['items']

    def get_profile_links(self):
        people_list = self.find_a_people()
        id_list = [people_list[i]['id'] for i in range(len(people_list))]
        return random.sample(id_list, 1)

    def get_photos(self, link):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': link,
            'access_token': self.token,
            'v': '5.130',
            'album_id': 'profile',
            'photo_sizes': '1',
            'extended': '1'
        }
        response = requests.get(url, params=params).json()
        try:
            return response['response']['items']
        except KeyError:
            return "Приватный профиль"

    def get_most_popular_photos(self, photo_owner_id):
        user_photos = self.get_photos(photo_owner_id)
        if user_photos == "Приватный профиль":
            return "Пользователь без фото или профиль закрыт"
        else:
            likes_and_comments_list = []
            for photo in user_photos:
                likes_and_comments_list.append(photo['likes']['count'] * photo['comments']['count'])
            most_popular_photos_indexes = []
            for i in range(3):
                max_index = likes_and_comments_list.index(max(likes_and_comments_list))
                most_popular_photos_indexes.append(max_index)
                likes_and_comments_list[max_index] = 0
            return list(set([user_photos[i]['id'] for i in most_popular_photos_indexes]))





