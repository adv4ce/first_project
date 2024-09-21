import requests
import os
from tqdm import tqdm

class YaUpload:
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

def response(token):
    url = "https://cloud-api.yandex.net/v1/disk"
    headers = {"Authorization": f"OAuth {token}"}

    return requests.get(url, headers=headers)

def check_ya_token():
    token = input("Введите токен Яндекс диска: ")
    
    if response(token).status_code == 401:
        while response(token).status_code == 401:
            print("Проверьте правильность введенного токена")
            token = input("Введите правильный токен Яндекс диска: ")
    return token
