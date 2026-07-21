import requests
from io import BytesIO
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
        self.ip = self.response.json()['ip']
        print(self.ip)# не работает принт
        return self.ip

class IPInfo:
    def __init__(self,ip):
        pass

    def get_info_ip(self,ip):
        self.url_ip_info = f'https://ipinfo.io/{self.ip}/geo'
        self.response=requests.get(self.url_ip_info)
        self.info_ip = self.response.json()
        
        # Создаём байтовый буфер
        buffer = BytesIO()
        # Сериализуем данные в JSON 
        self.json_srting = json.dumps(self.info_ip).encode('utf-8')
        # записываем сериалезованные данные в буфер
        buffer.write(self.json_bytes)
        # Извлекаем байты из потока в переменную
        self.json_bytes = buffer.getvalue() 
        # ОШИБКА    TypeError: a bytes-like object is required, not 'IPInfo'
        print(self.json_bytes) # не работает принт
        buffer.close()
        return self.json_bytes # возвращаем байтовый объект

class YandexUploader:
    def __init__(self,token,json_bytes):
        self.json_bytes = json_bytes
        self.url_yandex_disk = 'https://cloud-api.yandex.net/'
        self.headers = {'Authorization': f'OAuth {token}'}
        
        
    def create_folder(self,path):      
        response=requests.put(f'{self.url_yandex_disk}v1/disk/resources',
                              headers=self.headers,
                              params={'path':path})
        if response.status_code == 201:
            print('Папка создана')
        return  response.status_code == 201

    def upload_file(self,json_bytes,path_file,path_yd):
        self.json_bytes = json_bytes
        self.response=requests.get(f'{self.url_yandex_disk}v1/disk/resources/upload',headers=self.headers,params={'path':path_yd,'overwrite':True})
        url_put_file = self.response.json()['href']
        self.response=requests.put(url_put_file,headers=self.headers,files={'file':(path_file, self.json_bytes)})
        print(f'файл создан')
        return self.response.status_code == 200


if __name__ == '__main__':
    api_get_ip = IPDetector()
    api_ip_info = IPInfo(api_get_ip)
    token = os.getenv('TOKEN')
    api_yandex_disk = YandexUploader(token,api_ip_info) # авторизуемся на яндекс диске
    api_yandex_disk.create_folder('ip_info') # создаем папку 
    api_yandex_disk.upload_file(api_ip_info,'info_ip.txt','ip_info/info_ip.txt') # загружаем файл 
