import requests

begin = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b"
origin = 'Красная пл-дь, 1'
geocode = "geocode=стадион Лужники Москва"
out_format = "format=json"
response = requests.get(f'{begin}&{geocode}&{out_format}')
if response:
    json_object = response.json()
    toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    toponym_coord = toponym["Point"]["pos"]
    print(f'Address: {toponym_address}; Coords: {toponym_coord}')
