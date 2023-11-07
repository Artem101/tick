import requests
import os
import time
from vivod import foto
ACCESS_TOKEN = 'sl.BpaTQ1gQOOdEh6UUNqUkzKWBbAj9mw0cKqacOeUj1_SKxmHS-9R2GveCT1JxMAgEWJH0COekL1hrnw0Jvvmiz5gySAp0TKXrZJ3pE2tV6nDlknwxYtfHoRBI-hTzfhKemjm6XLpF9daW'
FOLDER_PATH = '/video'


while True:
    list_files_url = 'https://api.dropboxapi.com/2/files/list_folder'
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    params = {
        'path': FOLDER_PATH,
        'recursive': False,
    }

    response = requests.post(list_files_url, headers=headers, json=params)

    if response.status_code == 200:
        files = [entry['name'] for entry in response.json()['entries'] if entry['.tag'] == 'file']
        
        video_txt_exists = os.path.exists('video.txt')
    
        if not video_txt_exists:
            with open('video.txt', 'w') as file:
                file.write('')
                print('Файл video.txt успешно создан.')

        with open('video.txt', 'r') as file:
            existing_files = [line.strip() for line in file.readlines()]

        new_files = [file_name for file_name in files if file_name not in existing_files]

        if new_files:
            with open('video.txt', 'a') as file:
                file.write('\n'.join(new_files) + '\n')

            new_file = new_files[-1]  # Берем последний файл из списка новых файлов

            download_url = 'https://content.dropboxapi.com/2/files/download'
            headers = {
                'Authorization': f'Bearer {ACCESS_TOKEN}',
                'Dropbox-API-Arg': f'{{"path": "{FOLDER_PATH}/{new_file}"}}'
            }

            download_response = requests.post(download_url, headers=headers)

            if download_response.status_code == 200:
                with open(new_file, 'wb') as downloaded_file:
                    downloaded_file.write(download_response.content)
                full_path = os.path.abspath(new_file)  # Get the full path to the downloaded file
                foto(full_path)
    
                print(f'Файл {full_path} успешно скачан.')

                
            else:
                print(f'Ошибка при скачивании файла {new_file}: {download_response.status_code}')
    else:
        print(f'Ошибка: {response.status_code}')
    
    time.sleep(10)  # Пауза 10 секунд между проверками
