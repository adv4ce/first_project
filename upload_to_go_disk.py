from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from tqdm import tqdm

class GoUpload:
    def __init__(self, count_photos):
        self.count_photos = count_photos

    def upload_photos(self):
        auth = GoogleAuth()
        auth.LocalWebserverAuth()
        try:
            drive = GoogleDrive(auth)
            
            folder_metadata = {
                'title': 'Homework photos',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive.CreateFile(folder_metadata)
            folder.Upload()
            
            folder_id = folder['id']
            
            for file_name in tqdm(
                os.listdir("user_photos")[: self.count_photos],
                desc="Uploading photos",
                unit=" photo",
            ):
                file_metadata = {
                    'title': file_name,
                    'parents': [{'id': folder_id}]
                }
                my_file = drive.CreateFile(file_metadata)
                my_file.SetContentFile(os.path.join('user_photos', file_name))
                my_file.Upload()

        except Exception as ex:
            return f'Что-то пошло не так: {ex}'
