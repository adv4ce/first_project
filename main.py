import os
from test import *
from get_photo_information import *
from create_json_file import *
from upload_to_ya_disk import *
from upload_to_ya_disk import *
from upload_to_go_disk import *
import configparser

def type_p():
    type_photos = input(
            "Выберите цифру в зависимости от типа фотографий, которые вы хотите загрузить:\n"
            "1 - profile (Фотографии из профиля пользователя)\n"
            "2 - wall (Фотографии со стены пользователя)\n"
            "3 - saved (Сохранённые фотографии пользователя)\n"
        )
    if type_photos not in ['1', '2', '3']:
        while type_photos not in ['1', '2', '3']:
            type_photos = input(
                    "Используйте только цифры из списка:\n"
                    "1 - profile (Фотографии из профиля пользователя)\n"
                    "2 - wall (Фотографии со стены пользователя)\n"
                    "3 - saved (Сохранённые фотографии пользователя)\n"
                )
    if type_photos == '1':
        return "profile"
    elif type_photos == '2':
        return "wall"
    elif type_photos == '3':
        return "saved"
    else:
        type_p('error')

def if_not_user_id(token):
    user_id = input("Введите id пользователя: ")
    if not check_user(token, user_id):
            while not check_user(token, user_id):
                print("Пользователь с таким ID не найден.")
                user_id = input("Введите правильный id пользователя: ")
            return user_id
    return user_id

def select_count_photos():
    count_photos = int(
        input(
            f'Введите количество фото для загрузки (Максимум {len(os.listdir("user_photos"))}): '
        )
    )
    if count_photos > len(os.listdir("user_photos")) or count_photos < 0:
        while count_photos > len(os.listdir("user_photos")) or count_photos < 0:
            count_photos = int(input("Введите правильное кол-во фото: "))
    return count_photos

def get_info():
    config = configparser.ConfigParser()
    config.read('access_token.ini')
    token = config['VK']['token']
    user_id = if_not_user_id(token)
    select_type = type_p()
    return [token, user_id, select_type]

def get_photos_inf(token, user_id, select_type):
    vk = VK(token, user_id, select_type)
    photo_data = vk.user_photos()
    save_photos = vk.save_photos(photo_data)
    print(f'Сохранено {len(os.listdir("user_photos"))} фотографии(-й)')
    return save_photos

def create_json(photos_data):
    json = JSON(photos_data)
    json.create_json()
    print("Отчет о фото сохранен в файл info.json")

def upload_to_ya_disk(ya_token, count_photos):
    try:
        upload = YaUpload(ya_token, count_photos)
        upload.create_folder()
        upload.upload_photos()
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        upload.create_folder()
        upload.upload_photos()
    else:
        print(
            f"Фотографии в количестве {count_photos} шт успешно загружены на ваш Яндекс Диск"
        )

def upload_to_go_disk(count_photos):
    upload = GoUpload(count_photos)
    upload.upload_photos()
    print(
            f"Фотографии в количестве {count_photos} шт успешно загружены на ваш Google Диск"
        )

def disk_selection():
    select = input('Выберите желаемый диск:\n'
                    '1 - Яндекс диск\n'
                    '2 - Google диск\n')
    if select not in ['1', '2']:
        while select not in ['1', '2']:
            select = input('Выберите правильное число из списка:\n'
                    '1 - Яндекс диск\n'
                    '2 - Google диск\n')
            
    return select

def selection_realization(disk, count_photos):
    if disk == '1':
        ya_token = check_ya_token()
        upload_to_ya_disk(ya_token, count_photos)
    else:
        upload_to_go_disk(count_photos)

if __name__ == "__main__":
    if "user_photos" not in os.listdir():
        os.mkdir("user_photos")
    
    info = get_info()
    token, user_id, select_type = info[0], info[1], info[2]
    size = get_photos_inf(token, user_id, select_type)

    create_json(size)
    disk = disk_selection()
    count_photos = select_count_photos()
    selection_realization(disk, count_photos)
