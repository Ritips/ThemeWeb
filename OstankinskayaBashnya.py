from distance import lonlat_distance
from math import sqrt
import requests


def get_point(name):
    geocoder_api = 'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b'
    geocode = f"&geocode={name}&format=json"
    request = geocoder_api + geocode
    response = requests.get(request)
    if not response:
        print(response.reason, response)
        print(response.url)
        return
    json_object = response.json()
    toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return ','.join(toponym["Point"]["pos"].split())


def main():
    address = input('Input address to analise: ')
    height = 525 / 1000
    point_1 = tuple(map(float, get_point("Останкинская башня").split(',')))
    point_2 = tuple(map(float, get_point(address).split(',')))
    length = lonlat_distance(point_1, point_2)
    height2 = (length / 3.6 - sqrt(height)) ** 2
    print(height2 * 1000)


if __name__ == '__main__':
    main()
