from distance import lonlat_distance
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
    address_school = input('Input address school: ')
    address_home = input("Input address home: ")
    point_school = tuple(map(float, get_point(address_school).split(',')))
    point_home = tuple(map(float, get_point(address_home).split(',')))
    print(round(lonlat_distance(point_home, point_school)), 'metres')


if __name__ == '__main__':
    main()
