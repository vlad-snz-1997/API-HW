import requests
from io import StringIO
import json
import os
from dotenv import load_dotenv

load_dotenv()

class IPDetector:
    def __init__(self):
        pass

    def get_ip(self):
        self.url_get_ip = 'https://api.ipify.org/?format=json'
        self.response=requests.get(self.url_get_ip)
        self.ip_number = self.response.json()['ip']
        json_ip = self.response.json()['ip']
        return json_ip

class IPInfo:
    def __init__(self):
        pass

    def get_info_ip(self):
        ip = IPDetector.get_ip(self)
        self.url_ip_info = f'https://ipinfo.io/{ip}/geo'
        self.response=requests.get(self.url_ip_info)
        self.info_ip = self.response.json()
        
        # Создаём байтовый буфер
        bytes_buffer = StringIO ()
        # Сериализуем данные в JSON и сразу записываем в буфер
        json.dump(self.info_ip, bytes_buffer)
        # Получаем байты из буфера
        json_bytes = bytes_buffer.getvalue()
        bytes_buffer.close()
        print(self.info_ip)
        return json_bytes

class YandexUploader:
    def __init__(self,token):
        self.url_yandex_disk = 'https://cloud-api.yandex.net/'
        self.headers = {'Authorization': f'OAuth {token}'}
        
        
    def create_folder(self,path):      
        response=requests.put(f'{self.url_yandex_disk}v1/disk/resources',
                              headers=self.headers,
                              params={'path':path})
        if response.status_code == 201:
            print('Папка создана')
        return  response.status_code == 201

    def upload_file(self,path_file,path_yd):
        json_bytes = IPInfo.get_info_ip(self)
        self.response=requests.get(f'{self.url_yandex_disk}v1/disk/resources/upload',headers=self.headers,params={'path':path_yd,'overwrite':True})
        url_put_file = self.response.json()['href']
        self.response=requests.put(url_put_file,headers=self.headers,files={'file':(path_file, json_bytes)})
        print(f'файл создан')
        return self.response.status_code == 200


if __name__ == '__main__':
    token = os.getenv('TOKEN')
    api_yandex_disk = YandexUploader(token) 
    api_yandex_disk.create_folder('ip_info')  
    api_yandex_disk.upload_file('info_ip.txt','ip_info/info_ip.txt')  