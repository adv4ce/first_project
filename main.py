import requests
import os
import json
from tqdm import tqdm


class VK:
    def __init__(self, token, user_id, type_photos, version="5.131"):
        self.token = token
        self.user_id = user_id
        self.version = version
        self.type_photos = type_photos
        self.params = {
            "access_token": self.token,
            "album_id": self.type_photos,
            "extended": True,
            "v": self.version,
        }

    def user_photos(self):
        url = "https://api.vk.com/method/photos.get"
        params = {"owner_id": self.user_id}
        response = requests.get(url, params={**self.params, **params})
        response_json = response.json()
        if "error" in response_json:
            error_code = response_json["error"]["error_code"]
            error_msg = response_json["error"]["error_msg"]
            print(f"Ошибка {error_code}: {error_msg}")
            return None
        else:
            photos = response_json.get("response", {}).get("items", [])
            return photos


class Likes:
    def __init__(self, photo_data, token):
        self.photo_data = photo_data
        self.token = token
        self.inf_photos = []

    def save_photos(self):
        for photos in tqdm(self.photo_data, desc="Saving photos", unit=" photo"):
            response = requests.get(photos["sizes"][-1]["url"])
            file_name = f"{photos['likes']['count']}.jpg"
            file_path = os.path.join("user_photos", file_name)

            if not os.path.isfile(file_path):
                with open(file_path, "wb") as file:
                    file.write(response.content)
            else:
                file_name = f"{photos['date']}.jpg"
                file_path = os.path.join("user_photos", file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)

            self.inf_photos.append(
                {"file_name": file_name, "size": f"{photos['sizes'][-1]['type']}"}
            )

        with open("info.json", "w", encoding="utf-8") as file:
            json.dump(self.inf_photos, file, indent=4, ensure_ascii=False)


class Upload:
    def __init__(
        self,
        token,
        count_photos=5,
        folder_name="Homework photos",
        upload_url="https://cloud-api.yandex.net/v1/disk/resources",
    ):
        self.token = token
        self.upload_url = upload_url
        self.folder_name = folder_name
        self.count_photos = count_photos
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}",
        }

    def create_folder(self):
        try:
            requests.put(
                f"{self.upload_url}?path=disk%3A%2F{self.folder_name}",
                headers=self.headers,
            )
        except requests.RequestException as e:
            print(f"Ошибка создания папки: {e}")
            return requests.put(
                f"{self.upload_url}?path=disk%3A%2F{self.folder_name}",
                headers=self.headers,
            )

    def upload_photos(self, replace=False):
        for upload_photo in tqdm(
            os.listdir("user_photos")[: self.count_photos],
            desc="Uploading photos",
            unit=" photo",
        ):
            res = requests.get(
                f"{self.upload_url}/upload?path={self.folder_name}/{upload_photo}&overwrite={replace}",
                headers=self.headers,
            ).json()

            with open(f"user_photos/{upload_photo}", "rb") as file:
                try:
                    requests.put(res["href"], files={"file": file})
                except KeyError:
                    print(f"Upload error: {res}")


def type_p(number_of_type):
    if number_of_type == 1:
        return "profile"
    elif number_of_type == 2:
        return "wall"
    elif number_of_type == 3:
        return "saved"
    else:
        return ValueError


def check_user(token, user_id):
    url = "https://api.vk.com/method/users.get"
    params = {"user_ids": user_id, "access_token": token, "v": "5.131"}

    response = requests.get(url, params=params).json()

    if "error" in response:
        error_code = response["error"]["error_code"]
        error_msg = response["error"]["error_msg"]
        print(f"Ошибка {error_code}: {error_msg}")
        return False
    else:
        users = response.get("response", [])
        if len(users) == 0:
            return False
    return True


def check_ya_token(token):
    url = "https://cloud-api.yandex.net/v1/disk"
    headers = {"Authorization": f"OAuth {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        return 1


if __name__ == "__main__":
    if "user_photos" not in os.listdir():
        os.mkdir("user_photos")
    token = open("access_token.txt", "r").read()
    user_id = input("Введите id пользователя: ")

    if not check_user(token, user_id):
        while not check_user(token, user_id):
            print("Пользователь с таким ID не найден.")
            user_id = input("Введите правильный id пользователя: ")

    ya_token = input("Введите токен Яндекс диска: ")
    if check_ya_token(ya_token) == 1:
        while check_ya_token(ya_token) == 1:
            print("Проверьте правильность введенного токена")
            ya_token = input("Введите правильный токен Яндекс диска: ")

    type_photos = int(
        input(
            "Выберите цифру в зависимости от типа фотографий, которые вы хотите загрузить:\n"
            "1 - profile (Фотографии из профиля пользователя)\n"
            "2 - wall (Фотографии со стены пользователя)\n"
            "3 - saved (Сохранённые фотографии пользователя)\n"
        )
    )
    select_type = type_p(type_photos)
    if select_type == ValueError:
        while select_type == ValueError:
            select_type = int(
                input(
                    "Ошибка. Выберите правильное число из списка:\n"
                    "1 - profile\n"
                    "2 - wall\n"
                    "3 - saved\n"
                )
            )

    vk = VK(token, user_id, select_type)
    photo_data = vk.user_photos()

    likes = Likes(photo_data, token)
    likes.save_photos()
    print(f'Сохранено {len(os.listdir("user_photos"))} фотографии(-й)')
    print("Отчет о фото сохранен в файл info.json")

    count_photos = int(
        input(
            f'Введите количество фото для загрузки (Максимум {len(os.listdir("user_photos"))}): '
        )
    )
    if count_photos > len(os.listdir("user_photos")) or count_photos < 0:
        while count_photos > len(os.listdir("user_photos")) or count_photos < 0:
            count_photos = int(input("Введите правильное кол-во фото: "))

    try:
        upload = Upload(ya_token, count_photos)
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
