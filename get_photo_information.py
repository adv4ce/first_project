import requests
from tqdm import tqdm
import os

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
        
    def save_photos(self, photo_data):
        photos_sizes = []
        for photos in tqdm(photo_data, desc="Saving photos", unit=" photo"):
            response = requests.get(photos["sizes"][-1]["url"])
            file_name = f"{photos['likes']['count']}.jpg"
            file_path = os.path.join("user_photos", file_name)
            photos_sizes.append(photos["sizes"][-1]['type'])
            if not os.path.isfile(file_path):
                with open(file_path, "wb") as file:
                    file.write(response.content)
            else:
                file_name = f"{photos['date']}.jpg"
                file_path = os.path.join("user_photos", file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
        return photos_sizes
    
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
