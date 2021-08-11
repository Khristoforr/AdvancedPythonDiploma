from api_vk import api_vk_server
from api_vk import api_vk_user
from api_vk.api_vk_find_city_id import find_a_city
from api_vk.api_vk_find_match import ApiVKmatch

user_name = api_vk_server.API_VK_SERVER().get_message_from_user()[1]

def answer(ans):
    api_vk_server.API_VK_SERVER().make_an_answer(ans, user_name)

def send_photo(photo_id,  photo_owner, user_name):
    api_vk_server.API_VK_SERVER().send_photo_to_user(photo_id, user_name, photo_owner)

def get_a_message_from_user():
    return api_vk_server.API_VK_SERVER().get_message_from_user()[0].lower()

flag = True

def func():
    global flag
    answer("Здравствуйте! Список доступных команд: \n"
           "1 - начать поиск пары\n"
           "2 - закончить работу")
    message = get_a_message_from_user()
    if message == "1":
        answer('Введите токен пользователя с нужными правами для поиска')
        user_token = get_a_message_from_user()
        while user_token != api_vk_user.ApiVKuser(1, user_token).get_token():
            answer('Некорректный токен, пробуйте еще раз')
            user_token = get_a_message_from_user()
        answer('Ура, токен совпал\n'
               'Введите id пользователя для которого будем искать пару')
        user_id = get_a_message_from_user()
        user_data_info = api_vk_user.ApiVKuser(user_id, user_token).get_user_correct_info()
        user_absent_info = api_vk_user.ApiVKuser(user_id, user_token).get_user_absent_info()
        for i in user_absent_info:
            if i == 'relation':
                answer('Введите семейное положение пользователя\n'
                      '1 — не женат/не замужем\n'
                      '2 — есть друг/есть подруга\n'
                      '3 — помолвлен/помолвлена\n'
                      '4 — женат/замужем\n'
                      '5 — всё сложно\n'
                      '6 — в активном поиске\n'
                      '7 — влюблён/влюблена\n'
                      '8 — в гражданском браке')
                x = get_a_message_from_user()
                while x not in '12345678':
                    answer('Ошибка, некорректные данные')
                    x = get_a_message_from_user()
                user_absent_info[i] = x
            elif i == 'city':
                answer("Введите город пользователя")
                city = get_a_message_from_user()
                city_id = find_a_city(user_token,city)
                while city_id == 'Ошибка':
                    answer("Ошибка! Введите город пользователя")
                    city = get_a_message_from_user()
                    city_id = find_a_city(user_token, city)
                user_absent_info[i] = {'id': city_id}
            elif i == 'bday':
                answer("Введите возраст пользователя")
                user_absent_info[i] = get_a_message_from_user()
        user_data_info.update(user_absent_info)
        match_person = ApiVKmatch(user_data_info,user_token)
        match_person_id = match_person.get_profile_links()[0]
        match_person_link = f'https://vk.com/id{match_person_id}'
        answer(match_person_link)
        for most_popular_photo in match_person.get_most_popular_photos(match_person_id):
            print(match_person.get_most_popular_photos(match_person_id))
            send_photo(photo_id=most_popular_photo, user_name=user_name,photo_owner=match_person_id)


    elif message == '2':
        answer("Пока")
        flag = False
        return flag

while flag == True:
    print(func())