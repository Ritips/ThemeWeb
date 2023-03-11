import requests
import sys


def get_toponym(toponym_to_find, kind=None):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"
    }
    if kind:
        geocoder_params["kind"] = kind
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print(response, response.url)
        return
    json_object = response.json()
    return json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_point(toponym):
    return tuple(map(float, toponym["Point"]["pos"].split()))


def get_name(toponym):
    return toponym["metaDataProperty"]["GeocoderMetaData"]["text"]


def main():
    address = ' '.join(sys.argv[1:])
    toponym = get_toponym(address)
    point = get_point(toponym)
    toponym2 = get_toponym(f"{point[0]},{point[1]}", kind="district")
    print(get_name(toponym2))


if __name__ == '__main__':
    main()
