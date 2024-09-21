import json
import os

class JSON:
    def __init__(self, size):
        self.size = size
        self.inf_photos = []
        
    def create_json(self):
        files = os.listdir('user_photos')
        for file in range(len(files)):
          self.inf_photos.append(
              {"file_name": files[file], "size": f"{self.size[file]}"}
          )
        with open("info.json", "w", encoding="utf-8") as file:
            json.dump(self.inf_photos, file, indent=4, ensure_ascii=False)

